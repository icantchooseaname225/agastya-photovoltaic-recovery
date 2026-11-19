"""Import the pinned, CC BY 4.0 GitHub panel-inspection dataset."""

import csv
import hashlib
import json
import os
import hashlib
import shutil
import urllib.request
import zipfile
from collections import defaultdict
from io import BytesIO
from pathlib import Path

from PIL import Image, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "datasets" / "raw"
SOURCE_ID = "github_solarpanel_inspection"
SOURCE_VERSION = "868cf7c004cf3cea274d2bfdf398ac6c2216ca47"
SOURCE_URL = "https://github.com/IsuruMunasinghe98/solar-panel-inspection-dataset"
ARCHIVE_URL = f"https://codeload.github.com/IsuruMunasinghe98/solar-panel-inspection-dataset/zip/{SOURCE_VERSION}"
LICENSE = "CC BY 4.0"
LABEL_MAP = {
    "bird drop": "bird_drop",
    "clean": "clean",
    "dusty": "dust",
    "electrical": "other",
    "physical": "other",
}
SOURCE_ROOT = RAW_ROOT / SOURCE_ID
ARCHIVE_CACHE = ROOT / "datasets" / ".cache" / f"{SOURCE_ID}-{SOURCE_VERSION}.zip"


class DisjointSet:
    def __init__(self):
        self.parent = {}

    def find(self, item):
        self.parent.setdefault(item, item)
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, first, second):
        left, right = self.find(first), self.find(second)
        if left != right:
            self.parent[max(left, right)] = min(left, right)


def atomic_csv(path, fields, rows):
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def update_project_csv(path, source_rows, fields, key_field="source_id"):
    previous = []
    if path.is_file():
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            previous = [row for row in csv.DictReader(file) if row.get(key_field) != SOURCE_ID]
    atomic_csv(path, fields, [*previous, *source_rows])


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
    records = {}
    image_count = 0
    missing_images = []
    ARCHIVE_CACHE.parent.mkdir(parents=True, exist_ok=True)
    if not ARCHIVE_CACHE.is_file():
        temporary_archive = ARCHIVE_CACHE.with_suffix(".part")
        request = urllib.request.Request(ARCHIVE_URL, headers={"User-Agent": "Agastya-EYE dataset importer"})
        try:
            with urllib.request.urlopen(request, timeout=90) as response, temporary_archive.open("wb") as output:
                shutil.copyfileobj(response, output)
            temporary_archive.replace(ARCHIVE_CACHE)
        except Exception:
            temporary_archive.unlink(missing_ok=True)
            raise

    archive_digest = sha256_file(ARCHIVE_CACHE)
    with zipfile.ZipFile(ARCHIVE_CACHE) as archive:
            names = archive.namelist()
            marker = "/solar-panel-inspection-dataset/train/_annotations.coco.json"
            annotation_path = next((name for name in names if name.endswith(marker)), None)
            if annotation_path is None:
                raise ValueError("Pinned GitHub archive does not contain the expected COCO annotations")
            archive_prefix = annotation_path[: -len("solar-panel-inspection-dataset/train/_annotations.coco.json")]
            if not archive_prefix:
                raise ValueError("Could not determine the dataset archive root")
            image_members = {}
            for split in ("train", "valid", "test"):
                split_prefix = (archive_prefix + f"solar-panel-inspection-dataset/{split}/").casefold()
                for name in names:
                    if name.casefold().startswith(split_prefix) and not name.endswith("/"):
                        image_members[(split, Path(name).name.casefold())] = name

            for split in ("train", "valid", "test"):
                annotation_member = archive_prefix + f"solar-panel-inspection-dataset/{split}/_annotations.coco.json"
                dataset = json.loads(archive.read(annotation_member))
                categories = {item["id"]: item["name"].strip().lower() for item in dataset["categories"]}
                labels_by_image = defaultdict(set)
                for annotation in dataset["annotations"]:
                    category = categories.get(annotation["category_id"], "")
                    if category in LABEL_MAP:
                        labels_by_image[annotation["image_id"]].add(category)

                for image in dataset["images"]:
                    source_labels = labels_by_image.get(image["id"], set())
                    if not source_labels:
                        continue
                    image_count += 1
                    filename = Path(image["file_name"]).name
                    if filename != image["file_name"] or filename in (".", ".."):
                        raise ValueError(f"Unsafe image path in COCO annotation: {image['file_name']}")
                    member = image_members.get((split, filename.casefold()))
                    if member is None:
                        missing_images.append({"split": split, "filename": filename})
                        continue
                    image_content = archive.read(member)
                    try:
                        with Image.open(BytesIO(image_content)) as picture:
                            picture.verify()
                    except (UnidentifiedImageError, OSError) as error:
                        raise ValueError(f"Invalid image in source archive: {filename}") from error

                    digest = hashlib.sha256(image_content).hexdigest()
                    stem = Path(filename).stem
                    family = stem.split(".rf.", 1)[0].casefold()
                    record = records.setdefault(digest, {
                        "image_bytes": image_content,
                        "filename": filename,
                        "labels": set(),
                        "families": set(),
                    })
                    record["labels"].update(source_labels)
                    record["families"].add(family)

    groups = DisjointSet()
    for digest, record in records.items():
        hash_node = f"sha256:{digest}"
        groups.find(hash_node)
        for family in record["families"]:
            groups.union(hash_node, f"family:{family}")

    component_names = defaultdict(list)
    for node in groups.parent:
        root = groups.find(node)
        if node.startswith("family:"):
            component_names[root].append(node.removeprefix("family:"))
    group_ids = {
        root: "family:" + min(families)
        for root, families in component_names.items()
    }

    source_manifest_rows = []
    source_classes = sorted(set(LABEL_MAP) | {"mixed_categories"})
    for source_class in source_classes:
        normalized = LABEL_MAP.get(source_class, "other")
        source_manifest_rows.append({
            "source_id": SOURCE_ID,
            "source_version": SOURCE_VERSION,
            "source_url": SOURCE_URL,
            "license": LICENSE,
            "original_class": source_class,
            "normalized_class": normalized,
            "task": "rgb_image_classification",
            "modality": "visible_rgb",
        })

    group_rows = []
    class_counts = defaultdict(int)
    used_groups = set()
    for digest, record in sorted(records.items()):
        normalized_labels = {LABEL_MAP[label] for label in record["labels"]}
        source_class = next(iter(record["labels"])) if len(record["labels"]) == 1 else "mixed_categories"
        normalized_class = next(iter(normalized_labels)) if len(normalized_labels) == 1 else "other"
        relative_folder = source_class
        if source_class == "mixed_categories":
            relative_folder = "mixed_categories"
        destination_dir = SOURCE_ROOT / relative_folder
        destination_dir.mkdir(parents=True, exist_ok=True)
        suffix = Path(record["filename"]).suffix.lower() or ".jpg"
        destination = destination_dir / f"{digest[:20]}{suffix}"
        if destination.exists() and hashlib.sha256(destination.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Refusing to overwrite different image data: {destination}")
        if not destination.exists():
            destination.write_bytes(record["image_bytes"])

        relative_path = destination.relative_to(SOURCE_ROOT).as_posix()
        family_group = group_ids[groups.find(f"sha256:{digest}")]
        group_rows.append({"source_id": SOURCE_ID, "relative_path": relative_path, "group_id": family_group})
        used_groups.add(family_group)
        class_counts[normalized_class] += 1

    source_manifest_path = ROOT / "datasets" / "source_manifest.csv"
    update_project_csv(
        source_manifest_path,
        source_manifest_rows,
        ("source_id", "source_version", "source_url", "license", "original_class", "normalized_class", "task", "modality"),
    )
    group_path = ROOT / "datasets" / "image_groups.csv"
    update_project_csv(group_path, group_rows, ("source_id", "relative_path", "group_id"))

    report_path = ROOT / "datasets" / "import_reports" / f"{SOURCE_ID}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps({
        "source_id": SOURCE_ID,
        "pinned_commit": SOURCE_VERSION,
        "archive_sha256": archive_digest,
        "license": LICENSE,
        "annotated_source_images": image_count,
        "unique_images_imported": len(records),
        "missing_annotated_images": missing_images,
    }, indent=2), encoding="utf-8")

    print(json.dumps({
        "source_id": SOURCE_ID,
        "pinned_commit": SOURCE_VERSION,
        "annotated_source_images": image_count,
        "missing_annotated_images": len(missing_images),
        "unique_images_imported": len(records),
        "grouped_image_families": len(used_groups),
        "normalized_class_counts": dict(sorted(class_counts.items())),
        "raw_folder": str(SOURCE_ROOT),
    }, indent=2))


if __name__ == "__main__":
    main()
