"""Import the version-pinned RaptorMaps infrared module dataset and create research splits."""

import argparse
import csv
import hashlib
import json
import shutil
import urllib.request
import zipfile
from collections import Counter
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from training.raptormaps_thermal import (
    CLASS_NAMES,
    ambiguous_hashes,
    normalize_class_name,
    safe_image_member,
    split_records,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "raptormaps_infrared_solar_modules"
SOURCE_VERSION = "88e2d1febbcefe401c17ec80b8973f36a02a1653"
SOURCE_URL = "https://github.com/RaptorMaps/InfraredSolarModules"
ARCHIVE_URL = (
    "https://raw.githubusercontent.com/RaptorMaps/InfraredSolarModules/"
    f"{SOURCE_VERSION}/2020-02-14_InfraredSolarModules.zip"
)
ARCHIVE_SHA256 = "b82c706bc719b045ac4f8930570d81767a8a170d0998ca3e09283b585db05b5e"
LICENSE = "MIT (repository-declared; see source LICENSE)"
ARCHIVE_PATH = ROOT / "datasets" / ".cache" / "InfraredSolarModules_2020-02-14.zip"
RAW_OUTPUT = ROOT / "datasets" / "raw" / "raptormaps_thermal_v1"
SPLIT_OUTPUT = ROOT / "datasets" / "processed" / "thermal_infrared"
SOURCE_MANIFEST = ROOT / "datasets" / "source_manifest.csv"
GROUPS_MANIFEST = ROOT / "datasets" / "image_groups.csv"
REPORT_PATH = ROOT / "datasets" / "import_reports" / "raptormaps_thermal_v1.json"


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_archive(destination=ARCHIVE_PATH):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".download")
    request = urllib.request.Request(ARCHIVE_URL, headers={"User-Agent": "Agastya-EYE research"})
    try:
        with urllib.request.urlopen(request, timeout=90) as response, temporary.open("wb") as output:
            shutil.copyfileobj(response, output)
        if sha256_file(temporary) != ARCHIVE_SHA256:
            raise ValueError("RaptorMaps archive checksum does not match the pinned source snapshot")
        temporary.replace(destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return destination


def read_archive(archive_path):
    archive_path = Path(archive_path)
    if sha256_file(archive_path) != ARCHIVE_SHA256:
        raise ValueError("archive checksum differs from the pinned RaptorMaps source snapshot")
    with zipfile.ZipFile(archive_path) as archive:
        names = set(archive.namelist())
        metadata_path = "InfraredSolarModules/module_metadata.json"
        if metadata_path not in names:
            raise ValueError("archive is missing module_metadata.json")
        metadata = json.loads(archive.read(metadata_path))
        if len(metadata) != 20_000:
            raise ValueError(f"expected 20,000 metadata records, found {len(metadata)}")

        rows = []
        image_bytes_by_id = {}
        for image_id, entry in metadata.items():
            if not str(image_id).isdecimal() or not isinstance(entry, dict):
                raise ValueError(f"invalid metadata record for image {image_id!r}")
            relative_member = safe_image_member(entry.get("image_filepath"))
            archive_member = f"InfraredSolarModules/{relative_member}"
            if archive_member not in names:
                raise ValueError(f"archive image is missing: {archive_member}")
            source_class = entry.get("anomaly_class")
            class_name = normalize_class_name(source_class)
            content = archive.read(archive_member)
            try:
                with Image.open(BytesIO(content)) as image:
                    image.verify()
                with Image.open(BytesIO(content)) as image:
                    if image.size != (24, 40):
                        raise ValueError(f"unexpected thermal image size for {image_id}: {image.size}")
            except (UnidentifiedImageError, OSError) as error:
                raise ValueError(f"invalid image data for {image_id}") from error
            image_bytes_by_id[str(image_id)] = content
            rows.append({
                "image_id": str(image_id),
                "source_class": source_class,
                "class_name": class_name,
                "sha256": sha256_bytes(content),
            })
    return rows, image_bytes_by_id


def write_csv(path, fields, rows):
    with Path(path).open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def update_source_manifests(rows):
    source_rows = []
    for label in CLASS_NAMES:
        original = next(row["source_class"] for row in rows if row["class_name"] == label)
        source_rows.append({
            "source_id": SOURCE_ID,
            "source_version": SOURCE_VERSION,
            "source_url": SOURCE_URL,
            "license": LICENSE,
            "original_class": original,
            "normalized_class": f"thermal_{label}",
            "task": "thermal_module_classification",
            "modality": "thermal_infrared",
        })

    manifest_fields = (
        "source_id", "source_version", "source_url", "license", "original_class",
        "normalized_class", "task", "modality",
    )
    prior = []
    if SOURCE_MANIFEST.is_file():
        with SOURCE_MANIFEST.open("r", encoding="utf-8-sig", newline="") as file:
            prior = [row for row in csv.DictReader(file) if row.get("source_id") != SOURCE_ID]
    for row in prior:
        row["task"] = row.get("task") or "rgb_image_classification"
        row["modality"] = row.get("modality") or "visible_rgb"
    SOURCE_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_MANIFEST, manifest_fields, [*prior, *source_rows])

    group_rows = []
    for row in rows:
        group_rows.append({
            "source_id": SOURCE_ID,
            "relative_path": f"{row['class_name']}/{row['image_id']}.jpg",
            "group_id": f"sha256:{row['sha256']}",
        })
    prior_groups = []
    if GROUPS_MANIFEST.is_file():
        with GROUPS_MANIFEST.open("r", encoding="utf-8-sig", newline="") as file:
            prior_groups = [row for row in csv.DictReader(file) if row.get("source_id") != SOURCE_ID]
    write_csv(GROUPS_MANIFEST, ("source_id", "relative_path", "group_id"), [*prior_groups, *group_rows])


def import_archive(archive_path=ARCHIVE_PATH, raw_output=RAW_OUTPUT, split_output=SPLIT_OUTPUT, seed=42):
    raw_output = Path(raw_output).resolve()
    split_output = Path(split_output).resolve()
    raw_root = (ROOT / "datasets" / "raw").resolve()
    processed_root = (ROOT / "datasets" / "processed").resolve()
    if not raw_output.is_relative_to(raw_root) or raw_output == raw_root:
        raise ValueError("raw output must stay inside datasets/raw")
    if not split_output.is_relative_to(processed_root) or split_output == processed_root:
        raise ValueError("split output must stay inside datasets/processed")
    if raw_output.exists() or split_output.exists():
        raise FileExistsError("dataset output already exists; move the existing output before re-importing")

    records, image_bytes_by_id = read_archive(archive_path)
    ambiguous = ambiguous_hashes(records)
    trainable_records = [row for row in records if row["sha256"] not in ambiguous]
    split_rows = split_records(trainable_records, seed=seed)
    raw_staging = raw_output.with_name(raw_output.name + ".staging")
    split_staging = split_output.with_name(split_output.name + ".staging")
    if raw_staging.exists() or split_staging.exists():
        raise FileExistsError("a prior dataset staging folder exists; inspect it before importing again")
    raw_staging.mkdir(parents=True)
    split_staging.mkdir(parents=True)
    try:
        shutil.copy2(ROOT / "datasets" / "licenses" / "RaptorMaps-MIT-LICENSE.txt", raw_staging / "LICENSE.txt")
        shutil.copy2(ROOT / "datasets" / "licenses" / "RaptorMaps-MIT-LICENSE.txt", split_staging / "LICENSE.txt")
        for row in records:
            destination = raw_staging / row["class_name"] / f"{row['image_id']}.jpg"
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(image_bytes_by_id[row["image_id"]])

        unique_rows = {}
        for row in split_rows:
            unique_rows.setdefault(row["sha256"], row)
        all_unique_hashes = {row["sha256"] for row in records}
        manifest_rows = []
        counts = {split: Counter() for split in ("train", "validation", "test")}
        for row in sorted(unique_rows.values(), key=lambda item: item["image_id"]):
            split = row["split"]
            relative = f"{split}/{row['class_name']}/{row['image_id']}.jpg"
            destination = split_staging / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(image_bytes_by_id[row["image_id"]])
            counts[split][row["class_name"]] += 1
            manifest_rows.append({
                "relative_path": relative,
                "source_id": SOURCE_ID,
                "source_version": SOURCE_VERSION,
                "source_url": SOURCE_URL,
                "license": LICENSE,
                "modality": "thermal_infrared",
                "task": "thermal_module_classification",
                "original_class": row["source_class"],
                "class_name": row["class_name"],
                "image_id": row["image_id"],
                "sha256": row["sha256"],
                "group_id": row["group_id"],
                "split": split,
            })
        write_csv(
            split_staging / "thermal_manifest.csv",
            ("relative_path", "source_id", "source_version", "source_url", "license", "modality",
             "task", "original_class", "class_name", "image_id", "sha256", "group_id", "split"),
            manifest_rows,
        )
        ambiguous_rows = [
            {
                "sha256": digest,
                "source_classes": "|".join(classes),
                "image_ids": "|".join(sorted(row["image_id"] for row in records if row["sha256"] == digest)),
                "excluded_from_training": True,
            }
            for digest, classes in sorted(ambiguous.items())
        ]
        write_csv(
            split_staging / "ambiguous_duplicates.csv",
            ("sha256", "source_classes", "image_ids", "excluded_from_training"),
            ambiguous_rows,
        )
        report = {
            "source_id": SOURCE_ID,
            "source_version": SOURCE_VERSION,
            "source_url": SOURCE_URL,
            "license": LICENSE,
            "archive_sha256": ARCHIVE_SHA256,
            "image_count": len(records),
            "trainable_image_records": len(trainable_records),
            "unique_images": len(all_unique_hashes),
            "trainable_unique_images": len(unique_rows),
            "exact_duplicate_images": len(records) - len(all_unique_hashes),
            "ambiguous_duplicate_groups": len(ambiguous),
            "ambiguous_duplicate_records": sum(1 for row in records if row["sha256"] in ambiguous),
            "class_counts": {split: dict(sorted(count.items())) for split, count in counts.items()},
            "split_method": "stratified random split by exact-image SHA-256; source has no physical module IDs",
            "seed": seed,
            "research_limitations": [
                "Image-level split only; physical-panel/site independent performance cannot be estimated.",
                "Thermal crops are 40x24 pixels and are not visible-RGB ESP32-CAM images.",
                "Source labels do not include separate burned or broken classes, defect boxes, or severity.",
                "Thermal pixel values are normalized grayscale, not calibrated temperature readings.",
                "Six identical-pixel groups have conflicting source class labels and are excluded from training.",
            ],
            "imported_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        (raw_staging / "agastya_import.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        (split_staging / "import_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        raw_staging.replace(raw_output)
        split_staging.replace(split_output)
        update_source_manifests(records)
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    except Exception:
        if raw_staging.exists():
            shutil.rmtree(raw_staging)
        if split_staging.exists():
            shutil.rmtree(split_staging)
        raise
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=ARCHIVE_PATH)
    parser.add_argument("--download", action="store_true", help="Download the pinned source ZIP if missing")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    try:
        archive_path = args.archive
        if not archive_path.is_file() and args.download:
            archive_path = download_archive(archive_path)
        print(json.dumps(import_archive(archive_path, seed=args.seed), indent=2))
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
