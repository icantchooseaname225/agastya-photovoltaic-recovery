"""Local web application for Agastya-EYE inspections and the panel ledger."""

import argparse
import base64
import binascii
import csv
import hmac
import ipaddress
import json
import math
import mimetypes
import os
import re
import socket
import sqlite3
import threading
import time
import warnings
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from PIL import Image, UnidentifiedImageError

from inference.classifier import LABELS, SolarClassifier
from inference.estimation import ResearchPowerLossEstimator
from inference.ledger import EventConflictError, Ledger
from inference.material_ledger import MaterialLedger
from inference.thermal_classifier import ThermalClassifier
from inference.visible_crop_classifier import VisibleCropDefectClassifier
from inference.triage import (
    DISPOSITIONS,
    PANEL_TECHNOLOGIES,
    SORT_ROUTES,
    recommend,
    recommend_route,
)
from hardware.approval import (
    DuplicateApprovalError,
    HardwareApprovalService,
    HardwareApprovalStore,
    IneligibleApprovalError,
    inspection_image_is_intact,
)
from hardware.arduino_config import ArduinoConfig
from hardware.arduino_controller import (
    ArduinoServoController,
    HardwareProtocolError,
    HardwareUnavailableError,
)

ROOT = Path(__file__).resolve().parent
WEB_ROOT = ROOT / "web"
IMAGE_ROOT = ROOT / "images"
DATASET_ROOT = ROOT / "datasets"
MAX_IMAGE_BYTES = 16 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"JPEG", "PNG", "WEBP", "BMP", "TIFF"}
JUNCTION_BOX_LOCATIONS = ("unknown", "rear_center", "rear_upper", "rear_lower", "rear_left", "rear_right", "other")
CAPTURE_VIEWS = ("unspecified", "front", "rear_nameplate", "rear_junction_box", "rear_overview")
DEVICE_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,79}$")
REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9_.:-]{1,96}$")
CAMERA_MODALITIES = {
    "visible_rgb": "visible RGB",
    "visible_rgb_closeup": "visible RGB close-up",
    "near_infrared": "near-infrared",
    "thermal_infrared": "thermal infrared",
    "electroluminescence": "electroluminescence",
}
STAGE_CODES = {"stage_2", "stage_3", "stage_4"}
STAGE_EVENT_TYPES = {"measurement", "material_output", "process_started", "process_completed", "safety_hold"}
MEASUREMENT_UNITS = {"g", "kg", "C", "V", "A", "W", "J", "Wh", "kWh", "s", "min", "mm", "count", "percent", "rpm"}
ledger = Ledger(ROOT / "database" / "eye.sqlite3", IMAGE_ROOT)
material_ledger = MaterialLedger(ROOT / "database" / "eye.sqlite3")
classifier = SolarClassifier()
thermal_classifier = ThermalClassifier()
visible_crop_classifier = VisibleCropDefectClassifier()
power_loss_estimator = ResearchPowerLossEstimator()
arduino_config = ArduinoConfig.from_env()
arduino_controller = ArduinoServoController(arduino_config)
hardware_approval_store = HardwareApprovalStore(ROOT / "database" / "hardware.sqlite3")
hardware_approval_service = HardwareApprovalService(
    arduino_controller,
    hardware_approval_store,
    max_age_seconds=arduino_config.approval_max_age_seconds,
)
DATASET_STATUS_CACHE_SECONDS = 30.0
_dataset_status_lock = threading.Lock()
_dataset_status_cache = {"created_at": 0.0, "value": None}


def parse_measurement(value, label):
    if value in (None, ""):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} must be a number") from error
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{label} must be finite and non-negative")
    return number


def validate_electrical_test(test_status, voltage, current, method, instrument, operator):
    if test_status in ("pass", "fail"):
        if voltage is None or current is None:
            raise ValueError("A qualified electrical result requires recorded voltage and current readings")
        if not method or not instrument or not operator:
            raise ValueError("A qualified electrical result requires the method, instrument ID, and operator")


def parse_dimension(value, label):
    measurement = parse_measurement(value, label)
    if measurement is not None and not 10 <= measurement <= 5000:
        raise ValueError(f"{label} must be between 10 and 5,000 mm")
    return measurement


def parse_rated_power(value):
    measurement = parse_measurement(value, "Nameplate power")
    if measurement is not None and not 1 <= measurement <= 5000:
        raise ValueError("Nameplate power must be between 1 and 5,000 W")
    return measurement


def parse_device_timestamp(value, label="X-Captured-At"):
    value = (value or "").strip()
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"{label} must be an ISO-8601 timestamp") from error
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc).isoformat(timespec="seconds")


def parse_capture_metadata(modality, sensor_id, capture_group_id):
    modality = (modality or "visible_rgb").strip().lower()
    if modality not in CAMERA_MODALITIES:
        choices = ", ".join(CAMERA_MODALITIES)
        raise ValueError(f"Camera modality must be one of: {choices}")
    sensor_id = (sensor_id or "unknown").strip()
    if not DEVICE_ID_PATTERN.fullmatch(sensor_id):
        raise ValueError("Camera sensor ID must use letters, numbers, '.', '_', ':' or '-' (up to 80 characters)")
    capture_group_id = (capture_group_id or "").strip() or None
    if capture_group_id and not REQUEST_ID_PATTERN.fullmatch(capture_group_id):
        raise ValueError("Capture group ID contains unsupported characters")
    return modality, sensor_id, capture_group_id


def parse_capture_view(value):
    view = str(value or "unspecified").strip().lower()
    if view not in CAPTURE_VIEWS:
        raise ValueError(f"Capture view must be one of: {', '.join(CAPTURE_VIEWS)}")
    return view


def image_from_bytes(image_bytes):
    if not image_bytes or len(image_bytes) > MAX_IMAGE_BYTES:
        raise ValueError("Image is empty or larger than 16 MB")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            image = Image.open(BytesIO(image_bytes))
            if image.format not in ALLOWED_IMAGE_TYPES:
                raise ValueError("Use a JPEG, PNG, WebP, BMP, or TIFF image")
            if image.width * image.height > 80_000_000:
                raise ValueError("Image dimensions are too large")
            image.verify()
            image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError, Image.DecompressionBombWarning) as error:
        raise ValueError("The uploaded file is not a valid supported image") from error
    if image.width * image.height > 80_000_000:
        raise ValueError("Image dimensions are too large")
    output = BytesIO()
    image.save(output, format="JPEG", quality=92, optimize=True)
    return image, output.getvalue()


def dataset_status(*, refresh=False):
    now = time.monotonic()
    cached = _dataset_status_cache["value"]
    if not refresh and cached is not None and now - _dataset_status_cache["created_at"] < DATASET_STATUS_CACHE_SECONDS:
        return cached
    with _dataset_status_lock:
        now = time.monotonic()
        cached = _dataset_status_cache["value"]
        if not refresh and cached is not None and now - _dataset_status_cache["created_at"] < DATASET_STATUS_CACHE_SECONDS:
            return cached
        value = _build_dataset_status()
        _dataset_status_cache.update({"created_at": now, "value": value})
        return value


def _build_dataset_status():
    processed = DATASET_ROOT / "processed"
    counts = {}
    for split in ("train", "validation", "test"):
        split_path = processed / split
        counts[split] = {
            label: sum(len(files) for _, _, files in os.walk(split_path / label))
            if (split_path / label).is_dir() else 0
            for label in LABELS
        }

    sources = []
    raw_root = DATASET_ROOT / "raw"
    if raw_root.is_dir():
        for source in sorted(path for path in raw_root.iterdir() if path.is_dir()):
            image_count = sum(
                sum(Path(name).suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"} for name in files)
                for _, _, files in os.walk(source)
            )
            sources.append({"source_id": source.name, "images": image_count})
    mappings = []
    manifest = DATASET_ROOT / "source_manifest.csv"
    if manifest.is_file():
        with manifest.open("r", encoding="utf-8-sig", newline="") as file:
            mappings = [row for row in csv.DictReader(file) if row.get("source_id")]
    benchmarks = []
    benchmark_root = processed / "pv_degradation_benchmark"
    for modality in ("HDR", "BW", "EL"):
        benchmark_report = benchmark_root / f"{modality.lower()}_benchmark_report.json"
        if not benchmark_report.is_file():
            continue
        with benchmark_report.open("r", encoding="utf-8") as file:
            report = json.load(file)
        benchmarks.append({
            "status": report.get("status"),
            "modality": report.get("modality"),
            "samples": report.get("samples"),
            "physical_cells": report.get("physical_cells", []),
            "fold_count": report.get("fold_count"),
            "overall_metrics": report.get("overall_cell_held_out_metrics", {}),
            "folds": report.get("folds", []),
            "limitations": report.get("limitations", []),
            "source": report.get("source", {}),
        })
    return {
        "sources": sources,
        "mapping_rows": len(mappings),
        "mappings": mappings,
        "processed": counts,
        "human_labeled_images": ledger.counts()["human_labeled_images"],
        "pv_degradation_benchmarks": benchmarks,
        "thermal_model": thermal_classifier.status(load=False),
        "visible_crop_model": visible_crop_classifier.status(load=False),
    }


def system_health():
    """Return readiness from the database and primary RGB inference model."""
    database_status = ledger.health_check()
    model_status = classifier.status(load=False)
    thermal_status = thermal_classifier.status(load=False)
    visible_crop_status = visible_crop_classifier.status(load=False)
    if not database_status["healthy"] or not model_status.get("ready"):
        status = "degraded"
    elif model_status.get("loading") or not model_status.get("loaded"):
        status = "warming"
    else:
        status = "ready"
    return {
        "api_version": "v1",
        "status": status,
        "inspection_ready": status == "ready",
        "database": database_status,
        "model": model_status,
        "thermal_model": thermal_status,
        "visible_crop_model": visible_crop_status,
        "device_upload_enabled": bool(os.environ.get("AGASTYA_DEVICE_TOKEN")),
        "hardware": {
            **arduino_controller.get_status(),
            "approval_ledger": hardware_approval_store.health_check(),
        },
    }


def inspection_image_available(record):
    return inspection_image_is_intact(record, project_root=ROOT, image_root=IMAGE_ROOT)


def fetch_camera_snapshot(camera_url):
    parsed = urlsplit(camera_url.strip())
    if parsed.scheme != "http" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Enter an http:// URL for an ESP32 camera snapshot endpoint")
    host = parsed.hostname.rstrip(".").lower()
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(host, parsed.port or 80, type=socket.SOCK_STREAM)}
    except OSError as error:
        raise ValueError("The camera host could not be reached on this network") from error
    if not addresses or any(
        not ipaddress.ip_address(address).is_private
        or ipaddress.ip_address(address).is_loopback
        or ipaddress.ip_address(address).is_link_local
        for address in addresses
    ):
        raise ValueError("Camera must be on a private local network")

    class NoRedirect(HTTPRedirectHandler):
        def redirect_request(self, request, file_pointer, code, message, headers, new_url):
            return None

    request = Request(camera_url.strip(), headers={"Accept": "image/jpeg,image/png,image/*"})
    try:
        with build_opener(NoRedirect).open(request, timeout=8) as response:
            content_type = response.headers.get_content_type()
            if not content_type.startswith("image/"):
                raise ValueError("Camera endpoint did not return an image; use its /capture URL")
            image_bytes = response.read(MAX_IMAGE_BYTES + 1)
    except (HTTPError, URLError, TimeoutError, OSError) as error:
        raise ValueError(f"Could not capture from the camera: {error}") from error
    image_from_bytes(image_bytes)
    return image_bytes


class EyeHandler(BaseHTTPRequestHandler):
    server_version = "AgastyaEYE/1.0"

    def do_GET(self):
        try:
            return self._handle_get()
        except (sqlite3.Error, OSError) as error:
            self.log_error("GET %s unavailable: %s", self.path, error)
            return self._json({"error": "EYE could not read the requested data"}, 503)
        except Exception as error:
            self.log_error("GET %s failed: %s", self.path, error)
            return self._json({"error": "EYE could not complete the request"}, 500)

    def _handle_get(self):
        path = urlsplit(self.path).path
        if path == "/" or path == "/index.html":
            return self._file(WEB_ROOT / "index.html")
        if path in ("/app.js", "/process.js", "/materials.js", "/styles.css"):
            return self._file(WEB_ROOT / path.lstrip("/"))
        if path == "/source-manifest.csv":
            return self._file(DATASET_ROOT / "source_manifest.csv")
        if path == "/api/ping":
            return self._json({"status": "ready", "app": "Agastya-EYE"})
        if path == "/api/status":
            return self._json({
                "model": classifier.status(load=False),
                "thermal_model": thermal_classifier.status(load=False),
                "visible_crop_model": visible_crop_classifier.status(load=False),
                "dataset": dataset_status(),
                "database": ledger.health_check(),
                "hardware": {
                    **arduino_controller.get_status(),
                    "approval_ledger": hardware_approval_store.health_check(),
                },
                **ledger.counts(),
            })
        if path == "/api/panels":
            return self._json(ledger.list_panels())
        if path == "/api/material/records":
            return self._json(material_ledger.list_records())
        if path == "/api/material/runs":
            records = material_ledger.list_records()
            return self._json([record for record in records if record["record_type"] == "run"])
        if path.startswith("/api/material/runs/") and path.endswith("/report"):
            run_id = unquote(path[len("/api/material/runs/"):-len("/report")].strip("/"))
            report = material_ledger.get_run_report(run_id)
            return self._json(report) if report else self._json({"error": "Run not found"}, 404)
        if path == "/api/material/compare":
            records = material_ledger.list_records()
            runs = [record for record in records if record["record_type"] == "run"]
            return self._json([material_ledger.get_run_report(run["record_id"]) for run in runs])
        if path == "/api/inspections":
            return self._json(ledger.list_inspections())
        if path == "/api/datasets":
            return self._json(dataset_status())
        if path == "/api/v1/health":
            health = system_health()
            status_code = 200 if health["status"] == "ready" else 503
            return self._json(health, status_code)
        if path == "/api/v1/hardware/status":
            return self._json({
                **arduino_controller.get_status(),
                "approval_ledger": hardware_approval_store.health_check(),
            })
        hardware_release_match = re.fullmatch(r"/api/v1/hardware/inspections/(\d+)/release", path)
        if hardware_release_match:
            inspection_id = int(hardware_release_match.group(1))
            record = ledger.get_inspection(inspection_id)
            if not record:
                return self._json({"error": "Inspection not found"}, 404)
            approval = hardware_approval_store.get_by_inspection(inspection_id)
            health = system_health()
            eligibility = hardware_approval_service.get_eligibility(
                record,
                backend_ready=health["inspection_ready"],
                image_available=inspection_image_available(record),
            )
            return self._json({
                "eligibility": eligibility,
                "approval": approval,
                "hardware": arduino_controller.get_status(),
                "approval_ledger": hardware_approval_store.health_check(),
                "approval_max_age_seconds": arduino_config.approval_max_age_seconds,
            })
        if path == "/api/v1/panels":
            return self._json(ledger.list_panels())
        if path.startswith("/api/v1/panels/") and path.endswith("/passport"):
            panel_id = unquote(path[len("/api/v1/panels/"):-len("/passport")].strip("/"))
            if not panel_id or "/" in panel_id:
                return self._json({"error": "Invalid panel ID"}, 400)
            passport = ledger.get_passport(panel_id)
            return self._json(passport) if passport else self._json({"error": "Panel not found"}, 404)
        if path == "/api/v1/inspections":
            return self._json(ledger.list_inspections())
        if path.startswith("/api/v1/inspections/"):
            try:
                inspection_id = int(path.rsplit("/", 1)[1])
            except ValueError:
                return self._json({"error": "Invalid inspection ID"}, 400)
            record = ledger.get_inspection(inspection_id)
            return self._json(record) if record else self._json({"error": "Inspection not found"}, 404)
        if path.startswith("/api/inspections/"):
            try:
                inspection_id = int(path.rsplit("/", 1)[1])
            except ValueError:
                return self._json({"error": "Invalid inspection ID"}, 400)
            record = ledger.get_inspection(inspection_id)
            return self._json(record) if record else self._json({"error": "Inspection not found"}, 404)
        if path.startswith("/images/"):
            parts = Path(unquote(path).lstrip("/")).parts
            if len(parts) < 2 or parts[0] != "images":
                return self._json({"error": "Image not found"}, 404)
            image_root = ledger.image_root.resolve()
            target = image_root.joinpath(*parts[1:]).resolve()
            if not target.is_relative_to(image_root) or not target.is_file():
                return self._json({"error": "Image not found"}, 404)
            return self._file(target)
        return self._json({"error": "Not found"}, 404)

    def do_POST(self):
        path = urlsplit(self.path).path
        try:
            if path == "/api/material/records":
                return self._json(material_ledger.create_material_record(self._read_json(64 * 1024)), 201)
            if path == "/api/material/assays":
                return self._json(material_ledger.create_assay(self._read_json(64 * 1024)), 201)
            if path == "/api/material/runs":
                return self._json(material_ledger.create_run(self._read_json(64 * 1024)), 201)
            if path == "/api/v1/inspections":
                return self._device_inspect()
            if path.startswith("/api/v1/panels/") and path.endswith("/events"):
                return self._stage_event(path)
            if path == "/api/v1/hardware/connect":
                if not self._is_loopback_request():
                    return self._json({"error": "Arduino controls are available only from this computer"}, 403)
                result = hardware_approval_service.connect()
                return self._json(result, 200 if result["ready"] else 503)
            if path == "/api/v1/hardware/config":
                if not self._is_loopback_request():
                    return self._json({"error": "Arduino controls are available only from this computer"}, 403)
                return self._hardware_configure()
            hardware_release_match = re.fullmatch(r"/api/v1/hardware/inspections/(\d+)/release", path)
            if hardware_release_match:
                return self._hardware_release(int(hardware_release_match.group(1)))
            if path == "/api/v1/admin/shutdown":
                if not self._is_loopback_request():
                    return self._json({"error": "Shutdown is available only from this computer"}, 403)
                self._json({"status": "stopping"}, 202)
                threading.Thread(target=self.server.shutdown, name="eye-shutdown", daemon=True).start()
                return
            body = self._read_json()
            if path == "/api/capture":
                image_bytes = fetch_camera_snapshot(str(body.get("camera_url", "")))
                encoded = base64.b64encode(image_bytes).decode("ascii")
                return self._json({"image_data": f"data:image/jpeg;base64,{encoded}"})
            if path == "/api/inspect":
                return self._inspect(body)
            return self._json({"error": "Not found"}, 404)
        except EventConflictError as error:
            return self._json({"error": str(error)}, 409)
        except ValueError as error:
            return self._json({"error": str(error)}, 400)
        except sqlite3.IntegrityError as error:
            return self._json({"error": f"Ledger constraint: {error}"}, 409)
        except Exception as error:
            self.log_error("POST %s failed: %s", path, error)
            return self._json({"error": "EYE could not complete the request"}, 500)

    def _is_loopback_request(self):
        try:
            if not ipaddress.ip_address(self.client_address[0]).is_loopback:
                return False
        except ValueError:
            return False
        origin = self.headers.get("Origin")
        if origin:
            parsed_origin = urlsplit(origin)
            if parsed_origin.netloc.lower() != self.headers.get("Host", "").lower():
                return False
        return True

    def _hardware_release(self, inspection_id):
        if not self._is_loopback_request():
            return self._json({"error": "Arduino controls are available only from this computer"}, 403)
        record = ledger.get_inspection(inspection_id)
        if not record:
            return self._json({"error": "Inspection not found"}, 404)
        try:
            body = self._read_json(8 * 1024)
            health = system_health()
            result = hardware_approval_service.release(
                record,
                operator_id=body.get("operator_id"),
                panel_confirmation=body.get("panel_id_confirmation"),
                backend_ready=health["inspection_ready"],
                image_available=inspection_image_available(record),
            )
            return self._json(result)
        except DuplicateApprovalError as error:
            return self._json({"error": str(error), "retry_allowed": False}, 409)
        except IneligibleApprovalError as error:
            return self._json({"error": str(error), "retry_allowed": False}, 409)
        except HardwareUnavailableError as error:
            approval = hardware_approval_store.get_by_inspection(inspection_id)
            if approval:
                return self._json({
                    "error": str(error),
                    "release_status": approval["state"],
                    "retry_allowed": False,
                    "physical_position_verified": False,
                }, 503)
            return self._json({"error": str(error), "release_status": "not_sent", "retry_allowed": True}, 503)
        except HardwareProtocolError as error:
            self.log_error("Arduino release outcome is uncertain for inspection %s: %s", inspection_id, error)
            return self._json({
                "error": str(error),
                "release_status": "uncertain",
                "retry_allowed": False,
                "physical_position_verified": False,
            }, 502)
        except sqlite3.Error as error:
            self.log_error("Hardware approval ledger failed for inspection %s: %s", inspection_id, error)
            return self._json({"error": "Hardware approval could not be recorded; no retry is allowed for this inspection"}, 503)
        except Exception as error:
            self.log_error("Arduino release failed for inspection %s: %s", inspection_id, error)
            return self._json({
                "error": "Release status is uncertain; inspect the gate and do not retry this inspection",
                "release_status": "uncertain",
                "retry_allowed": False,
                "physical_position_verified": False,
            }, 502)

    def _hardware_configure(self):
        global arduino_config
        body = self._read_json(8 * 1024)
        if not isinstance(body.get("enabled"), bool):
            raise ValueError("enabled must be true or false")
        hardware = arduino_controller.set_activation(body["enabled"], body.get("port", ""))
        arduino_config = arduino_controller.config
        return self._json({"hardware": hardware, "session_only": True})

    def _inspect(self, body):
        image_data = str(body.get("image_data", ""))
        if "," in image_data and image_data.startswith("data:"):
            image_data = image_data.split(",", 1)[1]
        try:
            image_bytes = base64.b64decode(image_data, validate=True)
        except (binascii.Error, ValueError) as error:
            raise ValueError("Choose or capture an image before inspecting") from error
        panel_id = str(body.get("panel_id", "")).strip() or None
        external_ref = str(body.get("external_ref", "")).strip() or None
        if len(external_ref or "") > 120:
            raise ValueError("Asset reference must be 120 characters or fewer")
        electrical_test = body.get("electrical_test", "not_tested")
        if electrical_test not in ("not_tested", "pass", "fail"):
            raise ValueError("Electrical test must be not tested, pass, or fail")
        electrical_method = str(body.get("electrical_method", "")).strip()
        electrical_instrument = str(body.get("electrical_instrument", "")).strip()
        electrical_operator = str(body.get("electrical_operator", "")).strip()
        if len(electrical_method) > 160 or len(electrical_instrument) > 120 or len(electrical_operator) > 80:
            raise ValueError("Electrical method, instrument ID, or operator is too long")
        panel_technology = str(body.get("panel_technology", "unknown")).strip().lower()
        if panel_technology not in PANEL_TECHNOLOGIES:
            raise ValueError("Panel technology must be unknown, c_si, thin_film, or other")
        frame_width_mm = parse_dimension(body.get("frame_width_mm"), "Frame width")
        frame_height_mm = parse_dimension(body.get("frame_height_mm"), "Frame height")
        if (frame_width_mm is None) != (frame_height_mm is None):
            raise ValueError("Record both frame width and height, or leave both blank")
        junction_box_location = str(body.get("junction_box_location", "unknown")).strip().lower()
        if junction_box_location not in JUNCTION_BOX_LOCATIONS:
            raise ValueError("Choose a valid junction-box location")
        camera_modality, camera_sensor_id, capture_group_id = parse_capture_metadata(
            str(body.get("camera_modality", "visible_rgb")),
            str(body.get("camera_sensor_id", "operator-upload")),
            str(body.get("capture_group_id", "")),
        )
        capture_view = parse_capture_view(body.get("capture_view", "unspecified"))
        voltage = parse_measurement(body.get("voltage"), "Voltage")
        current = parse_measurement(body.get("current"), "Current")
        power = parse_measurement(body.get("power"), "Power")
        rated_power_w = parse_rated_power(body.get("rated_power_w"))
        validate_electrical_test(
            electrical_test, voltage, current, electrical_method, electrical_instrument, electrical_operator
        )

        chosen = str(body.get("final_disposition", "")).strip()
        if chosen and chosen not in DISPOSITIONS:
            raise ValueError("Select a valid final disposition")
        reviewer_note = str(body.get("reviewer_note", "")).strip()
        if len(reviewer_note) > 2000:
            raise ValueError("Reviewer note must be 2,000 characters or fewer")
        selected_route = str(body.get("final_route", "")).strip()
        if selected_route and selected_route not in SORT_ROUTES:
            raise ValueError("Select a valid downstream sort route")
        confirmed_visual_label = str(body.get("confirmed_visual_label", "")).strip().lower() or None
        if confirmed_visual_label and confirmed_visual_label not in LABELS:
            raise ValueError("Confirmed visual class must be one of the Agastya-EYE model classes")
        if confirmed_visual_label and (
            camera_modality != "visible_rgb" or capture_view not in ("front", "unspecified")
        ):
            raise ValueError("Full-panel RGB training labels require a front-view RGB capture")
        stage2_isolation_confirmed = body.get("stage2_isolation_confirmed", False)
        if not isinstance(stage2_isolation_confirmed, bool):
            raise ValueError("Stage 2 isolation confirmation must be true or false")
        record = self._create_inspection(
            image_bytes=image_bytes,
            panel_id=panel_id,
            external_ref=external_ref,
            electrical_test=electrical_test,
            voltage=voltage,
            current=current,
            power=power,
            rated_power_w=rated_power_w,
            panel_technology=panel_technology,
            frame_width_mm=frame_width_mm,
            frame_height_mm=frame_height_mm,
            junction_box_location=junction_box_location,
            chosen=chosen,
            reviewer_note=reviewer_note,
            selected_route=selected_route,
            electrical_method=electrical_method,
            electrical_instrument=electrical_instrument,
            electrical_operator=electrical_operator,
            confirmed_visual_label=confirmed_visual_label,
            stage2_isolation_confirmed=stage2_isolation_confirmed,
            camera_modality=camera_modality,
            camera_sensor_id=camera_sensor_id,
            capture_group_id=capture_group_id,
            capture_view=capture_view,
        )
        return self._json(record, 201)

    def _authorize_device(self):
        expected_token = os.environ.get("AGASTYA_DEVICE_TOKEN", "")
        if not expected_token:
            return self._json({"error": "Device uploads are disabled; configure AGASTYA_DEVICE_TOKEN"}, 503)
        authorization = self.headers.get("Authorization", "")
        scheme, _, supplied_token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not hmac.compare_digest(supplied_token.strip(), expected_token):
            return self._json({"error": "Unauthorized device"}, 401)
        return None

    def _stage_event(self, path):
        authorization_error = self._authorize_device()
        if authorization_error:
            return authorization_error
        if self.headers.get_content_type() != "application/json":
            return self._json({"error": "Stage events must use application/json"}, 415)
        panel_id = unquote(path[len("/api/v1/panels/"):-len("/events")].strip("/"))
        if not panel_id or "/" in panel_id or not DEVICE_ID_PATTERN.fullmatch(panel_id):
            return self._json({"error": "Invalid panel ID"}, 400)

        body = self._read_json(64 * 1024)
        allowed_fields = {
            "event_id", "stage_code", "event_type", "station_id", "occurred_at",
            "operator_id", "instrument_id", "calibration_ref", "measurements", "note",
        }
        extra_fields = set(body) - allowed_fields
        if extra_fields:
            raise ValueError(f"Unsupported stage event fields: {', '.join(sorted(extra_fields))}")
        event_id = str(body.get("event_id", "")).strip()
        if not REQUEST_ID_PATTERN.fullmatch(event_id):
            raise ValueError("event_id is required and must use letters, numbers, '.', '_', ':' or '-'")
        stage_code = str(body.get("stage_code", "")).strip().lower()
        if stage_code not in STAGE_CODES:
            raise ValueError("stage_code must be stage_2, stage_3, or stage_4")
        event_type = str(body.get("event_type", "")).strip().lower()
        if event_type not in STAGE_EVENT_TYPES:
            raise ValueError("event_type must be measurement, material_output, process_started, process_completed, or safety_hold")

        def required_id(field, label):
            value = str(body.get(field, "")).strip()
            if not DEVICE_ID_PATTERN.fullmatch(value):
                raise ValueError(f"{label} is required and must use letters, numbers, '.', '_', ':' or '-'")
            return value

        station_id = required_id("station_id", "station_id")
        operator_id = required_id("operator_id", "operator_id")
        instrument_id = str(body.get("instrument_id", "")).strip()
        calibration_ref = str(body.get("calibration_ref", "")).strip()
        for value, label in ((instrument_id, "instrument_id"), (calibration_ref, "calibration_ref")):
            if value and not DEVICE_ID_PATTERN.fullmatch(value):
                raise ValueError(f"{label} contains unsupported characters")
        occurred_at = parse_device_timestamp(str(body.get("occurred_at", "")), "occurred_at")
        if not occurred_at:
            raise ValueError("occurred_at is required for a traceable station event")
        measurements = body.get("measurements", [])
        if not isinstance(measurements, list) or len(measurements) > 100:
            raise ValueError("measurements must be a list containing at most 100 entries")
        normalized_measurements = []
        measurement_name_pattern = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,79}$")
        for measurement in measurements:
            if not isinstance(measurement, dict) or set(measurement) != {"name", "value", "unit"}:
                raise ValueError("Each measurement must contain only name, value, and unit")
            name = str(measurement["name"]).strip()
            unit = str(measurement["unit"]).strip()
            try:
                value = float(measurement["value"])
            except (TypeError, ValueError) as error:
                raise ValueError("Measurement values must be finite numbers") from error
            if (not measurement_name_pattern.fullmatch(name) or unit not in MEASUREMENT_UNITS
                    or not math.isfinite(value)):
                raise ValueError("Measurement name, unit, or value is invalid")
            if unit in {"g", "kg", "J", "Wh", "kWh", "s", "min", "mm", "count", "percent"} and value < 0:
                raise ValueError(f"{unit} measurements cannot be negative")
            if unit == "percent" and value > 100:
                raise ValueError("Percentage measurements must be between 0 and 100")
            if unit == "count" and not value.is_integer():
                raise ValueError("Count measurements must be whole numbers")
            normalized_measurements.append({"name": name, "value": value, "unit": unit})

        note = str(body.get("note", "")).strip()
        if len(note) > 2000:
            raise ValueError("Event note must be 2,000 characters or fewer")
        if event_type in {"measurement", "material_output"} and not normalized_measurements:
            raise ValueError(f"{event_type} events require at least one measured value")
        if event_type in {"measurement", "material_output", "process_completed"}:
            if not instrument_id or not calibration_ref:
                raise ValueError("Measured or completed events require instrument_id and calibration_ref")
        if event_type == "process_completed":
            units = {measurement["unit"] for measurement in normalized_measurements}
            if not units.intersection({"g", "kg"}):
                raise ValueError("Process completion requires at least one measured mass in g or kg")
            if stage_code == "stage_3" and "C" not in units:
                raise ValueError("Stage 3 completion requires a calibrated temperature measurement in C")

        event, duplicate = ledger.append_stage_event(
            panel_id=panel_id,
            event_id=event_id,
            stage_code=stage_code,
            event_type=event_type,
            station_id=station_id,
            occurred_at=occurred_at,
            operator_id=operator_id,
            instrument_id=instrument_id,
            calibration_ref=calibration_ref,
            measurements=normalized_measurements,
            note=note,
        )
        return self._json(event, 200 if duplicate else 201)

    def _device_inspect(self):
        authorization_error = self._authorize_device()
        if authorization_error:
            return authorization_error

        if self.headers.get_content_type() not in ("image/jpeg", "image/png"):
            return self._json({"error": "Device upload must be a JPEG or PNG image"}, 415)
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return self._json({"error": "Invalid Content-Length"}, 400)
        if length <= 0 or length > MAX_IMAGE_BYTES:
            return self._json({"error": "Image is empty or larger than 16 MB"}, 413)

        try:
            image_bytes = self.rfile.read(length)
            device_id = self.headers.get("X-Device-ID", "").strip()
            if not DEVICE_ID_PATTERN.fullmatch(device_id):
                raise ValueError("X-Device-ID is required and must use letters, numbers, '.', '_', ':' or '-'")
            request_id = self.headers.get("X-Request-ID", "").strip()
            if request_id and not REQUEST_ID_PATTERN.fullmatch(request_id):
                raise ValueError("X-Request-ID contains unsupported characters")
            external_ref = self.headers.get("X-Panel-Ref", "").strip() or None
            if len(external_ref or "") > 120:
                raise ValueError("X-Panel-Ref must be 120 characters or fewer")
            electrical_test = self.headers.get("X-Electrical-Test", "not_tested").strip().lower()
            if electrical_test != "not_tested":
                raise ValueError("Camera uploads may send raw telemetry only; a qualified operator must record electrical pass/fail in the app")
            panel_technology = self.headers.get("X-Panel-Technology", "unknown").strip().lower()
            if panel_technology not in PANEL_TECHNOLOGIES:
                raise ValueError("X-Panel-Technology must be unknown, c_si, thin_film, or other")
            frame_width_mm = parse_dimension(self.headers.get("X-Frame-Width-MM"), "Frame width")
            frame_height_mm = parse_dimension(self.headers.get("X-Frame-Height-MM"), "Frame height")
            if (frame_width_mm is None) != (frame_height_mm is None):
                raise ValueError("Record both frame width and height, or leave both blank")
            junction_box_location = self.headers.get("X-Junction-Box", "unknown").strip().lower()
            if junction_box_location not in JUNCTION_BOX_LOCATIONS:
                raise ValueError("X-Junction-Box must use a supported location")
            voltage = parse_measurement(self.headers.get("X-Voltage-V"), "Voltage")
            current = parse_measurement(self.headers.get("X-Current-A"), "Current")
            power = parse_measurement(self.headers.get("X-Power-W"), "Power")
            rated_power_w = parse_rated_power(self.headers.get("X-Rated-Power-W"))
            captured_at = parse_device_timestamp(self.headers.get("X-Captured-At"))
            camera_modality, camera_sensor_id, capture_group_id = parse_capture_metadata(
                self.headers.get("X-Camera-Modality", "visible_rgb"),
                self.headers.get("X-Camera-Sensor-ID", device_id),
                self.headers.get("X-Capture-Group-ID", ""),
            )
            capture_view = parse_capture_view(self.headers.get("X-Capture-View", "unspecified"))
            record = self._create_inspection(
                image_bytes=image_bytes,
                panel_id=None,
                external_ref=external_ref,
                electrical_test=electrical_test,
                voltage=voltage,
                current=current,
                power=power,
                rated_power_w=rated_power_w,
                panel_technology=panel_technology,
                frame_width_mm=frame_width_mm,
                frame_height_mm=frame_height_mm,
                junction_box_location=junction_box_location,
                chosen="",
                reviewer_note="",
                device_id=device_id,
                device_captured_at=captured_at,
                device_request_id=request_id or None,
                electrical_method="",
                electrical_instrument="",
                electrical_operator="",
                confirmed_visual_label=None,
                stage2_isolation_confirmed=False,
                camera_modality=camera_modality,
                camera_sensor_id=camera_sensor_id,
                capture_group_id=capture_group_id,
                capture_view=capture_view,
            )
            return self._json(record, 201)
        except ValueError as error:
            return self._json({"error": str(error)}, 400)

    def _create_inspection(self, image_bytes, panel_id, external_ref, electrical_test,
                           voltage, current, power, panel_technology, frame_width_mm,
                           frame_height_mm, junction_box_location, chosen, reviewer_note, device_id=None,
                           device_captured_at=None, device_request_id=None, selected_route="",
                           electrical_method="", electrical_instrument="", electrical_operator="",
                           confirmed_visual_label=None, stage2_isolation_confirmed=False,
                           camera_modality="visible_rgb", camera_sensor_id="unknown",
                           capture_group_id=None, rated_power_w=None, capture_view="unspecified"):
        if confirmed_visual_label and (
            camera_modality != "visible_rgb" or capture_view not in ("front", "unspecified")
        ):
            raise ValueError("Full-panel RGB training labels require a front-view RGB capture")
        image, image_bytes = image_from_bytes(image_bytes)
        power_loss_estimate = power_loss_estimator.estimate(image, camera_modality)
        triage_predictions = []
        advisory_predictions = []
        rear_view_only = camera_modality == "visible_rgb" and capture_view not in ("front", "unspecified")
        if camera_modality == "visible_rgb" and capture_view in ("front", "unspecified"):
            triage_predictions = classifier.predict(image)
        elif camera_modality == "visible_rgb_closeup":
            advisory_predictions = visible_crop_classifier.predict(image)
        elif camera_modality == "thermal_infrared":
            thermal_status = thermal_classifier.status()
            triage_predictions = (
                thermal_classifier.predict(image)
                if thermal_status.get("ready") and thermal_classifier.supports_input(image)
                else []
            )
        predictions = triage_predictions + advisory_predictions
        recommendation, reason = recommend(
            triage_predictions, electrical_test, panel_technology, confirmed_visual_label
        )
        recommended_route, route_reason = recommend_route(
            triage_predictions, electrical_test, panel_technology, confirmed_visual_label
        )
        if rear_view_only:
            detail = (
                f" This {capture_view.replace('_', ' ')} RGB capture was archived without applying the front-panel defect model."
            )
            route_reason = f"{route_reason}{detail} Human review is required."
            reason = f"{reason}{detail} Human review is required."
        if advisory_predictions:
            detail = (
                " Visible close-up model hints are research-only and were not used to calculate this route."
            )
            route_reason = f"{route_reason}{detail}"
            reason = f"{reason}{detail}"
        if camera_modality == "thermal_infrared":
            raptormaps_compatible = (
                thermal_classifier.status().get("ready") and thermal_classifier.supports_input(image)
            )
            if raptormaps_compatible:
                detail = (
                    " RaptorMaps thermal-crop prediction is research-only; it provides no field validation, "
                    "calibrated temperature, severity, or automated sort decision. Human review is required."
                )
            else:
                detail = (
                    " No thermal model accepted this image geometry; it was archived without inference. "
                    "Human review is required."
                )
            route_reason = f"{route_reason}{detail}"
            reason = f"{reason}{detail}"
        elif camera_modality == "visible_rgb_closeup":
            detail = (
                " This is a close-up research screen, not a full-panel inspection; verify defects and all sort decisions manually."
            )
            route_reason = f"{route_reason}{detail}"
            reason = f"{reason}{detail}"
        elif camera_modality != "visible_rgb":
            detail = (
                f"No validated {CAMERA_MODALITIES[camera_modality]} classifier is available; "
                "this image was archived without running the RGB model."
            )
            route_reason = f"{route_reason} {detail}"
            reason = f"{reason} {detail}"
        if panel_technology == "thin_film" and selected_route and selected_route != "LICENSED_THIN_FILM_HANDLER":
            raise ValueError("Thin-film modules must remain intact and use the licensed-handler route")
        if panel_technology == "thin_film" and chosen and chosen not in (
            "ROUTE_TO_LICENSED_HANDLER", "PENDING_REVIEW"
        ):
            raise ValueError("Thin-film modules must remain intact and be routed to a licensed handler")
        if chosen and chosen != recommendation and not reviewer_note:
            raise ValueError("Add a reviewer note when changing the recommended disposition")
        final_route = selected_route or recommended_route
        if final_route != recommended_route and not reviewer_note:
            raise ValueError("Add a reviewer note when changing the recommended sort route")
        if final_route == "STAGE_2_CSI" and (
            panel_technology != "c_si" or not stage2_isolation_confirmed or not reviewer_note
        ):
            raise ValueError("Stage 2 routing requires confirmed c-Si, a recorded isolation check, and a reviewer note")
        if chosen == "REUSE_CANDIDATE" and (recommended_route != "SECOND_LIFE_REVIEW" or final_route != "SECOND_LIFE_REVIEW"):
            raise ValueError("A second-life candidate requires a clean, documented electrical pass and matching sort route")
        if chosen == "REUSED":
            if recommended_route != "SECOND_LIFE_REVIEW" or final_route != "SECOND_LIFE_REVIEW":
                raise ValueError("Reuse requires the second-life review route; an image alone cannot approve reuse")
            if electrical_test != "pass" or not reviewer_note:
                raise ValueError("Final reuse requires a qualified electrical pass and a reviewer note")
        if chosen == "ROUTED_TO_STAGE_2" and (
            final_route != "STAGE_2_CSI" or panel_technology != "c_si" or not stage2_isolation_confirmed
        ):
            raise ValueError("Stage 2 routing requires confirmed c-Si and a recorded isolation check")
        if chosen == "SERVICE_AND_RETEST" and final_route != "SERVICE_AND_RETEST":
            raise ValueError("Service status requires the service-and-retest route")
        if chosen == "REPAIRED" and (final_route != "SERVICE_AND_RETEST" or electrical_test != "pass" or not reviewer_note):
            raise ValueError("Completed repair requires a documented service route, electrical retest, and reviewer note")
        if chosen == "ROUTE_TO_LICENSED_HANDLER" and final_route != "LICENSED_THIN_FILM_HANDLER":
            raise ValueError("Licensed-handler disposition requires the licensed thin-film route")
        final_disposition = chosen or "PENDING_REVIEW"
        decision_source = "manual" if chosen or selected_route else "triage_rules"
        return ledger.save_inspection(
            image_bytes=image_bytes,
            panel_id=panel_id,
            external_ref=external_ref,
            predictions=predictions,
            recommendation=recommendation,
            final_disposition=final_disposition,
            decision_source=decision_source,
            reason=reason,
            reviewer_note=reviewer_note,
            panel_technology=panel_technology,
            frame_width_mm=frame_width_mm,
            frame_height_mm=frame_height_mm,
            junction_box_location=junction_box_location,
            electrical_test=electrical_test,
            voltage=voltage,
            current=current,
            power=power,
            rated_power_w=rated_power_w,
            device_id=device_id,
            device_captured_at=device_captured_at,
            device_request_id=device_request_id,
            recommended_route=recommended_route,
            final_route=final_route,
            route_reason=route_reason,
            route_source=("manual" if selected_route else
                          "human_confirmed_label" if confirmed_visual_label else "triage_rules"),
            electrical_method=electrical_method,
            electrical_instrument=electrical_instrument,
            electrical_operator=electrical_operator,
            confirmed_visual_label=confirmed_visual_label,
            stage2_isolation_confirmed=stage2_isolation_confirmed,
            camera_modality=camera_modality,
            camera_sensor_id=camera_sensor_id,
            capture_group_id=capture_group_id,
            capture_view=capture_view,
            power_loss_estimate=power_loss_estimate,
        )

    def _read_json(self, max_bytes=MAX_IMAGE_BYTES * 2):
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as error:
            raise ValueError("Invalid request length") from error
        if length <= 0 or length > max_bytes:
            raise ValueError("Request is empty or too large")
        try:
            body = json.loads(self.rfile.read(length))
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise ValueError("Request body must be valid JSON") from error
        if not isinstance(body, dict):
            raise ValueError("Request body must be a JSON object")
        return body

    def _json(self, value, status=200):
        payload = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        try:
            self.wfile.write(payload)
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError):
            return

    def _file(self, path):
        if not path.is_file():
            return self._json({"error": "File not found"}, 404)
        data = path.read_bytes()
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format_string, *args):
        print(f"[EYE] {self.address_string()} - {format_string % args}")


def warm_models():
    for model in (classifier, thermal_classifier, visible_crop_classifier):
        model.status()


def main():
    parser = argparse.ArgumentParser(description="Run the Agastya-EYE local inspection app")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (default: localhost only)")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    device_token = os.environ.get("AGASTYA_DEVICE_TOKEN", "")
    if args.host not in ("127.0.0.1", "localhost", "::1") and not device_token:
        parser.error("Set AGASTYA_DEVICE_TOKEN before binding beyond localhost")
    if device_token and len(device_token) < 24:
        parser.error("AGASTYA_DEVICE_TOKEN must be at least 24 characters")
    server = ThreadingHTTPServer((args.host, args.port), EyeHandler)
    print(f"Agastya-EYE server listening at http://{args.host}:{args.port}; check /api/v1/health for readiness")
    threading.Thread(target=warm_models, name="eye-model-warmup", daemon=True).start()
    if arduino_config.enabled:
        threading.Thread(target=arduino_controller.connect, name="eye-arduino-connect", daemon=True).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nAgastya-EYE stopping")
    finally:
        server.server_close()
        arduino_controller.disconnect()
        print("Agastya-EYE stopped")


if __name__ == "__main__":
    main()
