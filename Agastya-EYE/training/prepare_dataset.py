"""Normalize licensed source datasets into leakage-aware MobileNet folders."""

import argparse
import csv
import hashlib
import json
import random
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "datasets" / "raw"
DEFAULT_MANIFEST = ROOT / "datasets" / "source_manifest.csv"
DEFAULT_GROUPS = ROOT / "datasets" / "image_groups.csv"
DEFAULT_OUTPUT = ROOT / "datasets" / "processed"
LABELS = ("clean", "dust", "crack", "broken", "burned", "snow", "bird_drop", "other")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
SAFE_ID = re.compile(r"^[A-Za-z0-9_-]+$")


def read_mappings(path):
    mappings = {}
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"source_id", "source_version", "source_url", "license", "original_class", "normalized_class"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path} must contain columns: {', '.join(sorted(required))}")
        for row in reader:
            task = (row.get("task") or "rgb_image_classification").strip()
            if task != "rgb_image_classification":
                continue
            source_id = (row.get("source_id") or "").strip()
            if not source_id:
                continue
            source_version = (row.get("source_version") or "").strip()
            source_url = (row.get("source_url") or "").strip()
            license_name = (row.get("license") or "").strip()
            original_class = (row.get("original_class") or "").strip()
            normalized_class = (row.get("normalized_class") or "").strip()
            if not SAFE_ID.fullmatch(source_id):
                raise ValueError(f"Unsafe source_id: {source_id!r}")
            if not source_version or not source_url or not license_name or not original_class:
                raise ValueError(f"Mapping for {source_id}/{original_class} is missing its version, source URL, or license")
            local_capture_source = source_id == "operator_review" and source_url == "local://agastya-eye/operator-captures"
            if not local_capture_source and not source_url.startswith(("https://", "http://")):
                raise ValueError(f"Source URL for {source_id}/{original_class} must use http or https")
            if original_class in (".", "..") or "/" in original_class or "\\" in original_class:
                raise ValueError(f"original_class must be a single folder name: {original_class!r}")
            if normalized_class not in LABELS:
                raise ValueError(f"Unknown normalized class {normalized_class!r}; use one of {', '.join(LABELS)}")
            key = (source_id, original_class)
            mapping = {
                "source_id": source_id,
                "source_version": source_version,
                "source_url": source_url,
                "license": license_name,
                "original_class": original_class,
                "normalized_class": normalized_class,
                "task": task,
                "modality": (row.get("modality") or "visible_rgb").strip(),
            }
            if key in mappings and mappings[key] != mapping:
                raise ValueError(f"Conflicting mappings for {source_id}/{original_class}")
            mappings[key] = mapping
    if not mappings:
        raise ValueError("Add verified class mappings to datasets/source_manifest.csv before preparing data")
    return mappings


def read_groups(path):
    groups = {}
    if not path.is_file():
        return groups
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"source_id", "relative_path", "group_id"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path} must contain columns: {', '.join(sorted(required))}")
        for row in reader:
            source_id = (row.get("source_id") or "").strip()
            relative_path = (row.get("relative_path") or "").strip().replace("\\", "/")
            group_id = (row.get("group_id") or "").strip()
            if not (source_id and relative_path and group_id):
                continue
            groups[(source_id, relative_path)] = group_id
    return groups


def digest_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assign_group_splits(samples_by_class, seed):
    keys = sorted({
        sample["group_key"]
        for samples in samples_by_class.values()
        for sample in samples
    })
    random.Random(seed).shuffle(keys)
    count = len(keys)
    if count == 1:
        train_count = 1
        validation_count = 0
    elif count == 2:
        train_count = 1
        validation_count = 1
    else:
        train_count = min(count - 2, max(1, round(count * 0.70)))
        validation_count = min(count - train_count - 1, max(1, round(count * 0.15)))
    train_keys = set(keys[:train_count])
    validation_keys = set(keys[train_count:train_count + validation_count])
    return {
        key: (
            "train" if key in train_keys else
            "validation" if key in validation_keys else "test"
        )
        for key in keys
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--groups", type=Path, default=DEFAULT_GROUPS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing processed directory")
    args = parser.parse_args()

    try:
        mappings = read_mappings(args.manifest)
        image_groups = read_groups(args.groups)
        samples_by_class = defaultdict(list)
        digest_labels = {}
        seen_source_hashes = set()
        for (source_id, original_class), mapping in mappings.items():
            class_dir = RAW_ROOT / source_id / original_class
            if not class_dir.is_dir():
                print(f"Skipping {source_id}/{original_class}: folder not found", file=sys.stderr)
                continue
            for image_path in sorted(class_dir.rglob("*")):
                if not image_path.is_file() or image_path.suffix.lower() not in IMAGE_SUFFIXES:
                    continue
                digest = digest_file(image_path)
                label = mapping["normalized_class"]
                previous_label = digest_labels.get(digest)
                if previous_label and previous_label != label:
                    raise ValueError(f"Same image has conflicting labels: {image_path} ({previous_label} vs {label})")
                if (source_id, digest) in seen_source_hashes:
                    continue
                seen_source_hashes.add((source_id, digest))
                digest_labels[digest] = label
                relative_path = image_path.relative_to(RAW_ROOT / source_id).as_posix()
                group_id = image_groups.get((source_id, relative_path))
                samples_by_class[label].append({
                    **mapping,
                    "path": image_path,
                    "digest": digest,
                    "group_key": group_id or f"sha256:{digest}",
                    "group_id": group_id or "",
                    "relative_path": relative_path,
                })

        if not any(samples_by_class.values()):
            raise ValueError("No mapped images found under datasets/raw/<source_id>/<original_class>/")
        group_splits = assign_group_splits(samples_by_class, args.seed)
        output = args.output.resolve()
        if output.exists():
            if not args.overwrite:
                raise ValueError(f"{output} already exists; use --overwrite to replace generated data")
            datasets_root = (ROOT / "datasets").resolve()
            if output == datasets_root or not output.is_relative_to(datasets_root):
                raise ValueError("Refusing to replace an output folder outside datasets/")
            shutil.rmtree(output)

        manifest_rows = []
        summary = {split: {label: 0 for label in LABELS} for split in ("train", "validation", "test")}
        for label in LABELS:
            samples = samples_by_class[label]
            if not samples:
                continue
            group_counts = len({sample["group_key"] for sample in samples})
            if group_counts < 3:
                print(f"Warning: {label} has {group_counts} independent groups; training needs train, validation, and test data", file=sys.stderr)
            for sample in samples:
                split = group_splits[sample["group_key"]]
                filename = f"{sample['source_id']}_{sample['digest'][:16]}{sample['path'].suffix.lower()}"
                destination = output / split / label / filename
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(sample["path"], destination)
                summary[split][label] += 1
                manifest_rows.append({
                    "processed_path": destination.relative_to(output).as_posix(),
                    "source_id": sample["source_id"],
                    "source_version": sample["source_version"],
                    "source_url": sample["source_url"],
                    "license": sample["license"],
                    "original_class": sample["original_class"],
                    "normalized_class": label,
                    "sha256": sample["digest"],
                    "group_id": sample["group_id"],
                    "split": split,
                })

        with (output / "processed_manifest.csv").open("w", encoding="utf-8", newline="") as file:
            fields = ("processed_path", "source_id", "source_version", "source_url", "license", "original_class", "normalized_class", "sha256", "group_id", "split")
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(manifest_rows)
        (output / "summary.json").write_text(json.dumps({"seed": args.seed, "classes": list(LABELS), "counts": summary}, indent=2), encoding="utf-8")
        print(json.dumps(summary, indent=2))
    except (OSError, ValueError, csv.Error) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
