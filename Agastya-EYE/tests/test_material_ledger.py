import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from inference.ledger import Ledger
from inference.material_ledger import MaterialLedger


class MaterialLedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.panel_ledger = Ledger(root / "eye.sqlite3", root / "images")
        self.materials = MaterialLedger(root / "eye.sqlite3")
        self.panel = self.panel_ledger.save_inspection(
            image_bytes=b"test panel image", panel_id=None, external_ref=None, predictions=[],
            recommendation="HUMAN_REVIEW", final_disposition="PENDING_REVIEW",
            decision_source="triage_rules", reason="test", reviewer_note="",
            panel_technology="unknown", frame_width_mm=None, frame_height_mm=None,
            junction_box_location="unknown", electrical_test="not_tested", voltage=None,
            current=None, power=None,
        )["panel_id"]
        self.operator = {"operator_id": "operator-1", "instrument_id": "scale-1",
                         "calibration_ref": "cal-2026", "occurred_at": "2026-10-07T10:00:00+05:30"}

    def tearDown(self):
        self.temp.cleanup()

    def material(self, record_id, kind, mass, parents=None, **extra):
        return self.materials.create_material_record({
            "record_id": record_id, "record_type": kind, "parent_record_ids": parents or [],
            "panel_ids": [self.panel] if kind == "stream" else [],
            "material_label": extra.pop("material_label", "PV laminate"), "mass_g": mass,
            "mass_basis": "dry", **self.operator, **extra,
        })

    def assay(self, record_id, sample_id, analyte, value):
        return self.materials.create_assay({
            "record_id": record_id, "sample_id": sample_id, "analyte": analyte,
            "mass_fraction": value, "method": "validated lab assay", "laboratory": "lab-1",
            "instrument_id": "assay-1", "calibration_ref": "assay-cal-1", "operator_id": "analyst-1",
        })

    def create_run(self, record_id, route, feed, outputs, targets, **values):
        return self.materials.create_run({
            "record_id": record_id, "route_code": route, "feed_record_ids": [feed],
            "output_record_ids": outputs, "target_output_ids": targets, "outputs_complete": True,
            "operator_id": "operator-1", "instrument_id": "meter-1", "calibration_ref": "meter-cal-1",
            "method": "documented pilot method", **values,
        })

    def test_route_a_calculates_assay_backed_silver_and_mass_metrics(self):
        self.material("source", "stream", 1000)
        self.material("feed", "batch", 1000, ["source"])
        self.material("silver-fines", "fraction", 200, ["feed"], route_code="direct_comminution")
        self.material("residue", "fraction", 800, ["feed"], route_code="direct_comminution")
        self.material("feed-sample", "sample", 10, ["feed"])
        self.material("fines-sample", "sample", 10, ["silver-fines"])
        self.assay("feed-ag", "feed-sample", "ag", 0.001)
        self.assay("fines-ag", "fines-sample", "ag", 0.004)
        self.create_run("route-a", "direct_comminution", "feed", ["silver-fines", "residue"],
                        ["silver-fines"], energy_kwh=0.2, cost_inr=50, target_description="Ag-bearing fines")
        report = self.materials.get_run_report("route-a")
        self.assertEqual(report["mass_closure_percent"], 100)
        self.assertAlmostEqual(report["route_metrics"]["feed_ag_grade_percent"], 0.1)
        self.assertAlmostEqual(report["route_metrics"]["target_ag_grade_percent"], 0.4)
        self.assertAlmostEqual(report["route_metrics"]["ag_recovery_percent"], 80)
        self.assertAlmostEqual(report["route_metrics"]["enrichment_ratio"], 4)
        self.assertAlmostEqual(report["specific_energy_kwh_per_kg_feed"], 0.2)
        self.assertEqual(report["integrity"]["status"], "verified")

    def test_route_b_keeps_intact_cell_and_polymer_targets_distinct(self):
        self.material("source-b", "stream", 1000)
        self.material("delam-feed", "batch", 1000, ["source-b"])
        self.material("cell-product", "fraction", 300, ["delam-feed"], route_code="delamination")
        self.material("delam-residue", "fraction", 700, ["delam-feed"], route_code="delamination")
        self.material("delam-feed-sample", "sample", 10, ["delam-feed"])
        self.material("cell-sample", "sample", 10, ["cell-product"])
        self.assay("feed-cell", "delam-feed-sample", "intact_cell", 0.2)
        self.assay("product-cell", "cell-sample", "intact_cell", 0.5)
        self.assay("product-polymer", "cell-sample", "polymer", 0.1)
        self.create_run("route-b", "delamination", "delam-feed", ["cell-product", "delam-residue"],
                        ["cell-product"], target_description="intact-cell product")
        report = self.materials.get_run_report("route-b")
        self.assertAlmostEqual(report["route_metrics"]["intact_cell_recovery_percent"], 75)
        self.assertAlmostEqual(report["route_metrics"]["target_residual_polymer_grade_percent"], 10)
        self.assertNotIn("ag_recovery_percent", report["route_metrics"])

    def test_missing_assay_or_incomplete_outputs_withholds_metrics(self):
        self.material("source", "stream", 100)
        self.material("feed", "batch", 100, ["source"])
        self.material("product", "fraction", 40, ["feed"])
        self.create_run("partial-run", "direct_comminution", "feed", ["product"], ["product"],
                        outputs_complete=False)
        report = self.materials.get_run_report("partial-run")
        self.assertIsNone(report["mass_closure_percent"])
        self.assertIsNone(report["route_metrics"]["ag_recovery_percent"])
        self.assertTrue(any("not declared complete" in flag for flag in report["flags"]))

    def test_requires_lineage_and_assay_provenance(self):
        with self.assertRaisesRegex(ValueError, "Parent material record not found"):
            self.material("orphan", "batch", 10, ["missing"])
        self.material("source", "stream", 100)
        self.material("feed", "batch", 100, ["source"])
        with self.assertRaisesRegex(ValueError, "exactly one parent"):
            self.materials.create_material_record({
                "record_id": "bad-sample", "record_type": "sample", "parent_record_ids": [],
                "material_label": "sample", "mass_g": 1, **self.operator,
            })
        with self.assertRaisesRegex(ValueError, "sample_id must refer"):
            self.assay("orphan-assay", "missing", "ag", 0.1)

    def test_append_only_database_and_hash_chain(self):
        self.material("feed", "stream", 100)
        records = self.materials.list_records()
        self.assertEqual(self.materials.verify_integrity(records)["status"], "verified")
        with self.assertRaisesRegex(Exception, "append-only"):
            with closing(self.materials._connect()) as connection:
                connection.execute("DELETE FROM material_journal WHERE record_id='feed'")


if __name__ == "__main__":
    unittest.main()
