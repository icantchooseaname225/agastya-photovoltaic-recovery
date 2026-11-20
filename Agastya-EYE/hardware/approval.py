"""Explicit, single-use operator approval for Arduino gate releases."""

import hashlib
import hmac
import math
import sqlite3
import uuid
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

from inference.triage import MIN_CONFIDENCE, MIN_MARGIN

from .arduino_controller import (
    ArduinoServoController,
    HardwareError,
    HardwareProtocolError,
    HardwareUnavailableError,
)


class ApprovalError(RuntimeError):
    """An approval request was refused or could not be safely completed."""


class DuplicateApprovalError(ApprovalError):
    """An inspection already has a one-time release request."""


class IneligibleApprovalError(ApprovalError):
    """The inspection or operator confirmation does not meet release rules."""


def inspection_image_is_intact(record, *, project_root, image_root):
    """Check that a stored inspection image stays under images/ and matches its ledger hash."""
    if not record or not record.get("image_sha256"):
        return False
    relative_path = Path(str(record.get("image_path", "")))
    if not relative_path.parts or relative_path.parts[0] != "images":
        return False
    try:
        root = Path(image_root).resolve()
        image_path = (Path(project_root).resolve() / relative_path).resolve()
        if not image_path.is_relative_to(root) or not image_path.is_file():
            return False
        digest = hashlib.sha256()
        with image_path.open("rb") as image_file:
            for chunk in iter(lambda: image_file.read(1024 * 1024), b""):
                digest.update(chunk)
        return hmac.compare_digest(digest.hexdigest(), str(record["image_sha256"]))
    except (OSError, RuntimeError):
        return False


def release_eligibility(record, *, backend_ready, image_available, max_age_seconds=300, now=None):
    """Return a fail-closed eligibility result for a human-approved clean c-Si panel."""
    if not backend_ready:
        return {"eligible": False, "reason": "The backend, database, or RGB model is not ready"}
    if not record or not all(record.get(field) for field in ("id", "panel_id", "image_path", "image_sha256")):
        return {"eligible": False, "reason": "The inspection record is incomplete"}
    if not image_available:
        return {"eligible": False, "reason": "The original inspection image is unavailable"}

    try:
        created_at = datetime.fromisoformat(str(record.get("created_at", "")))
        if created_at.tzinfo is None:
            raise ValueError("Inspection time has no timezone")
        current_time = now or datetime.now(timezone.utc)
        age = (current_time - created_at.astimezone(timezone.utc)).total_seconds()
    except (TypeError, ValueError):
        return {"eligible": False, "reason": "The inspection timestamp is invalid"}
    if age < 0 or age > max_age_seconds:
        return {"eligible": False, "reason": "The inspection approval is stale; complete a fresh inspection"}

    if (record.get("camera_modality") != "visible_rgb"
            or record.get("capture_view") not in ("front", "unspecified")):
        return {"eligible": False, "reason": "Only a full-panel front-view RGB inspection can be released"}
    if (record.get("panel_technology") != "c_si"
            or record.get("recommended_route") != "SECOND_LIFE_REVIEW"
            or record.get("final_route") != "SECOND_LIFE_REVIEW"):
        return {"eligible": False, "reason": "The inspection does not have the approved second-life route"}
    if (record.get("final_disposition") != "REUSED"
            or record.get("confirmed_visual_label") != "clean"
            or not str(record.get("reviewer_note", "")).strip()):
        return {"eligible": False, "reason": "A human-reviewed clean result and final reuse approval are required"}
    if (record.get("electrical_test") != "pass"
            or not all(str(record.get(field, "")).strip() for field in (
                "electrical_method", "electrical_instrument", "electrical_operator"
            ))):
        return {"eligible": False, "reason": "A documented electrical pass is required"}
    try:
        voltage = float(record["voltage"])
        current = float(record["current"])
    except (KeyError, TypeError, ValueError):
        return {"eligible": False, "reason": "Recorded voltage and current readings are required for electrical approval"}
    if not math.isfinite(voltage) or not math.isfinite(current) or voltage < 0 or current < 0:
        return {"eligible": False, "reason": "Recorded voltage and current readings are invalid"}

    predictions = record.get("predictions")
    if not isinstance(predictions, list) or not predictions:
        return {"eligible": False, "reason": "A completed RGB inference result is required"}
    try:
        top_confidence = float(predictions[0]["confidence"])
        runner_up = float(predictions[1]["confidence"]) if len(predictions) > 1 else 0.0
    except (KeyError, TypeError, ValueError):
        return {"eligible": False, "reason": "The RGB inference result is incomplete"}
    if (predictions[0].get("label") != "clean"
            or top_confidence < MIN_CONFIDENCE
            or top_confidence - runner_up < MIN_MARGIN):
        return {"eligible": False, "reason": "The RGB result is uncertain or does not support a clean disposition"}
    return {"eligible": True, "reason": "Ready for a separate one-time operator release approval"}


class HardwareApprovalStore:
    """Append-only approval and command-event store separate from the inspection ledger."""

    EVENT_STATES = {"approved", "command_sent", "acknowledged", "closed_commanded", "uncertain", "failed"}
    TRANSITIONS = {
        "approved": {"command_sent", "failed"},
        "command_sent": {"acknowledged", "uncertain", "failed"},
        "acknowledged": {"closed_commanded", "uncertain"},
    }

    def __init__(self, database_path):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS release_requests (
                    command_id TEXT PRIMARY KEY,
                    inspection_id INTEGER NOT NULL UNIQUE,
                    panel_id TEXT NOT NULL,
                    approved_by TEXT NOT NULL,
                    approved_at TEXT NOT NULL,
                    duration_ms INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS release_events (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    command_id TEXT NOT NULL REFERENCES release_requests(command_id),
                    state TEXT NOT NULL CHECK(state IN (
                        'approved', 'command_sent', 'acknowledged', 'closed_commanded', 'uncertain', 'failed'
                    )),
                    occurred_at TEXT NOT NULL,
                    detail TEXT NOT NULL DEFAULT '',
                    acknowledgement TEXT NOT NULL DEFAULT ''
                );
                CREATE INDEX IF NOT EXISTS release_events_command_idx
                    ON release_events(command_id, sequence DESC);
                CREATE TRIGGER IF NOT EXISTS release_requests_no_update
                    BEFORE UPDATE ON release_requests BEGIN
                        SELECT RAISE(ABORT, 'hardware approvals are append-only');
                    END;
                CREATE TRIGGER IF NOT EXISTS release_requests_no_delete
                    BEFORE DELETE ON release_requests BEGIN
                        SELECT RAISE(ABORT, 'hardware approvals are append-only');
                    END;
                CREATE TRIGGER IF NOT EXISTS release_events_no_update
                    BEFORE UPDATE ON release_events BEGIN
                        SELECT RAISE(ABORT, 'hardware events are append-only');
                    END;
                CREATE TRIGGER IF NOT EXISTS release_events_no_delete
                    BEFORE DELETE ON release_events BEGIN
                        SELECT RAISE(ABORT, 'hardware events are append-only');
                    END;
                """
            )

    def _connect(self):
        connection = sqlite3.connect(self.database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @staticmethod
    def _utc_now():
        return datetime.now(timezone.utc).isoformat(timespec="seconds")

    def health_check(self):
        if not self.database_path.is_file():
            return {"healthy": False, "integrity": "missing"}
        try:
            uri = self.database_path.resolve().as_uri() + "?mode=ro"
            with closing(sqlite3.connect(uri, uri=True, timeout=1)) as connection:
                result = connection.execute("PRAGMA quick_check").fetchone()[0]
                foreign_key_issue = connection.execute("PRAGMA foreign_key_check").fetchone()
            return {"healthy": result == "ok" and foreign_key_issue is None,
                    "integrity": result if foreign_key_issue is None else "foreign_key_error"}
        except (OSError, sqlite3.Error) as error:
            return {"healthy": False, "integrity": "error", "message": f"{type(error).__name__}: {error}"}

    def create_request(self, command_id, inspection_id, panel_id, approved_by, duration_ms):
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "INSERT INTO release_requests VALUES (?, ?, ?, ?, ?, ?)",
                (command_id, inspection_id, panel_id, approved_by, self._utc_now(), duration_ms),
            )
            connection.execute(
                "INSERT INTO release_events (command_id, state, occurred_at) VALUES (?, 'approved', ?)",
                (command_id, self._utc_now()),
            )
            connection.commit()
        except sqlite3.IntegrityError as error:
            connection.rollback()
            raise DuplicateApprovalError("This inspection already has a release request") from error
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
        return self.get_by_inspection(inspection_id)

    def append_event(self, command_id, state, *, detail="", acknowledgement=""):
        if state not in self.EVENT_STATES:
            raise ValueError("Unknown hardware command event")
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            latest = connection.execute(
                "SELECT state FROM release_events WHERE command_id = ? ORDER BY sequence DESC LIMIT 1",
                (command_id,),
            ).fetchone()
            if latest is None or state not in self.TRANSITIONS.get(latest["state"], set()):
                raise ApprovalError("Invalid hardware command state transition")
            connection.execute(
                "INSERT INTO release_events (command_id, state, occurred_at, detail, acknowledgement) "
                "VALUES (?, ?, ?, ?, ?)",
                (command_id, state, self._utc_now(), str(detail)[:1000], str(acknowledgement)[:200]),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
        return self.get_by_command(command_id)

    def get_by_inspection(self, inspection_id):
        connection = self._connect()
        try:
            row = connection.execute(
                "SELECT * FROM release_requests WHERE inspection_id = ?", (inspection_id,)
            ).fetchone()
            return self._with_events(connection, row) if row else None
        finally:
            connection.close()

    def get_by_command(self, command_id):
        connection = self._connect()
        try:
            row = connection.execute(
                "SELECT * FROM release_requests WHERE command_id = ?", (command_id,)
            ).fetchone()
            return self._with_events(connection, row) if row else None
        finally:
            connection.close()

    @staticmethod
    def _with_events(connection, row):
        record = dict(row)
        events = connection.execute(
            "SELECT state, occurred_at, detail, acknowledgement FROM release_events "
            "WHERE command_id = ? ORDER BY sequence",
            (record["command_id"],),
        ).fetchall()
        record["events"] = [dict(event) for event in events]
        record["state"] = record["events"][-1]["state"] if record["events"] else "unknown"
        return record


class HardwareApprovalService:
    def __init__(self, controller, store, *, max_age_seconds=300):
        self.controller = controller
        self.store = store
        self.max_age_seconds = max_age_seconds

    def get_eligibility(self, record, *, backend_ready, image_available, now=None):
        if record and self.store.get_by_inspection(record.get("id")):
            return {"eligible": False, "reason": "This inspection already has a one-time release request"}
        if not self.controller.config.enabled:
            return {"eligible": False, "reason": "Hardware activation is disabled"}
        if not backend_ready:
            return {"eligible": False, "reason": "The backend, database, or RGB model is not ready"}
        if not self.store.health_check().get("healthy"):
            return {"eligible": False, "reason": "The hardware approval ledger is unavailable"}
        if not self.controller.is_ready():
            return {"eligible": False, "reason": self.controller.get_status()["message"]}
        return release_eligibility(
            record,
            backend_ready=backend_ready,
            image_available=image_available,
            max_age_seconds=self.max_age_seconds,
            now=now,
        )

    def connect(self):
        ready = self.controller.connect()
        return {"ready": ready, "hardware": self.controller.get_status()}

    def release(self, record, *, operator_id, panel_confirmation, backend_ready, image_available, now=None):
        if not self.controller.config.enabled:
            raise HardwareUnavailableError("Hardware activation is disabled")
        if not backend_ready:
            raise HardwareUnavailableError("The backend, database, or RGB model is not ready")
        if not record:
            raise IneligibleApprovalError("Inspection was not found")
        if self.store.get_by_inspection(record.get("id")):
            raise DuplicateApprovalError("This inspection already has a one-time release request")
        if not self.store.health_check().get("healthy"):
            raise HardwareUnavailableError("The hardware approval ledger is unavailable")
        eligibility = release_eligibility(
            record,
            backend_ready=backend_ready,
            image_available=image_available,
            max_age_seconds=self.max_age_seconds,
            now=now,
        )
        if not eligibility["eligible"]:
            raise IneligibleApprovalError(eligibility["reason"])
        operator = str(operator_id or "").strip()
        if not operator or len(operator) > 80:
            raise IneligibleApprovalError("Enter the approving operator ID (1 to 80 characters)")
        if str(panel_confirmation or "").strip() != str(record.get("panel_id", "")):
            raise IneligibleApprovalError("Type the exact panel ID to confirm this one-time release")
        if not self.controller.is_ready() and not self.controller.connect():
            raise HardwareUnavailableError(self.controller.get_status()["message"])

        command_id = uuid.uuid4().hex
        approval = self.store.create_request(
            command_id,
            int(record["id"]),
            str(record["panel_id"]),
            operator,
            self.controller.config.open_duration_ms,
        )
        self.store.append_event(command_id, "command_sent")
        try:
            result = self.controller.release_panel(command_id, self.controller.config.open_duration_ms)
        except Exception as error:
            release_started = self.controller.get_status().get("last_command_id") == command_id
            try:
                self.store.append_event(
                    command_id,
                    "uncertain" if release_started else "failed",
                    detail=f"{type(error).__name__}: {error}",
                )
            except Exception:
                pass
            if isinstance(error, HardwareError):
                raise
            raise HardwareProtocolError(f"Release result is uncertain: {error}") from error

        self.store.append_event(
            command_id,
            "acknowledged",
            acknowledgement=result.get("acknowledgement", ""),
        )
        approval = self.store.append_event(
            command_id,
            "closed_commanded",
            acknowledgement=result.get("close_acknowledgement", ""),
        )
        return {
            "approval": approval,
            "release": result,
            "physical_position_verified": False,
            "message": "Arduino acknowledged the release and timed close commands; no position sensor confirms physical servo motion.",
        }
