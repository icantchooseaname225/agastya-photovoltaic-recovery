"""Exercise the device and operator APIs against an isolated temporary ledger."""

import base64
import hashlib
import json
import os
import secrets
import sqlite3
import sys
import tempfile
import threading
import uuid
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

from PIL import Image, ImageChops, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app as eye
from inference.ledger import HASH_FIELDS, Ledger, canonical_json
from inference.triage import recommend_route


class SimulatorClassifier:
    def __init__(self):
        self.predict_calls = 0

    def status(self):
        return {"ready": True, "message": "PC simulation stub; no panel inference"}

    def predict(self, image):
        self.predict_calls += 1
        return [{"label": "other", "confidence": 0.5}]


class SimulatorThermalClassifier:
    def __init__(self):
        self.predict_calls = 0

    def status(self):
        return {"ready": True, "message": "Synthetic thermal model stub; no panel inference"}

    def supports_input(self, image):
        width, height = image.size
        if abs(width / max(height, 1) - (24 / 40)) > 0.12:
            return False
        pixels = image.convert("RGB").resize((24, 40))
        red, green, blue = pixels.split()
        return (ImageChops.difference(red, green).getbbox() is None
                and ImageChops.difference(green, blue).getbbox() is None)

    def predict(self, image):
        self.predict_calls += 1
        return [{"label": "cracking", "confidence": 0.88}, {"label": "no_anomaly", "confidence": 0.04}]


class SimulatorVisibleCropClassifier:
    def __init__(self):
        self.predict_calls = 0

    def status(self):
            return {"ready": True, "message": "Visible close-up research screen", "used_for_routing": False}

    def predict(self, image):
        self.predict_calls += 1
        if min(image.size) < 512 or abs(image.width / max(image.height, 1) - 1.0) > 0.08:
            return []
        pixels = image.convert("RGB").resize((24, 24))
        red, green, blue = pixels.split()
        if (ImageChops.difference(red, green).getbbox() is not None
                or ImageChops.difference(green, blue).getbbox() is not None):
            return []
        return [{
            "label": "broken", "confidence": 0.99, "model": "pv_multi_defect_visible_crop_research",
            "advisory_only": True,
        }]


class SimulatorPowerLossEstimator:
    def estimate(self, image, camera_modality):
        return {
            "status": "not_available",
            "estimated_power_loss_pct": None,
            "reason": "Research estimator is stubbed for PC simulation.",
            "sorting_use": False,
        }


def make_test_image():
    image = Image.new("RGB", (640, 400), "#25343a")
    draw = ImageDraw.Draw(image)
    draw.rectangle((28, 28, 612, 372), outline="#d1dfd7", width=3)
    draw.text((72, 132), "AGASTYA-EYE PC SIMULATOR", fill="white")
    draw.text((72, 184), "SYNTHETIC TEST CARD - NOT A PANEL", fill="#f4c76b")
    output = BytesIO()
    image.save(output, format="JPEG", quality=88)
    return output.getvalue()


def make_raptormaps_test_image():
    output = BytesIO()
    Image.new("L", (24, 40), 128).save(output, format="JPEG", quality=95)
    return output.getvalue()


def make_visible_crop_test_image():
    output = BytesIO()
    Image.new("L", (600, 600), 128).save(output, format="JPEG", quality=95)
    return output.getvalue()


def post(url, body, headers):
    request = Request(url, data=body, headers=headers, method="POST")
    with urlopen(request, timeout=60) as response:
        return response.status, json.loads(response.read())


def mark_legacy_hash(ledger, record):
    connection = sqlite3.connect(ledger.database_path)
    try:
        connection.row_factory = sqlite3.Row
        stored = connection.execute(
            """SELECT i.*, p.panel_id FROM inspections i
               JOIN panels p ON p.id = i.panel_row_id WHERE i.id = ?""",
            (record["id"],),
        ).fetchone()
        digest = hashlib.sha256(
            canonical_json({key: stored[key] for key in HASH_FIELDS}).encode("utf-8")
        ).hexdigest()
        connection.execute("DROP TRIGGER inspections_no_update")
        connection.execute(
            "UPDATE inspections SET hash_version = '1.2', record_hash = ? WHERE id = ?",
            (digest, record["id"]),
        )
        connection.execute(
            """CREATE TRIGGER inspections_no_update BEFORE UPDATE ON inspections BEGIN
                   SELECT RAISE(ABORT, 'inspection records are append-only');
               END"""
        )
        connection.commit()
    finally:
        connection.close()


def main():
    token = secrets.token_urlsafe(32)
    previous_token = os.environ.get("AGASTYA_DEVICE_TOKEN")
    previous_ledger = eye.ledger
    previous_classifier = eye.classifier
    previous_thermal_classifier = eye.thermal_classifier
    previous_visible_crop_classifier = eye.visible_crop_classifier
    previous_power_loss_estimator = eye.power_loss_estimator
    server = None
    thread = None

    try:
        os.environ["AGASTYA_DEVICE_TOKEN"] = token
        with tempfile.TemporaryDirectory(prefix="agastya-eye-smoke-") as temp_dir:
            temp_path = Path(temp_dir)
            eye.ledger = Ledger(temp_path / "database" / "eye.sqlite3", temp_path / "images")
            eye.classifier = SimulatorClassifier()
            eye.thermal_classifier = SimulatorThermalClassifier()
            eye.visible_crop_classifier = SimulatorVisibleCropClassifier()
            eye.power_loss_estimator = SimulatorPowerLossEstimator()
            server = eye.ThreadingHTTPServer(("127.0.0.1", 0), eye.EyeHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            base_url = f"http://127.0.0.1:{server.server_port}"

            with urlopen(base_url + "/api/v1/health", timeout=30) as response:
                health = json.loads(response.read())
            if health["status"] != "ready" or not health["device_upload_enabled"]:
                raise RuntimeError("Versioned device API health check failed")

            image_bytes = make_test_image()
            request_id = uuid.uuid4().hex
            reference = f"PC-SIM-{uuid.uuid4().hex[:12]}"
            captured_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            headers = {
                "Content-Type": "image/jpeg",
                "Authorization": f"Bearer {token}",
                "X-Device-ID": "pc-simulator",
                "X-Request-ID": request_id,
                "X-Panel-Ref": reference,
                "X-Captured-At": captured_at,
                "X-Camera-Modality": "visible_rgb",
                "X-Camera-Sensor-ID": "pc-simulator-rgb-01",
                "X-Capture-Group-ID": "pc-simulator-pair-01",
                "X-Capture-View": "front",
                "X-Electrical-Test": "not_tested",
            }
            status, record = post(base_url + "/api/v1/inspections", image_bytes, headers)
            retry_status, retry_record = post(base_url + "/api/v1/inspections", image_bytes, headers)
            if status != 201 or retry_status != 201 or retry_record["id"] != record["id"]:
                raise RuntimeError("Device capture or idempotent retry check failed")
            if (record["device_id"] != "pc-simulator"
                    or record["electrical_test"] != "not_tested"
                    or record["panel_technology"] != "unknown"
                    or record["camera_modality"] != "visible_rgb"
                    or record["capture_view"] != "front"
                    or record["camera_sensor_id"] != "pc-simulator-rgb-01"
                    or record["capture_group_id"] != "pc-simulator-pair-01"
                    or any(record[key] is not None for key in ("voltage", "current", "power"))):
                raise RuntimeError("The device record did not preserve the not-tested electrical state")
            with urlopen(base_url + record["image_url"], timeout=5) as response:
                served_image = response.read()
                if (response.status != 200
                        or response.headers.get_content_type() != "image/jpeg"
                        or hashlib.sha256(served_image).hexdigest() != record["image_sha256"]):
                    raise RuntimeError("Saved inspection image URL did not return its recorded JPEG")
            mark_legacy_hash(eye.ledger, record)

            infrared_headers = {
                **headers,
                "X-Request-ID": uuid.uuid4().hex,
                "X-Camera-Modality": "near_infrared",
                "X-Camera-Sensor-ID": "pc-simulator-nir-01",
                "X-Capture-Group-ID": "pc-simulator-pair-01",
            }
            rgb_prediction_calls = eye.classifier.predict_calls
            _, infrared_record = post(base_url + "/api/v1/inspections", image_bytes, infrared_headers)
            if (infrared_record["camera_modality"] != "near_infrared"
                    or infrared_record["capture_group_id"] != record["capture_group_id"]
                    or infrared_record["camera_sensor_id"] != "pc-simulator-nir-01"
                    or infrared_record["predictions"]
                    or infrared_record["recommended_route"] != "HUMAN_REVIEW"
                    or eye.classifier.predict_calls != rgb_prediction_calls
                    or "near-infrared" not in infrared_record["route_reason"].lower()):
                raise RuntimeError("Near-infrared imagery was not safely archived without RGB inference")

            thermal_headers = {
                **headers,
                "X-Request-ID": uuid.uuid4().hex,
                "X-Camera-Modality": "thermal_infrared",
                "X-Camera-Sensor-ID": "pc-simulator-thermal-01",
            }
            _, thermal_record = post(
                base_url + "/api/v1/inspections", make_raptormaps_test_image(), thermal_headers
            )
            if (thermal_record["camera_modality"] != "thermal_infrared"
                    or thermal_record["predictions"][0]["label"] != "cracking"
                    or thermal_record["recommended_route"] != "SAFETY_HOLD"
                    or eye.thermal_classifier.predict_calls != 1
                    or eye.visible_crop_classifier.predict_calls != 0
                    or eye.classifier.predict_calls != rgb_prediction_calls
                    or "human review is required" not in thermal_record["route_reason"].lower()):
                raise RuntimeError("Thermal inference was not kept separate and safely routed")

            closeup_headers = {
                **headers,
                "X-Request-ID": uuid.uuid4().hex,
                "X-Camera-Modality": "visible_rgb_closeup",
                "X-Camera-Sensor-ID": "pc-simulator-visible-closeup-01",
            }
            _, closeup_record = post(
                base_url + "/api/v1/inspections",
                make_visible_crop_test_image(),
                closeup_headers,
            )
            if (closeup_record["camera_modality"] != "visible_rgb_closeup"
                    or closeup_record["predictions"][0]["label"] != "broken"
                    or not closeup_record["predictions"][0]["advisory_only"]
                    or closeup_record["recommended_route"] != "HUMAN_REVIEW"
                    or closeup_record["sort_recommendation"]["destination"] != "MANUAL_REVIEW"
                    or closeup_record["sort_recommendation"]["actuator_commanded"]
                    or "not used to calculate this route" not in closeup_record["route_reason"].lower()
                    or eye.visible_crop_classifier.predict_calls != 1):
                raise RuntimeError("Visible crop hints were not kept advisory and separate from routing")

            rear_headers = {
                **headers,
                "X-Request-ID": uuid.uuid4().hex,
                "X-Capture-View": "rear_nameplate",
                "X-Panel-Technology": "c_si",
                "X-Rated-Power-W": "3",
            }
            rgb_calls_before_rear = eye.classifier.predict_calls
            _, rear_record = post(base_url + "/api/v1/inspections", image_bytes, rear_headers)
            if (rear_record["capture_view"] != "rear_nameplate"
                    or rear_record["panel_id"] != record["panel_id"]
                    or rear_record["rated_power_w"] != 3
                    or rear_record["predictions"]
                    or eye.classifier.predict_calls != rgb_calls_before_rear):
                raise RuntimeError("Rear nameplate capture did not append to its panel with the view label")

            try:
                post(base_url + "/api/v1/inspections", image_bytes, {
                    **headers,
                    "X-Request-ID": uuid.uuid4().hex,
                    "X-Camera-Modality": "thermal_blob",
                })
            except HTTPError as error:
                error_body = json.loads(error.read())
                if error.code != 400 or "camera modality" not in error_body.get("error", "").lower():
                    raise RuntimeError("Unsupported camera modality was not rejected clearly") from error
            else:
                raise RuntimeError("The device API accepted an unknown camera modality")

            try:
                post(base_url + "/api/v1/inspections", image_bytes, {
                    **headers,
                    "X-Request-ID": uuid.uuid4().hex,
                    "X-Capture-View": "underside-of-mars",
                })
            except HTTPError as error:
                error_body = json.loads(error.read())
                if error.code != 400 or "capture view" not in error_body.get("error", "").lower():
                    raise RuntimeError("Unsupported capture view was not rejected clearly") from error
            else:
                raise RuntimeError("The device API accepted an unknown capture view")

            with urlopen(base_url + "/api/v1/panels/" + quote(record["panel_id"]) + "/passport", timeout=5) as response:
                paired_passport = json.loads(response.read())
            if (paired_passport["schema_version"] != "1.6"
                    or paired_passport["inspection_count"] != 5
                    or paired_passport["inspections"][1]["camera_modality"] != "near_infrared"
                    or paired_passport["inspections"][2]["camera_modality"] != "thermal_infrared"
                    or paired_passport["inspections"][4]["capture_view"] != "rear_nameplate"
                    or paired_passport["integrity"]["status"] != "verified"):
                raise RuntimeError("The multimodal passport did not preserve paired image provenance")

            thin_film_reference = f"PC-THIN-FILM-{uuid.uuid4().hex[:8]}"
            thin_film_headers = {
                **headers,
                "X-Request-ID": uuid.uuid4().hex,
                "X-Panel-Ref": thin_film_reference,
                "X-Panel-Technology": "thin_film",
                "X-Frame-Width-MM": "1650",
                "X-Frame-Height-MM": "990",
                "X-Junction-Box": "rear_center",
            }
            _, thin_film_record = post(base_url + "/api/v1/inspections", image_bytes, thin_film_headers)
            if (thin_film_record["recommended_disposition"] != "ROUTE_TO_LICENSED_HANDLER"
                    or thin_film_record["panel_technology"] != "thin_film"
                    or thin_film_record["frame_width_mm"] != 1650
                    or thin_film_record["frame_height_mm"] != 990
                    or thin_film_record["junction_box_location"] != "rear_center"):
                raise RuntimeError("Thin-film routing rule was not applied")
            with urlopen(base_url + "/api/v1/panels/" + quote(thin_film_record["panel_id"]) + "/passport", timeout=5) as response:
                passport = json.loads(response.read())
            if (passport["schema_version"] != "1.6" or passport["inspection_count"] != 1
                    or passport["inspections"][0]["frame_width_mm"] != 1650
                    or passport["integrity"]["status"] != "verified"
                    or passport["integrity"]["verified_records"] != 1):
                raise RuntimeError("Panel passport endpoint did not return its inspection history")

            thin_film_override = {
                "image_data": "data:image/jpeg;base64," + base64.b64encode(image_bytes).decode("ascii"),
                "panel_technology": "thin_film",
                "final_disposition": "REPAIRED",
                "reviewer_note": "This should be rejected by the intact-routing guard.",
            }
            try:
                post(
                    base_url + "/api/inspect",
                    json.dumps(thin_film_override).encode("utf-8"),
                    {"Content-Type": "application/json"},
                )
            except HTTPError as error:
                error_body = json.loads(error.read())
                if error.code != 400 or "must remain intact" not in error_body.get("error", ""):
                    raise RuntimeError("Thin-film override guard returned the wrong response") from error
            else:
                raise RuntimeError("Thin-film route was overridden")

            false_pass_headers = {**headers, "X-Request-ID": uuid.uuid4().hex, "X-Electrical-Test": "pass"}
            try:
                post(base_url + "/api/v1/inspections", image_bytes, false_pass_headers)
            except HTTPError as error:
                error_body = json.loads(error.read())
                if error.code != 400 or "raw telemetry only" not in error_body.get("error", ""):
                    raise RuntimeError("The device API returned the wrong error for a pass without readings") from error
            else:
                raise RuntimeError("The device API accepted an electrical pass without readings")

            operator_body = {
                "image_data": "data:image/jpeg;base64," + base64.b64encode(image_bytes).decode("ascii"),
                "electrical_test": "not_tested",
                "final_disposition": "MANUALLY_INSPECTED",
                "reviewer_note": "Synthetic PC simulator workflow check only.",
                "confirmed_visual_label": "other",
            }
            try:
                post(
                    base_url + "/api/inspect",
                    json.dumps({**operator_body, "camera_modality": "near_infrared",
                                "confirmed_visual_label": "clean"}).encode("utf-8"),
                    {"Content-Type": "application/json"},
                )
            except HTTPError as error:
                error_body = json.loads(error.read())
                if error.code != 400 or "RGB training labels" not in error_body.get("error", ""):
                    raise RuntimeError("The operator API allowed an RGB class on an NIR capture") from error
            else:
                raise RuntimeError("The operator API accepted an RGB class on an NIR capture")
            try:
                post(
                    base_url + "/api/inspect",
                    json.dumps({**operator_body, "frame_width_mm": 1650}).encode("utf-8"),
                    {"Content-Type": "application/json"},
                )
            except HTTPError as error:
                error_body = json.loads(error.read())
                if error.code != 400 or "both frame width and height" not in error_body.get("error", ""):
                    raise RuntimeError("Partial frame measurement validation returned the wrong response") from error
            else:
                raise RuntimeError("The operator API accepted a partial frame measurement")
            operator_status, operator_record = post(
                base_url + "/api/inspect",
                json.dumps(operator_body).encode("utf-8"),
                {"Content-Type": "application/json"},
            )
            if operator_status != 201 or operator_record["final_disposition"] != "MANUALLY_INSPECTED":
                raise RuntimeError("Operator inspection and documented override check failed")

            operator_body["electrical_test"] = "pass"
            try:
                post(
                    base_url + "/api/inspect",
                    json.dumps(operator_body).encode("utf-8"),
                    {"Content-Type": "application/json"},
                )
            except HTTPError as error:
                error_body = json.loads(error.read())
                if error.code != 400 or "requires recorded voltage and current" not in error_body.get("error", ""):
                    raise RuntimeError("The operator API returned the wrong error for a pass without readings") from error
            else:
                raise RuntimeError("The operator API accepted an electrical pass without readings")

            qualified_test_body = {
                **operator_body,
                "electrical_test": "pass",
                "voltage": 3.0,
                "current": 0.12,
                "electrical_method": "Synthetic low-voltage procedure",
                "electrical_instrument": "DEMO-METER-01",
                "electrical_operator": "PC simulator",
            }
            qualified_status, qualified_record = post(
                base_url + "/api/inspect",
                json.dumps(qualified_test_body).encode("utf-8"),
                {"Content-Type": "application/json"},
            )
            if (qualified_status != 201 or qualified_record["electrical_test"] != "pass"
                    or qualified_record["electrical_instrument"] != "DEMO-METER-01"
                    or qualified_record["final_disposition"] != "MANUALLY_INSPECTED"):
                raise RuntimeError("Qualified-test provenance was not recorded independently from reuse approval")

            stage2_body = {
                **operator_body,
                "panel_technology": "c_si",
                "electrical_test": "not_tested",
                "final_route": "STAGE_2_CSI",
                "final_disposition": "ROUTED_TO_STAGE_2",
            }
            try:
                post(base_url + "/api/inspect", json.dumps(stage2_body).encode("utf-8"),
                     {"Content-Type": "application/json"})
            except HTTPError as error:
                error_body = json.loads(error.read())
                if error.code != 400 or "isolation check" not in error_body.get("error", ""):
                    raise RuntimeError("Stage 2 safety interlock returned the wrong response") from error
            else:
                raise RuntimeError("Stage 2 route was accepted without isolation confirmation")

            stage2_body["stage2_isolation_confirmed"] = True
            stage2_status, stage2_record = post(
                base_url + "/api/inspect", json.dumps(stage2_body).encode("utf-8"),
                {"Content-Type": "application/json"},
            )
            if (stage2_status != 201 or stage2_record["final_route"] != "STAGE_2_CSI"
                    or not stage2_record["stage2_isolation_confirmed"]
                    or stage2_record["sort_lane_decision"]["lane"] != "RIGHT"
                    or stage2_record["sort_lane_decision"]["actuator_commanded"]):
                raise RuntimeError("Stage 2 route did not retain its human isolation checkpoint")

            event_headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            }
            occurred_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            stage3_early = {
                "event_id": uuid.uuid4().hex,
                "stage_code": "stage_3",
                "event_type": "process_started",
                "station_id": "pc-sim-stage-3",
                "operator_id": "pc-simulator",
                "occurred_at": occurred_at,
            }
            try:
                post(
                    base_url + "/api/v1/panels/" + quote(stage2_record["panel_id"]) + "/events",
                    json.dumps({**stage3_early, "command": "start-heater"}).encode("utf-8"), event_headers,
                )
            except HTTPError as error:
                event_error = json.loads(error.read())
                if error.code != 400 or "unsupported stage event fields" not in event_error.get("error", "").lower():
                    raise RuntimeError("The event API did not reject actuator command fields") from error
            else:
                raise RuntimeError("The measurement API accepted an actuator command field")
            try:
                post(
                    base_url + "/api/v1/panels/" + quote(stage2_record["panel_id"]) + "/events",
                    json.dumps(stage3_early).encode("utf-8"), event_headers,
                )
            except HTTPError as error:
                event_error = json.loads(error.read())
                if error.code != 409 or "stage 2" not in event_error.get("error", "").lower():
                    raise RuntimeError("Stage event ordering guard returned the wrong response") from error
            else:
                raise RuntimeError("Stage 3 event was accepted before a Stage 2 completion")

            stage2_event = {
                "event_id": uuid.uuid4().hex,
                "stage_code": "stage_2",
                "event_type": "process_completed",
                "station_id": "pc-sim-stage-2",
                "operator_id": "pc-simulator",
                "occurred_at": occurred_at,
                "instrument_id": "SIM-SCALE-01",
                "calibration_ref": "SIM-CAL-2026-01",
                "measurements": [
                    {"name": "input_mass", "value": 4.2, "unit": "kg"},
                    {"name": "frame_output_mass", "value": 0.35, "unit": "kg"},
                ],
            }
            stage2_event_url = base_url + "/api/v1/panels/" + quote(stage2_record["panel_id"]) + "/events"
            stage2_event_status, saved_stage2_event = post(
                stage2_event_url, json.dumps(stage2_event).encode("utf-8"), event_headers
            )
            retry_status, retried_stage2_event = post(
                stage2_event_url, json.dumps(stage2_event).encode("utf-8"), event_headers
            )
            if (stage2_event_status != 201 or retry_status != 200
                    or saved_stage2_event["event_id"] != retried_stage2_event["event_id"]
                    or saved_stage2_event["measurements"][1]["unit"] != "kg"):
                raise RuntimeError("Stage event provenance or idempotent retry check failed")
            invalid_mass_event = {
                **stage2_event,
                "event_id": uuid.uuid4().hex,
                "event_type": "measurement",
                "measurements": [{"name": "invalid_mass", "value": -1, "unit": "kg"}],
            }
            try:
                post(stage2_event_url, json.dumps(invalid_mass_event).encode("utf-8"), event_headers)
            except HTTPError as error:
                event_error = json.loads(error.read())
                if error.code != 400 or "cannot be negative" not in event_error.get("error", ""):
                    raise RuntimeError("Negative mass measurement returned the wrong response") from error
            else:
                raise RuntimeError("The event API accepted a negative mass")
            try:
                changed_retry = {**stage2_event, "measurements": [
                    {"name": "input_mass", "value": 99, "unit": "kg"},
                ]}
                post(stage2_event_url, json.dumps(changed_retry).encode("utf-8"), event_headers)
            except HTTPError as error:
                event_error = json.loads(error.read())
                if error.code != 409 or "different event content" not in event_error.get("error", "").lower():
                    raise RuntimeError("Conflicting event ID reuse returned the wrong response") from error
            else:
                raise RuntimeError("An event ID was reused with different measurement data")

            stage4_early = {
                **stage3_early,
                "event_id": uuid.uuid4().hex,
                "stage_code": "stage_4",
                "station_id": "pc-sim-stage-4",
            }
            try:
                post(stage2_event_url, json.dumps(stage4_early).encode("utf-8"), event_headers)
            except HTTPError as error:
                event_error = json.loads(error.read())
                if error.code != 409 or "stage 3" not in event_error.get("error", "").lower():
                    raise RuntimeError("Stage 4 ordering guard returned the wrong response") from error
            else:
                raise RuntimeError("Stage 4 event was accepted before a Stage 3 completion")

            stage3_event = {
                **stage2_event,
                "event_id": uuid.uuid4().hex,
                "stage_code": "stage_3",
                "station_id": "pc-sim-stage-3",
                "instrument_id": "SIM-TEMP-01",
                "calibration_ref": "SIM-CAL-2026-02",
                "measurements": [
                    {"name": "thermal_zone_temperature", "value": 165, "unit": "C"},
                    {"name": "glass_output_mass", "value": 3.1, "unit": "kg"},
                ],
            }
            stage3_missing_temperature = {
                **stage3_event,
                "event_id": uuid.uuid4().hex,
                "measurements": [{"name": "glass_output_mass", "value": 3.1, "unit": "kg"}],
            }
            try:
                post(stage2_event_url, json.dumps(stage3_missing_temperature).encode("utf-8"), event_headers)
            except HTTPError as error:
                event_error = json.loads(error.read())
                if error.code != 400 or "temperature" not in event_error.get("error", "").lower():
                    raise RuntimeError("Stage 3 temperature provenance returned the wrong response") from error
            else:
                raise RuntimeError("Stage 3 was marked complete without a temperature measurement")
            _, saved_stage3_event = post(stage2_event_url, json.dumps(stage3_event).encode("utf-8"), event_headers)
            if saved_stage3_event["stage_code"] != "stage_3":
                raise RuntimeError("Stage 3 process event was not saved")

            stage4_event = {
                **stage2_event,
                "event_id": uuid.uuid4().hex,
                "stage_code": "stage_4",
                "station_id": "pc-sim-stage-4",
                "instrument_id": "SIM-SCALE-02",
                "calibration_ref": "SIM-CAL-2026-03",
                "measurements": [
                    {"name": "copper_output_mass", "value": 0.04, "unit": "kg"},
                ],
            }
            _, saved_stage4_event = post(stage2_event_url, json.dumps(stage4_event).encode("utf-8"), event_headers)
            if saved_stage4_event["stage_code"] != "stage_4":
                raise RuntimeError("Stage 4 process event was not saved")

            structural_review = {
                **operator_body,
                "electrical_test": "not_tested",
                "panel_technology": "c_si",
                "confirmed_visual_label": "crack",
            }
            _, structural_record = post(
                base_url + "/api/inspect", json.dumps(structural_review).encode("utf-8"),
                {"Content-Type": "application/json"},
            )
            if (structural_record["recommended_route"] != "SAFETY_HOLD"
                    or structural_record["final_route"] != "SAFETY_HOLD"
                    or structural_record["route_source"] != "human_confirmed_label"
                    or structural_record["sort_lane_decision"]["lane"] != "HOLD"):
                raise RuntimeError("Human-confirmed structural damage did not trigger the safety hold")

            clean_predictions = [
                {"label": "clean", "confidence": 0.92},
                {"label": "dust", "confidence": 0.03},
            ]
            route_cases = (
                (recommend_route(clean_predictions, "pass", "c_si")[0], "SECOND_LIFE_REVIEW"),
                (recommend_route(clean_predictions, "not_tested", "c_si")[0], "ELECTRICAL_TEST_REQUIRED"),
                (recommend_route(clean_predictions, "not_tested", "thin_film")[0], "LICENSED_THIN_FILM_HANDLER"),
                (recommend_route(clean_predictions, "fail", "thin_film")[0], "SAFETY_HOLD"),
                (recommend_route([{"label": "crack", "confidence": 0.95}], "not_tested", "unknown")[0], "SAFETY_HOLD"),
                (recommend_route(clean_predictions, "not_tested", "c_si", "dust")[0], "SERVICE_AND_RETEST"),
            )
            if any(actual != expected for actual, expected in route_cases):
                raise RuntimeError("Conservative sort-route rule checks failed")

            tamper_path = temp_path / thin_film_record["image_path"]
            tamper_path.write_bytes(b"tampered image bytes")
            with urlopen(base_url + "/api/v1/panels/" + quote(thin_film_record["panel_id"]) + "/passport", timeout=5) as response:
                tampered_passport = json.loads(response.read())
            if tampered_passport["integrity"]["status"] != "integrity_error":
                raise RuntimeError("Passport verification did not detect altered image bytes")

            with urlopen(base_url + "/api/v1/panels/" + quote(stage2_record["panel_id"]) + "/passport", timeout=5) as response:
                process_passport = json.loads(response.read())
            if (process_passport["schema_version"] != "1.6"
                    or [event["stage_code"] for event in process_passport["stage_events"]] != ["stage_2", "stage_3", "stage_4"]
                    or process_passport["event_integrity"]["status"] != "verified"):
                raise RuntimeError("Process event history or its integrity chain was not returned")
            database_connection = sqlite3.connect(eye.ledger.database_path)
            try:
                database_connection.row_factory = sqlite3.Row
                raw_events = [dict(row) for row in database_connection.execute(
                    """SELECT e.*, p.panel_id FROM stage_events e
                       JOIN panels p ON p.id = e.panel_row_id
                       WHERE p.panel_id = ? ORDER BY e.id""",
                    (stage2_record["panel_id"],),
                ).fetchall()]
            finally:
                database_connection.close()
            tampered_event = dict(raw_events[0])
            tampered_event["note"] += " changed"
            if Ledger._verify_stage_events([tampered_event])["status"] != "integrity_error":
                raise RuntimeError("The stage event hash did not detect changed event content")
            with urlopen(base_url + "/api/panels", timeout=5) as response:
                panel_rows = json.loads(response.read())
            panel_summary = next(row for row in panel_rows if row["panel_id"] == stage2_record["panel_id"])
            if (panel_summary["stage_event_count"] != 3
                    or panel_summary["last_stage_code"] != "stage_4"
                    or panel_summary["last_stage_event_type"] != "process_completed"):
                raise RuntimeError("Panel ledger did not summarize the latest downstream stage event")

            print("PASS: /api/v1/health reports ready")
            print(f"PASS: authenticated synthetic camera upload saved as inspection {record['id']}")
            print("PASS: saved image URL returned its JPEG with the recorded SHA-256")
            print("PASS: retry with the same request ID returned the same inspection")
            print("PASS: rear nameplate capture was linked to the existing panel passport")
            print("PASS: unsupported capture views are rejected")
            print("PASS: device record retained electrical_test=not_tested and no readings")
            print("PASS: unknown panel technology remains in human review")
            print("PASS: thin-film inspection routes intact to licensed handler")
            print("PASS: thin-film routing cannot be overridden in the prototype")
            print("PASS: versioned material passport returns the panel history")
            print("PASS: paired RGB/NIR captures retain modality, sensor, and group provenance; NIR bypasses RGB inference")
            print("PASS: thermal captures use the separate research model and hold possible cracking for human review")
            print("PASS: visible close-up defect hints stay advisory and map to a non-actuating human-review destination")
            print("PASS: stage 2-4 process events append calibrated measurements to the panel passport")
            print("PASS: stage event order, retries, and event hash chain are verified")
            print("PASS: measured frame dimensions and junction-box location travel into the passport")
            print("PASS: partial frame measurements are rejected")
            print("PASS: device API rejects device-asserted electrical pass/fail")
            print("PASS: electrical pass requires readings and method/instrument/operator provenance")
            print("PASS: electrical pass alone does not approve reuse")
            print("PASS: Stage 2 routing requires explicit isolation confirmation and a reviewer note")
            print("PASS: human-confirmed structural damage triggers a source-audited safety hold")
            print("PASS: route rules hold thin-film intact, require output testing for second life, and hold structural concerns")
            print("PASS: passport record and image hashes verify; altered image bytes are detected")
            print("PASS: operator review override was accepted with a reviewer note")
            print(f"Model: {health['model']['message']}")
            print("No real panel, camera, electrical sensor, or solar-model inference was tested.")
    finally:
        if server is not None:
            server.shutdown()
            server.server_close()
        if thread is not None:
            thread.join(timeout=5)
        eye.ledger = previous_ledger
        eye.classifier = previous_classifier
        eye.thermal_classifier = previous_thermal_classifier
        eye.visible_crop_classifier = previous_visible_crop_classifier
        eye.power_loss_estimator = previous_power_loss_estimator
        if previous_token is None:
            os.environ.pop("AGASTYA_DEVICE_TOKEN", None)
        else:
            os.environ["AGASTYA_DEVICE_TOKEN"] = previous_token


if __name__ == "__main__":
    main()
