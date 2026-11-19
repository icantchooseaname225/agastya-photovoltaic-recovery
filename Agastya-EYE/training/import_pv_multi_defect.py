"""Import the pinned PV-Multi-Defect grayscale close-up research archive."""

import argparse
import csv
import hashlib
import json
import zipfile
from collections import Counter
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

from PIL import Image

from training.pv_surface_defects import (
    CLASS_NAMES,
    deduplicate_exact_images,
    parse_voc_annotation,
    safe_archive_member,
    split_grouped_records,
)

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "2c4df0c1477032d6b0dd9372a517cdbfd6a09e09"
ARCHIVE_SHA256 = "9828728712ea6a819d81b2de907f5cf659396b9a0d7765a015e29e7d3a07ab0e"
SOURCE_URL = "https://github.com/CCNUZFW/PV-Multi-Defect"
ARCHIVE_PATH = ROOT / "datasets" / ".cache" / "pv_multi_defect_2c4df0c.zip"
RAW_ROOT = ROOT / "datasets" / "raw" / "pv_multi_defect_unverified"
PROCESSED_ROOT = ROOT / "datasets" / "processed" / "pv_multi_defect"
RIGHTS_NOTICE = (
    "The source repository does not declare a dataset-specific license. The cited paper is CC BY 3.0, "
    "but that citation does not clearly license the image collection. This copy is retained for local research "
    "and audit only; obtain permission or a clear license before redistribution or publication."
)


def import_report_contract():
    return {
        "source_id": "pv_multi_defect_unverified",
        "source_url": SOURCE_URL,
        "paper_doi": "10.3390/electronics12030561",
        "source_commit": COMMIT,
        "archive_sha256": ARCHIVE_SHA256,
        "modality": "grayscale_camera_crop_unspecified",
        "image_format_note": (
            "camera-captured crops processed to grayscale; the source does not identify the sensor spectral band; "
            "not calibrated temperature, electroluminescence, or full-panel RGB"
        ),
        "source_license_status": "UNDECLARED; local research only pending image-data permission",
        "research_only": True,
        "class_names": list(CLASS_NAMES),
    }


def write_same_or_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file():
        if path.read_bytes() != data:
            raise FileExistsError(f"refusing to overwrite changed source artifact: {path}")
        return
    path.write_bytes(data)


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def _write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2), encoding="utf-8")


def import_archive(archive_path=ARCHIVE_PATH):
    archive_path = Path(archive_path)
    if sha256_bytes(archive_path.read_bytes()) != ARCHIVE_SHA256:
        raise ValueError("PV-Multi-Defect archive SHA-256 does not match the pinned source")
    repository_root = f"PV-Multi-Defect-{COMMIT}"
    image_bytes_by_name = {}
    image_hashes = {}
    image_dimensions = {}
    annotation_members = []
    with zipfile.ZipFile(archive_path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            if info.filename.startswith(f"{repository_root}/JPEGImages/"):
                name = safe_archive_member(info.filename, repository_root, "JPEGImages")
                if Path(name).suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                    continue
                if name in image_bytes_by_name:
                    raise ValueError(f"duplicate image filename in source archive: {name}")
                data = archive.read(info)
                with Image.open(BytesIO(data)) as image:
                    image.verify()
                with Image.open(BytesIO(data)) as image:
                    image_dimensions[name] = image.size
                image_bytes_by_name[name] = data
                image_hashes[name] = sha256_bytes(data)
            elif info.filename.startswith(f"{repository_root}/Annotations/"):
                name = safe_archive_member(info.filename, repository_root, "Annotations")
                if not name.lower().endswith(".xml"):
                    continue
                annotation_members.append((name, archive.read(info)))

        if not image_bytes_by_name or not annotation_members:
            raise ValueError("archive is missing the expected JPEGImages or Annotations tree")

        records = []
        for xml_name, xml_bytes in sorted(annotation_members):
            annotation = parse_voc_annotation(xml_bytes)
            image_name = annotation["filename"]
            if image_name not in image_bytes_by_name:
                raise ValueError(f"annotation references missing image: {image_name}")
            if image_dimensions[image_name] != (annotation["width"], annotation["height"]):
                raise ValueError(f"annotation dimensions do not match image: {xml_name}")
            records.append({
                "image_id": Path(image_name).stem,
                "image_name": image_name,
                "sha256": image_hashes[image_name],
                "source_xml": xml_name,
                "objects": annotation["objects"],
                "labels": sorted({item["label"] for item in annotation["objects"]}),
                "width": annotation["width"],
                "height": annotation["height"],
            })

        # Preserve the source archive exactly for later audits and licensing review.
        for info in archive.infolist():
            if info.is_dir():
                continue
            if not info.filename.startswith(f"{repository_root}/"):
                continue
            relative = Path(*info.filename.split("/")[1:])
            if any(part in ("", ".", "..") for part in relative.parts):
                raise ValueError(f"unsafe source archive path: {info.filename}")
            target = RAW_ROOT / relative
            write_same_or_new(target, archive.read(info))

    kept, conflicting_duplicates = deduplicate_exact_images(records)
    split_records = split_grouped_records(kept, seed=42)
    class_boxes = Counter()
    class_images = Counter()
    split_class_boxes = {split: Counter() for split in ("train", "validation", "test")}
    split_image_counts = Counter()
    manifest_rows = []
    annotation_files = {split: [] for split in split_class_boxes}

    for row in split_records:
        split = row["split"]
        sha256 = row["sha256"]
        output_name = f"{sha256}.jpg"
        output_path = PROCESSED_ROOT / "images" / split / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)
        write_same_or_new(output_path, image_bytes_by_name[row["image_name"]])
        split_image_counts[split] += 1
        for label in row["labels"]:
            class_images[label] += 1
        for item in row["objects"]:
            class_boxes[item["label"]] += 1
            split_class_boxes[split][item["label"]] += 1
        annotation_files[split].append({
            "image": f"images/{split}/{output_name}",
            "image_id": row["image_id"],
            "image_sha256": sha256,
            "width": row["width"],
            "height": row["height"],
            "source_annotation": row["source_xml"],
            "source_license_status": "UNDECLARED; local research copy only",
            "objects": row["objects"],
        })
        manifest_rows.append({
            "image_id": row["image_id"],
            "image": f"images/{split}/{output_name}",
            "sha256": sha256,
            "group_id": row["group_id"],
            "split": split,
            "source_xml": row["source_xml"],
            "labels": ";".join(row["labels"]),
            "object_count": len(row["objects"]),
        })

    PROCESSED_ROOT.mkdir(parents=True, exist_ok=True)
    for split, items in annotation_files.items():
        target = PROCESSED_ROOT / "annotations" / f"{split}.jsonl"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("".join(json.dumps(item, separators=(",", ":")) + "\n" for item in items), encoding="utf-8")
    with (PROCESSED_ROOT / "manifest.csv").open("w", encoding="utf-8", newline="") as file:
        fields = ("image_id", "image", "sha256", "group_id", "split", "source_xml", "labels", "object_count")
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(manifest_rows)

    rights = {"license_status": "UNDECLARED", "notice": RIGHTS_NOTICE, "source_url": SOURCE_URL}
    _write_json(RAW_ROOT / "LOCAL_RESEARCH_RIGHTS.json", rights)
    _write_json(PROCESSED_ROOT / "LOCAL_RESEARCH_RIGHTS.json", rights)
    report = {
        **import_report_contract(),
        "source_images": len(image_bytes_by_name),
        "source_annotation_files": len(annotation_members),
        "annotations_without_image": 0,
        "images_without_annotation": len(set(image_bytes_by_name) - {row["image_name"] for row in records}),
        "annotated_records": len(records),
        "unique_annotated_pixel_hashes": len({row["sha256"] for row in records}),
        "duplicate_conflict_groups_excluded": len(conflicting_duplicates),
        "duplicate_conflict_records_excluded": sum(len(item["image_ids"]) for item in conflicting_duplicates),
        "deduplicated_images_used": len(kept),
        "empty_annotation_images": sum(not row["objects"] for row in kept),
        "class_names": list(CLASS_NAMES),
        "class_box_counts": dict(class_boxes),
        "class_image_counts": dict(class_images),
        "split_image_counts": dict(split_image_counts),
        "split_class_box_counts": {split: dict(counts) for split, counts in split_class_boxes.items()},
        "split_method": "grouped exact-image SHA-256; deterministic multilabel greedy split; no physical panel/site IDs",
        "seed": 42,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "limitations": [
            "The repository does not declare a dataset-specific image license; do not redistribute pending permission.",
            "Source labels are hot_spot, scratch, no_electricity, black_border, and broken; no explicit burnt class.",
            "Exact duplicate images with disagreeing box annotations are quarantined from modeling.",
            "No physical panel/site identifiers exist; image-level held-out performance is not field generalization.",
            "Source sensor spectral band is unspecified; do not treat grayscale values as thermal/EL measurements or assume direct RGB transfer.",
            "Annotations are not severity scores, electrical measurements, or a burned class.",
        ],
    }
    _write_json(PROCESSED_ROOT / "import_report.json", report)
    with (PROCESSED_ROOT / "duplicate_conflicts.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=("sha256", "image_ids", "annotation_versions"))
        writer.writeheader()
        writer.writerows({**row, "image_ids": ";".join(row["image_ids"])} for row in conflicting_duplicates)

    print(json.dumps(report, indent=2))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=ARCHIVE_PATH)
    args = parser.parse_args()
    import_archive(args.archive)


if __name__ == "__main__":
    main()
