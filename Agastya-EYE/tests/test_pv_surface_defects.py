import unittest

from training.pv_surface_defects import (
    CLASS_NAMES,
    deduplicate_exact_images,
    labels_to_multihot,
    parse_voc_annotation,
    select_f1_thresholds,
    safe_archive_member,
    split_grouped_records,
)


class PVSurfaceDefectTests(unittest.TestCase):
    def test_voc_boxes_are_validated_and_converted_to_zero_based_xyxy(self):
        annotation = b"""<annotation>
          <filename>panel.jpg</filename><size><width>20</width><height>10</height></size>
          <object><name>broken</name><bndbox><xmin>1</xmin><ymin>2</ymin><xmax>8</xmax><ymax>9</ymax></bndbox></object>
        </annotation>"""
        parsed = parse_voc_annotation(annotation)
        self.assertEqual(parsed["filename"], "panel.jpg")
        self.assertEqual(parsed["objects"][0]["label"], "broken")
        self.assertEqual(parsed["objects"][0]["bbox_xyxy"], [0, 1, 8, 9])

    def test_voc_rejects_unknown_labels_and_out_of_bounds_boxes(self):
        unknown = b"""<annotation><filename>x.jpg</filename><size><width>10</width><height>10</height></size>
          <object><name>burned</name><bndbox><xmin>1</xmin><ymin>1</ymin><xmax>2</xmax><ymax>2</ymax></bndbox></object></annotation>"""
        outside = b"""<annotation><filename>x.jpg</filename><size><width>10</width><height>10</height></size>
          <object><name>broken</name><bndbox><xmin>1</xmin><ymin>1</ymin><xmax>11</xmax><ymax>2</ymax></bndbox></object></annotation>"""
        with self.assertRaisesRegex(ValueError, "unsupported VOC class"):
            parse_voc_annotation(unknown)
        with self.assertRaisesRegex(ValueError, "outside image bounds"):
            parse_voc_annotation(outside)

    def test_group_split_is_deterministic_duplicate_safe_and_covers_each_class(self):
        records = []
        for index in range(60):
            labels = [CLASS_NAMES[index % len(CLASS_NAMES)]]
            if index % 3 == 0:
                labels.append("broken")
            records.append({"image_id": str(index), "sha256": f"sha-{index}", "labels": labels})
        records.append({"image_id": "duplicate", "sha256": "sha-0", "labels": ["hot_spot"]})
        first = split_grouped_records(records, seed=19)
        second = split_grouped_records(records, seed=19)
        self.assertEqual(first, second)
        self.assertEqual(first[0]["split"], first[-1]["split"])
        for label in CLASS_NAMES:
            self.assertEqual(
                {row["split"] for row in first if label in row["labels"]},
                {"train", "validation", "test"},
            )

    def test_duplicate_pixels_with_disagreeing_boxes_are_quarantined(self):
        rows = [
            {"image_id": "a", "sha256": "same", "objects": [{"label": "broken", "bbox_xyxy": [1, 1, 5, 5]}]},
            {"image_id": "b", "sha256": "same", "objects": [{"label": "broken", "bbox_xyxy": [1, 1, 6, 5]}]},
            {"image_id": "c", "sha256": "other", "objects": []},
        ]
        kept, conflicts = deduplicate_exact_images(rows)
        self.assertEqual([row["image_id"] for row in kept], ["c"])
        self.assertEqual(conflicts[0]["sha256"], "same")
        self.assertEqual(conflicts[0]["image_ids"], ["a", "b"])

    def test_archive_members_cannot_escape_source_directories(self):
        self.assertEqual(safe_archive_member("repo/JPEGImages/a.jpg", "repo", "JPEGImages"), "a.jpg")
        for member in ("../escape.jpg", "repo/JPEGImages/../escape.jpg", "repo/Annotations/a.xml"):
            with self.subTest(member=member), self.assertRaises(ValueError):
                safe_archive_member(member, "repo", "JPEGImages")

    def test_source_box_labels_become_multi_hot_without_inventing_burn_labels(self):
        vector = labels_to_multihot(["broken", "scratch", "broken"])
        self.assertEqual(sum(vector), 2)
        self.assertEqual(vector[CLASS_NAMES.index("broken")], 1)
        self.assertEqual(vector[CLASS_NAMES.index("scratch")], 1)
        self.assertNotIn("burned", CLASS_NAMES)

    def test_dataset_modality_remains_unspecified_and_no_burn_label_is_invented(self):
        from training.import_pv_multi_defect import import_report_contract

        contract = import_report_contract()
        self.assertEqual(contract["modality"], "grayscale_camera_crop_unspecified")
        self.assertIn("does not identify the sensor spectral band", contract["image_format_note"])
        self.assertIn("not calibrated temperature", contract["image_format_note"])
        self.assertNotIn("burned", contract["class_names"])

    def test_thresholds_are_selected_from_validation_probabilities(self):
        labels = [[1, 0], [1, 0], [0, 1], [0, 1]]
        probabilities = [[0.9, 0.2], [0.7, 0.3], [0.4, 0.8], [0.2, 0.6]]
        self.assertEqual(select_f1_thresholds(probabilities, labels), [0.7, 0.6])


if __name__ == "__main__":
    unittest.main()
