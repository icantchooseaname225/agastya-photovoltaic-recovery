"""Label and split the RaptorMaps infrared module-classification dataset."""

import random
import re
from pathlib import PurePosixPath


SOURCE_CLASSES = (
    "Cell",
    "Cell-Multi",
    "Cracking",
    "Diode",
    "Diode-Multi",
    "Hot-Spot",
    "Hot-Spot-Multi",
    "No-Anomaly",
    "Offline-Module",
    "Shadowing",
    "Soiling",
    "Vegetation",
)
CLASS_NAMES = tuple(sorted(re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") for name in SOURCE_CLASSES))
CLASS_BY_SOURCE = {
    name: re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    for name in SOURCE_CLASSES
}


def normalize_class_name(source_name):
    try:
        return CLASS_BY_SOURCE[source_name]
    except (KeyError, TypeError) as error:
        raise ValueError(f"unknown RaptorMaps class: {source_name!r}") from error


def safe_image_member(value):
    if not isinstance(value, str) or "\\" in value or ":" in value:
        raise ValueError(f"unsafe image path: {value!r}")
    path = PurePosixPath(value)
    if (path.is_absolute() or len(path.parts) != 2 or path.parts[0] != "images"
            or path.parts[1] in ("", ".", "..") or path.suffix.lower() != ".jpg"
            or not path.stem.isdecimal()):
        raise ValueError(f"unsafe image path: {value!r}")
    return path.as_posix()


def ambiguous_hashes(records):
    labels_by_hash = {}
    for record in records:
        labels_by_hash.setdefault(record["sha256"], set()).add(record["class_name"])
    return {
        digest: tuple(sorted(labels))
        for digest, labels in labels_by_hash.items()
        if len(labels) > 1
    }


def split_records(records, seed=42, validation_fraction=0.15, test_fraction=0.15):
    if validation_fraction <= 0 or test_fraction <= 0 or validation_fraction + test_fraction >= 1:
        raise ValueError("validation and test fractions must be positive and sum to less than one")

    by_hash = {}
    for record in records:
        label = record.get("class_name")
        digest = record.get("sha256")
        image_id = str(record.get("image_id", ""))
        if label not in CLASS_NAMES or not image_id or not isinstance(digest, str) or not digest:
            raise ValueError("each image record needs a known class, image ID, and content hash")
        previous = by_hash.get(digest)
        if previous and previous["class_name"] != label:
            raise ValueError(f"conflicting labels for identical image pixels: {digest}")
        by_hash.setdefault(digest, {"class_name": label, "image_id": image_id})

    by_class = {label: [] for label in CLASS_NAMES}
    for digest, record in by_hash.items():
        by_class[record["class_name"]].append(digest)

    rng = random.Random(seed)
    split_by_hash = {}
    for label, hashes in by_class.items():
        if len(hashes) < 3:
            raise ValueError(f"class {label!r} needs at least three unique images for separate splits")
        hashes.sort()
        rng.shuffle(hashes)
        test_count = max(1, round(len(hashes) * test_fraction))
        validation_count = max(1, round(len(hashes) * validation_fraction))
        while test_count + validation_count >= len(hashes):
            if test_count >= validation_count and test_count > 1:
                test_count -= 1
            else:
                validation_count -= 1
        for digest in hashes[:test_count]:
            split_by_hash[digest] = "test"
        for digest in hashes[test_count:test_count + validation_count]:
            split_by_hash[digest] = "validation"
        for digest in hashes[test_count + validation_count:]:
            split_by_hash[digest] = "train"

    return sorted(
        ({**record, "split": split_by_hash[record["sha256"]], "group_id": f"sha256:{record['sha256']}"}
         for record in records),
        key=lambda record: str(record["image_id"]),
    )
