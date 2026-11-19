import math
import unittest

from validate_accounting_kernel_v2 import (
    cumulative_recovery_percent,
    mass_balance_discrepancy_kg,
    mass_fraction_to_ppm,
    percent_to_fraction,
    ppm_to_mass_fraction,
    silver_grade_percent,
    silver_mass_kg,
    stage_recovery_percent,
    stream_mass_sum,
    validate_streams,
)


class AccountingValidationTests(unittest.TestCase):
    def test_ppm_to_mass_fraction_300(self):
        self.assertAlmostEqual(ppm_to_mass_fraction(300), 0.0003, places=15)

    def test_ppm_to_mass_fraction_630(self):
        self.assertAlmostEqual(ppm_to_mass_fraction(630), 0.00063, places=15)

    def test_mass_fraction_to_ppm(self):
        self.assertAlmostEqual(mass_fraction_to_ppm(0.0003), 300.0)

    def test_mass_conversion_rejects_fraction_over_one(self):
        with self.assertRaises(ValueError):
            mass_fraction_to_ppm(1.01)

    def test_percent_conversion(self):
        self.assertAlmostEqual(percent_to_fraction(100), 1.0)

    def test_silver_mass(self):
        self.assertAlmostEqual(silver_mass_kg(1.0, 300), 0.0003, places=15)

    def test_zero_ag_is_allowed_as_mass(self):
        self.assertEqual(silver_mass_kg(2.0, 0), 0.0)

    def test_zero_feed_is_allowed_as_mass(self):
        self.assertEqual(silver_mass_kg(0.0, 300), 0.0)

    def test_negative_feed_rejected(self):
        with self.assertRaises(ValueError):
            silver_mass_kg(-1.0, 300)

    def test_missing_ag_rejected(self):
        with self.assertRaises(ValueError):
            silver_mass_kg(1.0, None)

    def test_nonfinite_input_rejected(self):
        with self.assertRaises(ValueError):
            silver_mass_kg(1.0, math.nan)

    def test_zero_recovery(self):
        self.assertEqual(stage_recovery_percent(0.0, 1.0), 0.0)

    def test_complete_recovery(self):
        self.assertEqual(stage_recovery_percent(1.0, 1.0), 100.0)

    def test_stage_recovery_rejects_over_100(self):
        with self.assertRaises(ValueError):
            stage_recovery_percent(1.01, 1.0)

    def test_zero_ag_input_recovery_undefined(self):
        with self.assertRaises(ValueError):
            stage_recovery_percent(0.0, 0.0)

    def test_grade(self):
        self.assertEqual(silver_grade_percent(0.2, 1.0), 20.0)

    def test_grade_rejects_ag_exceeding_product_mass(self):
        with self.assertRaises(ValueError):
            silver_grade_percent(1.1, 1.0)

    def test_grade_rejects_zero_concentrate_mass(self):
        with self.assertRaises(ValueError):
            silver_grade_percent(0.0, 0.0)

    def test_stream_mass_sum(self):
        self.assertAlmostEqual(stream_mass_sum([0.1, 0.2, 0.3]), 0.6, places=15)

    def test_balance_reports_discrepancy(self):
        self.assertAlmostEqual(mass_balance_discrepancy_kg(1.0, [0.8], 0.1), 0.1)

    def test_balance_does_not_force_closure(self):
        self.assertNotEqual(mass_balance_discrepancy_kg(1.0, [0.8], 0.0), 0.0)

    def test_inconsistent_units_rejected(self):
        with self.assertRaises(ValueError):
            mass_balance_discrepancy_kg(1.0, [0.5], 0.0, unit="g")

    def test_cumulative_recovery(self):
        self.assertAlmostEqual(cumulative_recovery_percent([80.0, 50.0]), 40.0)

    def test_stream_ids_and_destination(self):
        rows = [{"stream_id":"tail","destination":"retained","mass_kg":0.9,"ag_mass_kg":0.01,"unit":"kg"}]
        self.assertEqual(validate_streams(rows), [])

    def test_duplicate_stream_id_rejected(self):
        rows = [
            {"stream_id":"x","destination":"a","mass_kg":1,"ag_mass_kg":0.1,"unit":"kg"},
            {"stream_id":"x","destination":"b","mass_kg":1,"ag_mass_kg":0.1,"unit":"kg"},
        ]
        with self.assertRaises(ValueError):
            validate_streams(rows)

    def test_missing_destination_rejected(self):
        with self.assertRaises(ValueError):
            validate_streams([{"stream_id":"x","destination":"","mass_kg":1,"ag_mass_kg":0,"unit":"kg"}])

    def test_silver_exceeding_stream_mass_rejected(self):
        with self.assertRaises(ValueError):
            validate_streams([{"stream_id":"x","destination":"out","mass_kg":0.5,"ag_mass_kg":0.6,"unit":"kg"}])

    def test_float_rounding(self):
        residual = mass_balance_discrepancy_kg(0.3, [0.1, 0.2], 0.0)
        self.assertAlmostEqual(residual, 0.0, places=15)


if __name__ == "__main__":
    unittest.main(verbosity=2)
