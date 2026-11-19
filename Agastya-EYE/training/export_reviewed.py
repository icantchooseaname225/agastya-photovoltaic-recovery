"""Export only human-confirmed inspection images into the training source set."""

import argparse
import csv
import hashlib
import os
import re
import shutil
import sqlite3
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "eye.sqlite3"
RAW_ROOT = ROOT / "datasets" / "raw"
MANIFEST_PATH = ROOT / "datasets" / "source_manifest.csv"
GROUPS_PATH = ROOT / "datasets" / "image_groups.csv"
SOURCE_ID = "operator_review"
SOURCE_VERSION = "agastya-eye-ledger-v1.2"
SOURCE_URL = "local://agastya-eye/operator-captures"
LICENSE = "Operator-captured; locally supplied and human-labeled"
LABELS = {"clean", "dust", "crack", "broken", "burned", "snow", "bird_drop", "other"}


def read_rows(path):
    if not path.is_file():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_rows(path, fields, rows):
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


class DisjointSet:
    def __init__(self):
        self.parent = {}

    def find(self, item):
        self.parent.setdefault(item, item)
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, left, right):
        a, b = self.find(left), self.find(right)
        if a != b:
            self.parent[max(a, b)] = min(a, b)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DB_PATH)
    args = parser.parse_args()
    database = args.database.resolve()
    try:
        with sqlite3.connect(database) as connection:
            connection.row_factory = sqlite3.Row
            records = connection.execute(
                """SELECT i.id, i.image_path, i.image_sha256, i.confirmed_visual_label, p.panel_id
                   FROM inspections i JOIN panels p ON p.id = i.panel_row_id
                   WHERE i.confirmed_visual_label IS NOT NULL ORDER BY i.id"""
            ).fetchall()
        if not records:
            print("No human-confirmed visual labels to export.")
            return

        groups = DisjointSet()
        payloads = []
        digest_labels = {}
        image_root = ROOT / "images"
        for record in records:
            label = record["confirmed_visual_label"]
            if label not in LABELS:
                raise ValueError(f"Inspection {record['id']} has an unsupported confirmed label: {label}")
            source_path = (ROOT / record["image_path"]).resolve()
            if not source_path.is_relative_to(image_root.resolve()) or not source_path.is_file():
                raise ValueError(f"Inspection {record['id']} image is missing or outside images/")
            digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
            if record["image_sha256"] and digest != record["image_sha256"]:
                raise ValueError(f"Inspection {record['id']} image failed its stored SHA-256 check")
            if digest in digest_labels and digest_labels[digest] != label:
                raise ValueError(f"Identical image bytes have conflicting labels: {digest[:12]}")
            digest_labels[digest] = label
            panel_node = f"panel:{record['panel_id']}"
            image_node = f"image:{digest}"
            groups.union(panel_node, image_node)
            payloads.append({
                "id": record["id"],
                "source_path": source_path,
                "digest": digest,
                "label": label,
                "panel_id": record["panel_id"],
                "panel_node": panel_node,
            })

        component_members = defaultdict(list)
        for node in groups.parent:
            component_members[groups.find(node)].append(node)
        component_ids = {
            root: "operator:" + hashlib.sha256("|".join(sorted(nodes)).encode("utf-8")).hexdigest()[:20]
            for root, nodes in component_members.items()
        }

        source_root = RAW_ROOT / SOURCE_ID
        source_root.mkdir(parents=True, exist_ok=True)
        group_rows = []
        for item in payloads:
            filename = f"inspection_{item['id']}_{item['digest'][:12]}.jpg"
            destination = source_root / item["label"] / filename
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                if hashlib.sha256(destination.read_bytes()).hexdigest() != item["digest"]:
                    raise ValueError(f"Refusing to replace changed training image: {destination}")
            else:
                shutil.copy2(item["source_path"], destination)
            group_rows.append({
                "source_id": SOURCE_ID,
                "relative_path": destination.relative_to(source_root).as_posix(),
                "group_id": component_ids[groups.find(item["panel_node"])],
            })

        manifest = [row for row in read_rows(MANIFEST_PATH) if row.get("source_id") != SOURCE_ID]
        labels = sorted({item["label"] for item in payloads})
        manifest.extend({
            "source_id": SOURCE_ID,
            "source_version": SOURCE_VERSION,
            "source_url": SOURCE_URL,
            "license": LICENSE,
            "original_class": label,
            "normalized_class": label,
            "task": "rgb_image_classification",
            "modality": "visible_rgb",
        } for label in labels)
        write_rows(MANIFEST_PATH,
                   ("source_id", "source_version", "source_url", "license", "original_class", "normalized_class", "task", "modality"),
                   manifest)

        existing_groups = [row for row in read_rows(GROUPS_PATH) if row.get("source_id") != SOURCE_ID]
        write_rows(GROUPS_PATH, ("source_id", "relative_path", "group_id"), [*existing_groups, *group_rows])
        counts = defaultdict(int)
        for item in payloads:
            counts[item["label"]] += 1
        print(f"Exported {len(payloads)} human-confirmed inspections to {source_root}")
        print("By class: " + ", ".join(f"{label}={count}" for label, count in sorted(counts.items())))
        print("Next: py training/prepare_dataset.py --overwrite")
    except (OSError, sqlite3.Error, ValueError, csv.Error) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
