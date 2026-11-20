from datetime import datetime, timedelta, timezone
import tempfile
import unittest
import hashlib
from pathlib import Path

from hardware.arduino_config import ArduinoConfig
from hardware.arduino_controller import (
    ArduinoServoController,
    HardwareProtocolError,
    HardwareUnavailableError,
)
from hardware.approval import (
    DuplicateApprovalError,
    HardwareApprovalService,
    HardwareApprovalStore,
    IneligibleApprovalError,
    inspection_image_is_intact,
    release_eligibility,
)
from tests.test_arduino_controller import FakeSerial, enabled_config


def approved_record(*, created_at=None):
    return {
        "id": 31,
        "panel_id": "PV-000031",
        "created_at": (created_at or datetime.now(timezone.utc)).isoformat(),
        "image_path": "images/PV-000031/inspection.jpg",
        "image_sha256": "a" * 64,
        "camera_modality": "visible_rgb",
        "capture_view": "front",
        "panel_technology": "c_si",
        "recommended_route": "SECOND_LIFE_REVIEW",
        "final_route": "SECOND_LIFE_REVIEW",
        "final_disposition": "REUSED",
        "confirmed_visual_label": "clean",
        "reviewer_note": "Qualified operator reviewed the panel and approved second-life use.",
        "electrical_test": "pass",
        "voltage": 32.1,
        "current": 4.5,
        "electrical_method": "I-V sweep",
        "electrical_instrument": "PV tester 01",
        "electrical_operator": "operator-1",
        "predictions": [
            {"label": "clean", "confidence": 0.91},
            {"label": "dust", "confidence": 0.04},
        ],
    }


class HardwareApprovalTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        root = Path(self.tempdir.name)
        self.store = HardwareApprovalStore(root / "hardware.sqlite3")
        self.device = FakeSerial()
        self.controller = ArduinoServoController(
            enabled_config(), serial_factory=lambda *args, **kwargs: self.device
        )
        self.service = HardwareApprovalService(self.controller, self.store, max_age_seconds=300)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_only_fresh_explicitly_approved_clean_electrically_passed_records_are_eligible(self):
        record = approved_record()
        eligible = release_eligibility(record, backend_ready=True, image_available=True)
        self.assertTrue(eligible["eligible"])

        cases = [
            ({"final_disposition": "PENDING_REVIEW"}, "final reuse approval"),
            ({"recommended_route": "HUMAN_REVIEW"}, "approved second-life route"),
            ({"electrical_test": "fail"}, "documented electrical pass"),
            ({"current": None}, "voltage and current readings"),
            ({"voltage": float("nan")}, "readings are invalid"),
            ({"camera_modality": "thermal_infrared"}, "front-view RGB"),
            ({"confirmed_visual_label": "dust"}, "clean result"),
            ({"predictions": [{"label": "clean", "confidence": 0.6}]}, "uncertain"),
        ]
        for values, message in cases:
            with self.subTest(values=values):
                candidate = {**record, **values}
                result = release_eligibility(candidate, backend_ready=True, image_available=True)
                self.assertFalse(result["eligible"])
                self.assertIn(message, result["reason"])

        stale = approved_record(created_at=datetime.now(timezone.utc) - timedelta(minutes=10))
        self.assertFalse(release_eligibility(stale, backend_ready=True, image_available=True)["eligible"])
        self.assertFalse(release_eligibility(record, backend_ready=False, image_available=True)["eligible"])
        self.assertFalse(release_eligibility(record, backend_ready=True, image_available=False)["eligible"])

    def test_release_image_must_remain_inside_image_root_and_match_recorded_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            project_root = Path(directory)
            image_root = project_root / "images"
            image_path = image_root / "PV-000031" / "inspection.jpg"
            image_path.parent.mkdir(parents=True)
            image_path.write_bytes(b"original inspected image")
            record = {
                "image_path": "images/PV-000031/inspection.jpg",
                "image_sha256": hashlib.sha256(image_path.read_bytes()).hexdigest(),
            }

            self.assertTrue(inspection_image_is_intact(
                record, project_root=project_root, image_root=image_root
            ))
            image_path.write_bytes(b"changed image")
            self.assertFalse(inspection_image_is_intact(
                record, project_root=project_root, image_root=image_root
            ))
            self.assertFalse(inspection_image_is_intact(
                {**record, "image_path": "images/../../outside.jpg"},
                project_root=project_root,
                image_root=image_root,
            ))

    def test_release_requires_operator_confirmation_and_is_single_use(self):
        record = approved_record()
        with self.assertRaises(IneligibleApprovalError):
            self.service.release(
                record,
                operator_id="operator-2",
                panel_confirmation="WRONG-PANEL",
                backend_ready=True,
                image_available=True,
            )
        self.assertEqual(self.device.writes, [])

        result = self.service.release(
            record,
            operator_id="operator-2",
            panel_confirmation="PV-000031",
            backend_ready=True,
            image_available=True,
        )
        self.assertEqual(result["approval"]["state"], "closed_commanded")
        self.assertFalse(result["physical_position_verified"])
        with self.assertRaises(DuplicateApprovalError):
            self.service.release(
                record,
                operator_id="operator-2",
                panel_confirmation="PV-000031",
                backend_ready=True,
                image_available=True,
            )
        self.assertEqual(sum(line.startswith("RELEASE ") for line in self.device.writes), 1)

    def test_failed_ack_is_recorded_as_uncertain_and_cannot_be_retried(self):
        self.device.answer_release = False
        record = approved_record()
        with self.assertRaises(HardwareProtocolError):
            self.service.release(
                record,
                operator_id="operator-2",
                panel_confirmation="PV-000031",
                backend_ready=True,
                image_available=True,
            )
        saved = self.store.get_by_inspection(record["id"])
        self.assertEqual(saved["state"], "uncertain")
        with self.assertRaises(DuplicateApprovalError):
            self.service.release(
                record,
                operator_id="operator-2",
                panel_confirmation="PV-000031",
                backend_ready=True,
                image_available=True,
            )
        self.assertEqual(sum(line.startswith("RELEASE ") for line in self.device.writes), 1)

    def test_disabled_hardware_never_opens_a_port(self):
        from unittest.mock import Mock

        factory = Mock()
        controller = ArduinoServoController(ArduinoConfig(), serial_factory=factory)
        service = HardwareApprovalService(controller, self.store)
        with self.assertRaises(HardwareUnavailableError):
            service.release(
                approved_record(),
                operator_id="operator-2",
                panel_confirmation="PV-000031",
                backend_ready=True,
                image_available=True,
            )
        factory.assert_not_called()

    def test_approval_store_is_healthy_and_duplicate_inspections_are_rejected(self):
        record = approved_record()
        self.store.create_request("1" * 32, record["id"], record["panel_id"], "operator-2", 3000)
        self.assertTrue(self.store.health_check()["healthy"])
        with self.assertRaises(DuplicateApprovalError):
            self.store.create_request("2" * 32, record["id"], record["panel_id"], "operator-2", 3000)


if __name__ == "__main__":
    unittest.main()
