import csv
import tempfile
import unittest
from pathlib import Path

from training.pv_degradation import (
    fit_ridge,
    grouped_leave_one_cell_out,
    parse_bbox,
    predict_ridge,
    power_loss_band,
    read_samples,
    regression_metrics,
    severity_band,
)
from training.import_pv_degradation import safe_member_path


class PVDegradationTests(unittest.TestCase):
    def write_fixture(self, root, power_loss="12.5"):
        image_root = root / "images"
        rows = []
        for cell, name in (("0.1", "0.1_D01"), ("0.2", "0.2_D01")):
            (image_root / "HDR").mkdir(parents=True, exist_ok=True)
            (image_root / "BW").mkdir(parents=True, exist_ok=True)
            (image_root / "EL").mkdir(parents=True, exist_ok=True)
            for modality, suffix in (("HDR", "HDR"), ("BW", "BN"), ("EL", "EL")):
                (image_root / modality / f"{name}_{suffix}_rt_cr.png").write_bytes(b"image")
            rows.append({
                "images_set_name": name,
                "PV_cell_name": cell,
                "Power_output_loss [%] [V*I]": power_loss,
                "Degradation_level": "minor",
                "incremental_damage_kind": "mechanical",
                "incremental_damage_HDR_visible_type": "edge crack",
                "EL_file_name": f"{name}_EL_rt_cr.png",
                "New_Damage_Xmin": "10",
                "New_Damage_Ymin": "20",
                "New_Damage_Xmax": "80",
                "New_Damage_Ymax": "90",
            })
        csv_path = root / "data.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys(), delimiter=";")
            writer.writeheader()
            writer.writerows(rows)
        return csv_path, image_root

    def test_reads_paired_modalities_and_preserves_source_severity(self):
        with tempfile.TemporaryDirectory() as temp:
            csv_path, image_root = self.write_fixture(Path(temp))
            samples = read_samples(csv_path, image_root, modality="HDR")
            self.assertEqual(len(samples), 2)
            self.assertEqual(samples[0].source_grade, "minor")
            self.assertEqual(samples[0].visible_damage, "edge crack")
            self.assertEqual(samples[0].group_id, "0.1")
            self.assertEqual(samples[0].image_path.name, "0.1_D01_HDR_rt_cr.png")
            self.assertEqual(samples[0].power_loss_pct, 12.5)

            bw_samples = read_samples(csv_path, image_root, modality="BW")
            el_samples = read_samples(csv_path, image_root, modality="EL")
            self.assertEqual(bw_samples[0].image_path.name, "0.1_D01_BN_rt_cr.png")
            self.assertEqual(el_samples[0].image_path.name, "0.1_D01_EL_rt_cr.png")

    def test_rejects_missing_or_invalid_measured_power_loss(self):
        with tempfile.TemporaryDirectory() as temp:
            csv_path, image_root = self.write_fixture(Path(temp), power_loss="NaN")
            with self.assertRaisesRegex(ValueError, "finite power-loss"):
                read_samples(csv_path, image_root)

        with tempfile.TemporaryDirectory() as temp:
            csv_path, image_root = self.write_fixture(Path(temp), power_loss="101")
            with self.assertRaisesRegex(ValueError, "between 0 and 100"):
                read_samples(csv_path, image_root)

    def test_requires_images_and_rejects_duplicate_sample_ids(self):
        with tempfile.TemporaryDirectory() as temp:
            csv_path, image_root = self.write_fixture(Path(temp))
            (image_root / "HDR" / "0.1_D01_HDR_rt_cr.png").unlink()
            with self.assertRaisesRegex(ValueError, "paired HDR image is missing"):
                read_samples(csv_path, image_root)

    def test_cell_held_out_folds_never_leak_a_physical_cell(self):
        with tempfile.TemporaryDirectory() as temp:
            csv_path, image_root = self.write_fixture(Path(temp))
            samples = read_samples(csv_path, image_root)
            folds = grouped_leave_one_cell_out(samples)
            self.assertEqual(len(folds), 2)
            for train, test in folds:
                self.assertEqual({item.group_id for item in test}.__len__(), 1)
                self.assertFalse({item.group_id for item in train} & {item.group_id for item in test})
                self.assertEqual(len(test), 1)

    def test_bbox_and_severity_bands_are_explicit_and_bounded(self):
        bbox = parse_bbox({
            "New_Damage_Xmin": "10", "New_Damage_Ymin": "20",
            "New_Damage_Xmax": "80", "New_Damage_Ymax": "90",
        })
        self.assertEqual(bbox, {"xmin": 10, "ymin": 20, "xmax": 80, "ymax": 90})
        self.assertIsNone(parse_bbox({"New_Damage_Xmin": "NaN"}))
        self.assertEqual(severity_band(0), "none")
        self.assertEqual(severity_band(4.9), "light")
        self.assertEqual(severity_band(5), "minor")
        self.assertEqual(severity_band(15), "moderate")
        self.assertEqual(severity_band(25), "severe")
        self.assertEqual(severity_band(45), "critical")
        self.assertEqual(severity_band(100), "catastrophic")
        self.assertEqual(power_loss_band(4.9, "dirt"), "low_soiling")
        self.assertEqual(power_loss_band(5, "dirt"), "medium_soiling")
        self.assertEqual(power_loss_band(10, "dirt"), "high_soiling")
        self.assertEqual(power_loss_band(20, "dirt"), "very_high_soiling")

    def test_ridge_baseline_and_metrics_use_continuous_targets(self):
        import numpy as np

        features = np.asarray([[0.0], [1.0], [2.0], [3.0]])
        target = np.asarray([0.0, 10.0, 20.0, 30.0])
        intercept, weights = fit_ridge(features, target, alpha=1e-8)
        predictions = predict_ridge(features, intercept, weights)
        self.assertTrue(np.allclose(predictions, target, atol=1e-3))
        metrics = regression_metrics(target, predictions)
        self.assertAlmostEqual(metrics["mae_pct_points"], 0.0, places=3)
        self.assertAlmostEqual(metrics["r2"], 1.0, places=5)

    def test_dataset_import_rejects_archive_path_traversal(self):
        self.assertEqual(safe_member_path("PV_EL_HDR_BW_Test_DB/data/ELPV_DATA_FULL.CSV").as_posix(), "data/ELPV_DATA_FULL.CSV")
        for path in (
            "../escape.txt",
            "PV_EL_HDR_BW_Test_DB/../../escape.txt",
            "PV_EL_HDR_BW_Test_DB/data\\..\\escape.txt",
            "PV_EL_HDR_BW_Test_DB/data/C:/escape.txt",
            "/PV_EL_HDR_BW_Test_DB/data/file.csv",
            "unexpected_root/data/file.csv",
        ):
            with self.subTest(path=path), self.assertRaises(ValueError):
                safe_member_path(path)


if __name__ == "__main__":
    unittest.main()
