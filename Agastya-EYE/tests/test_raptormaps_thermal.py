import csv
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from inference.thermal_classifier import ThermalClassifier
from training.raptormaps_thermal import (
    CLASS_NAMES,
    ambiguous_hashes,
    normalize_class_name,
    safe_image_member,
    split_records,
)
from training.prepare_dataset import read_mappings


class RaptorMapsThermalTests(unittest.TestCase):
    def test_source_classes_are_preserved_without_claiming_burn_or_severity(self):
        self.assertEqual(len(CLASS_NAMES), 12)
        self.assertEqual(normalize_class_name("Cracking"), "cracking")
        self.assertEqual(normalize_class_name("No-Anomaly"), "no_anomaly")
        self.assertNotIn("burned", CLASS_NAMES)
        self.assertNotIn("broken", CLASS_NAMES)

    def test_image_member_must_be_a_flat_jpeg_under_images(self):
        self.assertEqual(safe_image_member("images/123.jpg"), "images/123.jpg")
        for member in ("../123.jpg", "images/../../escape.jpg", "C:/image.jpg", "images/sub/123.jpg"):
            with self.subTest(member=member), self.assertRaises(ValueError):
                safe_image_member(member)

    def test_split_is_deterministic_and_keeps_exact_duplicates_together(self):
        records = [
            {"image_id": f"{label}-{index}", "class_name": label, "sha256": f"{label}-{index}"}
            for label in CLASS_NAMES
            for index in range(10)
        ]
        records.append({"image_id": "duplicate", "class_name": CLASS_NAMES[0], "sha256": f"{CLASS_NAMES[0]}-0"})
        first = split_records(records, seed=17)
        second = split_records(records, seed=17)
        self.assertEqual(first, second)
        self.assertEqual(first[0]["split"], first[-1]["split"])
        for label in CLASS_NAMES:
            self.assertEqual(
                {row["split"] for row in first if row["class_name"] == label},
                {"train", "validation", "test"},
            )

    def test_conflicting_labels_for_same_pixels_are_rejected(self):
        records = [
            {"image_id": "a", "class_name": CLASS_NAMES[0], "sha256": "same"},
            {"image_id": "b", "class_name": CLASS_NAMES[1], "sha256": "same"},
        ]
        with self.assertRaisesRegex(ValueError, "conflicting labels"):
            split_records(records, seed=1)
        self.assertEqual(ambiguous_hashes(records), {"same": tuple(sorted(CLASS_NAMES[:2]))})

    def test_rgb_preparer_does_not_consume_thermal_mappings(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sources.csv"
            fields = (
                "source_id", "source_version", "source_url", "license",
                "original_class", "normalized_class", "task", "modality",
            )
            rows = [
                {
                    "source_id": "rgb_source", "source_version": "v1", "source_url": "https://example.org/rgb",
                    "license": "CC BY 4.0", "original_class": "clean", "normalized_class": "clean",
                    "task": "rgb_image_classification", "modality": "visible_rgb",
                },
                {
                    "source_id": "thermal_source", "source_version": "v1", "source_url": "https://example.org/ir",
                    "license": "MIT", "original_class": "Cracking", "normalized_class": "thermal_cracking",
                    "task": "thermal_module_classification", "modality": "thermal_infrared",
                },
            ]
            with path.open("w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            mappings = read_mappings(path)
            self.assertEqual(list(mappings), [("rgb_source", "clean")])

    def test_thermal_model_rejects_rgb_frames_and_pseudocolor_inputs(self):
        self.assertTrue(ThermalClassifier.supports_input(Image.new("L", (24, 40), 128)))
        self.assertFalse(ThermalClassifier.supports_input(Image.new("RGB", (24, 40), "red")))
        self.assertFalse(ThermalClassifier.supports_input(Image.new("L", (640, 400), 128)))


if __name__ == "__main__":
    unittest.main()
