"""Audited helpers for the PV-Multi-Defect Pascal VOC source."""

import random
import json
import xml.etree.ElementTree as ET
from pathlib import PurePosixPath, PurePath


CLASS_NAMES = ("black_border", "broken", "hot_spot", "no_electricity", "scratch")
SPLIT_RATIOS = {"train": 0.70, "validation": 0.15, "test": 0.15}


def parse_voc_annotation(xml_bytes):
    try:
        root = ET.fromstring(xml_bytes)
        filename = (root.findtext("filename") or "").strip()
        size = root.find("size")
        width = int(size.findtext("width"))
        height = int(size.findtext("height"))
    except (ET.ParseError, AttributeError, TypeError, ValueError) as error:
        raise ValueError(f"invalid Pascal VOC annotation: {error}") from error

    if not filename or filename in (".", "..") or PurePath(filename).name != filename:
        raise ValueError("VOC filename must be a plain image filename")
    if width < 1 or height < 1:
        raise ValueError("VOC image dimensions must be positive")

    objects = []
    for item in root.findall("object"):
        label = (item.findtext("name") or "").strip().lower().replace(" ", "_")
        if label not in CLASS_NAMES:
            raise ValueError(f"unsupported VOC class: {label or '<empty>'}")
        box = item.find("bndbox")
        try:
            xmin, ymin, xmax, ymax = (
                int(box.findtext(key)) for key in ("xmin", "ymin", "xmax", "ymax")
            )
        except (AttributeError, TypeError, ValueError) as error:
            raise ValueError("VOC object has an invalid bounding box") from error
        if not (1 <= xmin <= xmax <= width and 1 <= ymin <= ymax <= height):
            raise ValueError("VOC bounding box is outside image bounds")
        objects.append({
            "label": label,
            "bbox_xyxy": [xmin - 1, ymin - 1, xmax, ymax],
        })

    return {"filename": filename, "width": width, "height": height, "objects": objects}


def split_grouped_records(records, seed=42):
    """Assign identical pixel hashes together using a deterministic multilabel split."""
    groups = {}
    for record in records:
        group_id = str(record.get("sha256") or "").strip()
        image_id = str(record.get("image_id") or "").strip()
        if not group_id or not image_id:
            raise ValueError("each split record needs image_id and sha256")
        labels = set(record.get("labels") or ())
        unknown = labels - set(CLASS_NAMES)
        if unknown:
            raise ValueError(f"unsupported source labels: {', '.join(sorted(unknown))}")
        group = groups.setdefault(group_id, {"rows": [], "labels": set()})
        group["rows"].append(record)
        group["labels"].update(labels)

    if not groups:
        raise ValueError("no annotated image records to split")

    label_frequency = {label: sum(label in group["labels"] for group in groups.values())
                       for label in CLASS_NAMES}
    rng = random.Random(seed)
    ordered = list(groups.items())
    rng.shuffle(ordered)
    ordered.sort(key=lambda item: (
        -sum(1 / label_frequency[label] for label in item[1]["labels"] if label_frequency[label]),
        -len(item[1]["labels"]),
    ))

    targets = {
        split: {label: len(groups) * ratio for label in CLASS_NAMES}
        for split, ratio in SPLIT_RATIOS.items()
    }
    target_sizes = {split: len(groups) * ratio for split, ratio in SPLIT_RATIOS.items()}
    assigned_labels = {split: {label: 0 for label in CLASS_NAMES} for split in SPLIT_RATIOS}
    assigned_sizes = {split: 0 for split in SPLIT_RATIOS}
    assignments = {}

    for group_id, group in ordered:
        def score(split):
            label_scores = [
                (targets[split][label] - assigned_labels[split][label]) / max(targets[split][label], 1)
                for label in group["labels"]
            ]
            label_score = sum(label_scores) / len(label_scores) if label_scores else 0
            size_score = (target_sizes[split] - assigned_sizes[split]) / max(target_sizes[split], 1)
            return label_score + 0.25 * size_score

        split = max(SPLIT_RATIOS, key=score)
        assignments[group_id] = split
        assigned_sizes[split] += 1
        for label in group["labels"]:
            assigned_labels[split][label] += 1

    result = []
    for record in records:
        row = dict(record)
        row["group_id"] = str(record["sha256"])
        row["split"] = assignments[row["group_id"]]
        result.append(row)
    return result


def deduplicate_exact_images(records):
    """Keep one exact duplicate only when every source box annotation agrees."""
    groups = {}
    for record in records:
        groups.setdefault(record["sha256"], []).append(record)

    kept = []
    conflicts = []
    for sha256, rows in sorted(groups.items()):
        signatures = {
            json.dumps(row.get("objects", []), sort_keys=True, separators=(",", ":"))
            for row in rows
        }
        if len(signatures) != 1:
            conflicts.append({
                "sha256": sha256,
                "image_ids": sorted(row["image_id"] for row in rows),
                "annotation_versions": len(signatures),
            })
            continue
        kept.append(min(rows, key=lambda row: row["image_id"]))
    return kept, conflicts


def safe_archive_member(member, repository_root, expected_folder):
    path = PurePosixPath(member)
    if (path.is_absolute() or ".." in path.parts or len(path.parts) != 3
            or path.parts[0] != repository_root or path.parts[1] != expected_folder
            or path.name in ("", ".", "..")):
        raise ValueError(f"unexpected archive member: {member}")
    return path.name


def labels_to_multihot(labels):
    unknown = set(labels) - set(CLASS_NAMES)
    if unknown:
        raise ValueError(f"unsupported source labels: {', '.join(sorted(unknown))}")
    present = set(labels)
    return [int(label in present) for label in CLASS_NAMES]


def select_f1_thresholds(probabilities, targets):
    """Choose per-label decision thresholds on validation data only."""
    if not probabilities or len(probabilities) != len(targets):
        raise ValueError("probabilities and targets must have the same non-zero row count")
    class_count = len(probabilities[0])
    if class_count < 1:
        raise ValueError("validation rows must contain at least one class")
    if any(len(row) != class_count for row in probabilities + targets):
        raise ValueError("validation rows do not match the supported class count")

    thresholds = []
    for class_index in range(class_count):
        best_f1 = -1.0
        best_threshold = 0.5
        for step in range(5, 96, 5):
            threshold = step / 100
            true_positive = false_positive = false_negative = 0
            for probs, actual in zip(probabilities, targets):
                predicted = probs[class_index] >= threshold
                expected = bool(actual[class_index])
                true_positive += predicted and expected
                false_positive += predicted and not expected
                false_negative += not predicted and expected
            precision = true_positive / max(true_positive + false_positive, 1)
            recall = true_positive / max(true_positive + false_negative, 1)
            f1 = 2 * precision * recall / max(precision + recall, 1e-12)
            if f1 > best_f1 or (f1 == best_f1 and threshold > best_threshold):
                best_f1 = f1
                best_threshold = threshold
        thresholds.append(best_threshold)
    return thresholds
