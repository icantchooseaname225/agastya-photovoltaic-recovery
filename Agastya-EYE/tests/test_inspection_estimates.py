import unittest
import tempfile
from pathlib import Path

from inference.estimation import (
    ResearchPowerLossEstimator,
    calculate_panel_estimates,
    supported_power_loss_model,
)
from inference.ledger import Ledger


class InspectionEstimateTests(unittest.TestCase):
    def test_calculates_frame_area_and_power_from_voltage_and_current(self):
        result = calculate_panel_estimates(
            width_mm=1000,
            height_mm=1700,
            voltage=36,
            current=8,
            power=None,
            rated_power_w=320,
        )
        self.assertEqual(result["panel_area_m2"], 1.7)
        self.assertEqual(result["power_w"], 288.0)
        self.assertEqual(result["power_source"], "voltage_current_product")
        self.assertEqual(result["nameplate_output_pct"], 90.0)
        self.assertEqual(result["below_nameplate_pct"], 10.0)

    def test_recorded_power_takes_precedence_and_missing_inputs_stay_unknown(self):
        result = calculate_panel_estimates(
            width_mm=None,
            height_mm=1700,
            voltage=36,
            current=8,
            power=290,
            rated_power_w=None,
        )
        self.assertIsNone(result["panel_area_m2"])
        self.assertEqual(result["power_w"], 290.0)
        self.assertEqual(result["power_source"], "recorded")
        self.assertIsNone(result["nameplate_output_pct"])

    def test_only_matching_nir_and_el_modalities_have_research_models(self):
        self.assertEqual(supported_power_loss_model("near_infrared"), "BW")
        self.assertEqual(supported_power_loss_model("electroluminescence"), "EL")
        for modality in ("visible_rgb", "visible_rgb_closeup", "thermal_infrared", "hdr"):
            with self.subTest(modality=modality):
                self.assertIsNone(supported_power_loss_model(modality))

    def test_rgb_estimate_is_explicitly_unavailable_without_loading_ai_weights(self):
        result = ResearchPowerLossEstimator().estimate(None, "visible_rgb")
        self.assertEqual(result["status"], "not_available")
        self.assertIsNone(result["estimated_power_loss_pct"])
        self.assertFalse(result["sorting_use"])

    def test_matching_modality_returns_separate_non_sorting_benchmark_estimate(self):
        import numpy as np

        estimator = ResearchPowerLossEstimator()
        estimator._load_artifact = lambda modality: (
            {"intercept": 15.0, "coefficients": np.zeros(1280)},
            {"training_samples": 84, "training_cells": ["cell-a", "cell-b"], "source_doi": "test", "source_license": "CC BY 4.0"},
            {"overall_cell_held_out_metrics": {"mae_pct_points": 13.8}},
        )
        estimator._extract_features = lambda image: np.zeros(1280)
        result = estimator.estimate(object(), "near_infrared")
        self.assertEqual(result["status"], "research_only")
        self.assertEqual(result["estimated_power_loss_pct"], 15.0)
        self.assertEqual(result["training_samples"], 84)
        self.assertFalse(result["sorting_use"])

    def test_nameplate_and_research_estimates_are_hash_protected_in_passport(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            ledger = Ledger(root / "eye.sqlite3", root / "images")
            record = ledger.save_inspection(
                image_bytes=b"inspection image",
                panel_id=None,
                external_ref=None,
                predictions=[],
                recommendation="HUMAN_REVIEW",
                final_disposition="PENDING_REVIEW",
                decision_source="triage_rules",
                reason="Manual check required",
                reviewer_note="",
                panel_technology="unknown",
                frame_width_mm=1000,
                frame_height_mm=1700,
                junction_box_location="unknown",
                electrical_test="not_tested",
                voltage=36,
                current=8,
                power=None,
                rated_power_w=320,
                power_loss_estimate={"status": "not_available", "sorting_use": False},
                capture_view="rear_nameplate",
            )
            self.assertEqual(record["hash_version"], "1.5")
            self.assertEqual(record["capture_view"], "rear_nameplate")
            self.assertEqual(record["inspection_estimates"]["power_w"], 288.0)
            passport = ledger.get_passport(record["panel_id"])
            self.assertEqual(passport["schema_version"], "1.6")
            self.assertEqual(passport["inspections"][0]["capture_view"], "rear_nameplate")
            self.assertEqual(passport["integrity"]["status"], "verified")


if __name__ == "__main__":
    unittest.main()
