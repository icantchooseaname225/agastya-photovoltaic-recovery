"""Append-only SQLite inspection ledger with per-panel tamper-evident passports."""

import hashlib
import json
import sqlite3
import uuid
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

from inference.estimation import calculate_panel_estimates
from inference.triage import sort_destination, sort_lane_decision


HASH_FIELDS = (
    "id", "panel_row_id", "panel_id", "created_at", "image_path",
    "image_sha256", "predictions_json", "recommended_disposition", "final_disposition",
    "decision_source", "decision_reason", "reviewer_note", "panel_technology",
    "frame_width_mm", "frame_height_mm", "junction_box_location", "electrical_test",
    "electrical_method", "electrical_instrument", "electrical_operator", "voltage",
    "current", "power", "device_id", "device_captured_at", "device_request_id",
    "recommended_route", "final_route", "route_reason", "route_source",
    "confirmed_visual_label", "stage2_isolation_confirmed", "previous_record_hash",
)
HASH_FIELDS_V13 = HASH_FIELDS + (
    "camera_modality", "camera_sensor_id", "capture_group_id", "hash_version",
)
HASH_FIELDS_V14 = HASH_FIELDS_V13 + ("rated_power_w", "power_loss_estimate_json")
HASH_FIELDS_V15 = HASH_FIELDS_V14 + ("capture_view",)
EVENT_HASH_FIELDS = (
    "id", "panel_row_id", "panel_id", "event_id", "stage_code", "event_type",
    "station_id", "occurred_at", "operator_id", "instrument_id", "calibration_ref",
    "measurements_json", "note", "previous_event_hash",
)


class EventConflictError(ValueError):
    """A station event conflicts with the recorded panel route or stage sequence."""


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


class Ledger:
    def __init__(self, database_path, image_root):
        self.database_path = Path(database_path)
        self.image_root = Path(image_root)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.image_root.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS panels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    panel_id TEXT UNIQUE,
                    external_ref TEXT UNIQUE,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS inspections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    panel_row_id INTEGER NOT NULL REFERENCES panels(id),
                    created_at TEXT NOT NULL,
                    image_path TEXT NOT NULL,
                    predictions_json TEXT NOT NULL,
                    recommended_disposition TEXT NOT NULL,
                    final_disposition TEXT NOT NULL,
                    decision_source TEXT NOT NULL,
                    decision_reason TEXT NOT NULL,
                    reviewer_note TEXT NOT NULL,
                    panel_technology TEXT NOT NULL DEFAULT 'unknown',
                    frame_width_mm REAL,
                    frame_height_mm REAL,
                    junction_box_location TEXT NOT NULL DEFAULT 'unknown',
                    electrical_test TEXT NOT NULL,
                    voltage REAL,
                    current REAL,
                    power REAL,
                    rated_power_w REAL,
                    power_loss_estimate_json TEXT NOT NULL DEFAULT '{}',
                    device_id TEXT,
                    device_captured_at TEXT,
                    device_request_id TEXT,
                    recommended_route TEXT NOT NULL DEFAULT 'HUMAN_REVIEW',
                    final_route TEXT NOT NULL DEFAULT 'HUMAN_REVIEW',
                    route_reason TEXT NOT NULL DEFAULT '',
                    route_source TEXT NOT NULL DEFAULT 'triage_rules',
                    electrical_method TEXT NOT NULL DEFAULT '',
                    electrical_instrument TEXT NOT NULL DEFAULT '',
                    electrical_operator TEXT NOT NULL DEFAULT '',
                    confirmed_visual_label TEXT,
                    stage2_isolation_confirmed INTEGER NOT NULL DEFAULT 0,
                    camera_modality TEXT NOT NULL DEFAULT 'visible_rgb',
                    camera_sensor_id TEXT NOT NULL DEFAULT 'unknown',
                    capture_group_id TEXT,
                    capture_view TEXT NOT NULL DEFAULT 'unspecified',
                    hash_version TEXT NOT NULL DEFAULT '1.2',
                    image_sha256 TEXT,
                    previous_record_hash TEXT,
                    record_hash TEXT
                );
                CREATE INDEX IF NOT EXISTS inspections_panel_idx ON inspections(panel_row_id, id DESC);
                CREATE TABLE IF NOT EXISTS stage_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    panel_row_id INTEGER NOT NULL REFERENCES panels(id),
                    event_id TEXT NOT NULL UNIQUE,
                    stage_code TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    station_id TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    operator_id TEXT NOT NULL,
                    instrument_id TEXT NOT NULL DEFAULT '',
                    calibration_ref TEXT NOT NULL DEFAULT '',
                    measurements_json TEXT NOT NULL,
                    note TEXT NOT NULL DEFAULT '',
                    previous_event_hash TEXT,
                    event_hash TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS stage_events_panel_idx ON stage_events(panel_row_id, id);
                """
            )
            columns = {row["name"] for row in connection.execute("PRAGMA table_info(inspections)")}
            for name, column_type in (
                ("device_id", "TEXT"),
                ("device_captured_at", "TEXT"),
                ("device_request_id", "TEXT"),
                ("panel_technology", "TEXT NOT NULL DEFAULT 'unknown'"),
                ("frame_width_mm", "REAL"),
                ("frame_height_mm", "REAL"),
                ("rated_power_w", "REAL"),
                ("power_loss_estimate_json", "TEXT NOT NULL DEFAULT '{}'"),
                ("junction_box_location", "TEXT NOT NULL DEFAULT 'unknown'"),
                ("recommended_route", "TEXT NOT NULL DEFAULT 'HUMAN_REVIEW'"),
                ("final_route", "TEXT NOT NULL DEFAULT 'HUMAN_REVIEW'"),
                ("route_reason", "TEXT NOT NULL DEFAULT ''"),
                ("route_source", "TEXT NOT NULL DEFAULT 'triage_rules'"),
                ("electrical_method", "TEXT NOT NULL DEFAULT ''"),
                ("electrical_instrument", "TEXT NOT NULL DEFAULT ''"),
                ("electrical_operator", "TEXT NOT NULL DEFAULT ''"),
                ("confirmed_visual_label", "TEXT"),
                ("stage2_isolation_confirmed", "INTEGER NOT NULL DEFAULT 0"),
                ("camera_modality", "TEXT NOT NULL DEFAULT 'visible_rgb'"),
                ("camera_sensor_id", "TEXT NOT NULL DEFAULT 'unknown'"),
                ("capture_group_id", "TEXT"),
                ("capture_view", "TEXT NOT NULL DEFAULT 'unspecified'"),
                ("hash_version", "TEXT NOT NULL DEFAULT '1.2'"),
                ("image_sha256", "TEXT"),
                ("previous_record_hash", "TEXT"),
                ("record_hash", "TEXT"),
            ):
                if name not in columns:
                    connection.execute(f"ALTER TABLE inspections ADD COLUMN {name} {column_type}")
            connection.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS inspections_device_request_idx "
                "ON inspections(device_request_id) WHERE device_request_id IS NOT NULL"
            )
            connection.executescript(
                """
                CREATE TRIGGER IF NOT EXISTS inspections_no_update
                BEFORE UPDATE ON inspections BEGIN
                    SELECT RAISE(ABORT, 'inspection records are append-only');
                END;
                CREATE TRIGGER IF NOT EXISTS inspections_no_delete
                BEFORE DELETE ON inspections BEGIN
                    SELECT RAISE(ABORT, 'inspection records are append-only');
                END;
                CREATE TRIGGER IF NOT EXISTS stage_events_no_update
                BEFORE UPDATE ON stage_events BEGIN
                    SELECT RAISE(ABORT, 'stage events are append-only');
                END;
                CREATE TRIGGER IF NOT EXISTS stage_events_no_delete
                BEFORE DELETE ON stage_events BEGIN
                    SELECT RAISE(ABORT, 'stage events are append-only');
                END;
                """
            )

    def _connect(self):
        connection = sqlite3.connect(self.database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def save_inspection(self, image_bytes, panel_id, external_ref, predictions, recommendation,
                        final_disposition, decision_source, reason, reviewer_note,
                        panel_technology, frame_width_mm, frame_height_mm, junction_box_location,
                        electrical_test, voltage, current, power, device_id=None,
                        device_captured_at=None, device_request_id=None,
                        recommended_route="HUMAN_REVIEW", final_route="HUMAN_REVIEW",
                        route_reason="", route_source="triage_rules", electrical_method="",
                        electrical_instrument="", electrical_operator="", confirmed_visual_label=None,
                        stage2_isolation_confirmed=False, camera_modality="visible_rgb",
                        camera_sensor_id="unknown", capture_group_id=None,
                        rated_power_w=None, power_loss_estimate=None,
                        capture_view="unspecified"):
        image_name = f"{uuid.uuid4().hex}.jpg"
        saved_path = None
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            if device_request_id:
                existing = connection.execute(
                    "SELECT id FROM inspections WHERE device_request_id = ?", (device_request_id,)
                ).fetchone()
                if existing:
                    connection.commit()
                    return self.get_inspection(existing["id"])
            if panel_id:
                panel = connection.execute(
                    "SELECT id, panel_id, external_ref FROM panels WHERE panel_id = ?", (panel_id,)
                ).fetchone()
                if panel is None:
                    raise ValueError(f"Panel {panel_id} does not exist in the ledger")
                if external_ref and panel["external_ref"] not in (None, external_ref):
                    raise ValueError("The selected panel already has a different asset reference")
                panel_row_id = panel["id"]
                panel_code = panel["panel_id"]
                asset_ref = panel["external_ref"] or external_ref
                if external_ref and panel["external_ref"] is None:
                    connection.execute("UPDATE panels SET external_ref = ? WHERE id = ?", (external_ref, panel_row_id))
            elif external_ref:
                panel = connection.execute(
                    "SELECT id, panel_id, external_ref FROM panels WHERE external_ref = ?", (external_ref,)
                ).fetchone()
                if panel:
                    panel_row_id, panel_code = panel["id"], panel["panel_id"]
                    asset_ref = panel["external_ref"]
                else:
                    cursor = connection.execute(
                        "INSERT INTO panels (panel_id, external_ref, created_at) VALUES (NULL, ?, ?)",
                        (external_ref, utc_now()),
                    )
                    panel_row_id = cursor.lastrowid
                    panel_code = f"PV-{panel_row_id:06d}"
                    asset_ref = external_ref
                    connection.execute("UPDATE panels SET panel_id = ? WHERE id = ?", (panel_code, panel_row_id))
            else:
                cursor = connection.execute(
                    "INSERT INTO panels (panel_id, external_ref, created_at) VALUES (NULL, NULL, ?)",
                    (utc_now(),),
                )
                panel_row_id = cursor.lastrowid
                panel_code = f"PV-{panel_row_id:06d}"
                asset_ref = None
                connection.execute("UPDATE panels SET panel_id = ? WHERE id = ?", (panel_code, panel_row_id))

            image_dir = self.image_root / panel_code
            image_dir.mkdir(parents=True, exist_ok=True)
            saved_path = image_dir / image_name
            saved_path.write_bytes(image_bytes)
            relative_path = (Path("images") / panel_code / image_name).as_posix()
            image_sha256 = hashlib.sha256(image_bytes).hexdigest()
            previous = connection.execute(
                "SELECT record_hash FROM inspections WHERE panel_row_id = ? AND record_hash IS NOT NULL ORDER BY id DESC LIMIT 1",
                (panel_row_id,),
            ).fetchone()
            previous_hash = previous["record_hash"] if previous else None
            next_id = connection.execute(
                "SELECT COALESCE((SELECT seq FROM sqlite_sequence WHERE name='inspections'), 0) + 1"
            ).fetchone()[0]
            record_values = {
                "id": next_id,
                "panel_row_id": panel_row_id,
                "panel_id": panel_code,
                "external_ref": asset_ref,
                "created_at": utc_now(),
                "image_path": relative_path,
                "image_sha256": image_sha256,
                "predictions_json": canonical_json(predictions),
                "recommended_disposition": recommendation,
                "final_disposition": final_disposition,
                "decision_source": decision_source,
                "decision_reason": reason,
                "reviewer_note": reviewer_note,
                "panel_technology": panel_technology,
                "frame_width_mm": frame_width_mm,
                "frame_height_mm": frame_height_mm,
                "junction_box_location": junction_box_location,
                "electrical_test": electrical_test,
                "electrical_method": electrical_method,
                "electrical_instrument": electrical_instrument,
                "electrical_operator": electrical_operator,
                "voltage": voltage,
                "current": current,
                "power": power,
                "rated_power_w": rated_power_w,
                "power_loss_estimate_json": canonical_json(power_loss_estimate or {}),
                "device_id": device_id,
                "device_captured_at": device_captured_at,
                "device_request_id": device_request_id,
                "recommended_route": recommended_route,
                "final_route": final_route,
                "route_reason": route_reason,
                "route_source": route_source,
                "confirmed_visual_label": confirmed_visual_label,
                "stage2_isolation_confirmed": int(bool(stage2_isolation_confirmed)),
                "camera_modality": camera_modality,
                "camera_sensor_id": camera_sensor_id,
                "capture_group_id": capture_group_id,
                "capture_view": capture_view,
                "hash_version": "1.5",
                "previous_record_hash": previous_hash,
            }
            for field in ("frame_width_mm", "frame_height_mm", "voltage", "current", "power", "rated_power_w"):
                if record_values[field] is not None:
                    record_values[field] = float(record_values[field])
            hash_projection = {key: record_values[key] for key in HASH_FIELDS_V15}
            record_hash = hashlib.sha256(canonical_json(hash_projection).encode("utf-8")).hexdigest()
            connection.execute(
                """INSERT INTO inspections (
                    id, panel_row_id, created_at, image_path, predictions_json,
                    recommended_disposition, final_disposition, decision_source,
                    decision_reason, reviewer_note, panel_technology, frame_width_mm,
                    frame_height_mm, junction_box_location, electrical_test, voltage,
                    current, power, rated_power_w, power_loss_estimate_json,
                    device_id, device_captured_at, device_request_id,
                    recommended_route, final_route, route_reason, route_source,
                    electrical_method, electrical_instrument, electrical_operator,
                    confirmed_visual_label, stage2_isolation_confirmed, camera_modality,
                    camera_sensor_id, capture_group_id, capture_view, hash_version, image_sha256,
                    previous_record_hash, record_hash
                ) VALUES (
                    :id, :panel_row_id, :created_at, :image_path, :predictions_json,
                    :recommended_disposition, :final_disposition, :decision_source,
                    :decision_reason, :reviewer_note, :panel_technology, :frame_width_mm,
                    :frame_height_mm, :junction_box_location, :electrical_test, :voltage,
                    :current, :power, :rated_power_w, :power_loss_estimate_json,
                    :device_id, :device_captured_at, :device_request_id,
                    :recommended_route, :final_route, :route_reason, :route_source,
                    :electrical_method, :electrical_instrument, :electrical_operator,
                    :confirmed_visual_label, :stage2_isolation_confirmed, :camera_modality,
                    :camera_sensor_id, :capture_group_id, :capture_view, :hash_version, :image_sha256,
                    :previous_record_hash, :record_hash
                )""",
                {**record_values, "record_hash": record_hash},
            )
            connection.commit()
        except Exception:
            connection.rollback()
            if saved_path:
                saved_path.unlink(missing_ok=True)
            raise
        finally:
            connection.close()
        return self.get_inspection(next_id)

    def append_stage_event(self, panel_id, event_id, stage_code, event_type, station_id,
                           occurred_at, operator_id, instrument_id, calibration_ref,
                           measurements, note):
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            existing = connection.execute(
                """SELECT e.*, p.panel_id FROM stage_events e
                   JOIN panels p ON p.id = e.panel_row_id WHERE e.event_id = ?""",
                (event_id,),
            ).fetchone()
            if existing:
                existing_event = self._stage_event_dict(existing)
                expected = {
                    "panel_id": panel_id,
                    "stage_code": stage_code,
                    "event_type": event_type,
                    "station_id": station_id,
                    "occurred_at": occurred_at,
                    "operator_id": operator_id,
                    "instrument_id": instrument_id,
                    "calibration_ref": calibration_ref,
                    "measurements": measurements,
                    "note": note,
                }
                if any(existing_event.get(key) != value for key, value in expected.items()):
                    raise EventConflictError("Event ID was already used for different event content")
                connection.commit()
                return existing_event, True

            panel = connection.execute(
                "SELECT id FROM panels WHERE panel_id = ?", (panel_id,)
            ).fetchone()
            if panel is None:
                raise ValueError(f"Panel {panel_id} does not exist in the material passport")
            panel_row_id = panel["id"]
            latest_inspection = connection.execute(
                """SELECT final_route, stage2_isolation_confirmed FROM inspections
                   WHERE panel_row_id = ? ORDER BY id DESC LIMIT 1""",
                (panel_row_id,),
            ).fetchone()
            completed_stages = {
                row["stage_code"] for row in connection.execute(
                    """SELECT stage_code FROM stage_events
                       WHERE panel_row_id = ? AND event_type = 'process_completed'""",
                    (panel_row_id,),
                )
            }
            if stage_code == "stage_2":
                if (latest_inspection is None or latest_inspection["final_route"] != "STAGE_2_CSI"
                        or not latest_inspection["stage2_isolation_confirmed"]):
                    raise EventConflictError(
                        "Stage 2 events require an EYE Stage 2 route and recorded isolation confirmation"
                    )
            elif stage_code == "stage_3" and "stage_2" not in completed_stages:
                raise EventConflictError("Stage 3 events require a recorded Stage 2 process completion")
            elif stage_code == "stage_4" and "stage_3" not in completed_stages:
                raise EventConflictError("Stage 4 events require a recorded Stage 3 process completion")

            previous = connection.execute(
                """SELECT event_hash FROM stage_events
                   WHERE panel_row_id = ? ORDER BY id DESC LIMIT 1""",
                (panel_row_id,),
            ).fetchone()
            previous_hash = previous["event_hash"] if previous else None
            next_id = connection.execute(
                "SELECT COALESCE((SELECT seq FROM sqlite_sequence WHERE name='stage_events'), 0) + 1"
            ).fetchone()[0]
            record = {
                "id": next_id,
                "panel_row_id": panel_row_id,
                "panel_id": panel_id,
                "event_id": event_id,
                "stage_code": stage_code,
                "event_type": event_type,
                "station_id": station_id,
                "occurred_at": occurred_at,
                "operator_id": operator_id,
                "instrument_id": instrument_id,
                "calibration_ref": calibration_ref,
                "measurements_json": canonical_json(measurements),
                "note": note,
                "previous_event_hash": previous_hash,
            }
            record["event_hash"] = hashlib.sha256(
                canonical_json({key: record[key] for key in EVENT_HASH_FIELDS}).encode("utf-8")
            ).hexdigest()
            connection.execute(
                """INSERT INTO stage_events (
                    id, panel_row_id, event_id, stage_code, event_type, station_id,
                    occurred_at, operator_id, instrument_id, calibration_ref,
                    measurements_json, note, previous_event_hash, event_hash
                ) VALUES (
                    :id, :panel_row_id, :event_id, :stage_code, :event_type, :station_id,
                    :occurred_at, :operator_id, :instrument_id, :calibration_ref,
                    :measurements_json, :note, :previous_event_hash, :event_hash
                )""",
                record,
            )
            connection.commit()
            return self._stage_event_dict(record), False
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def list_panels(self):
        with closing(self._connect()) as connection:
            rows = connection.execute(
                """SELECT p.panel_id, p.external_ref, p.created_at,
                          COUNT(i.id) AS inspection_count, MAX(i.created_at) AS last_inspected,
                          (SELECT final_disposition FROM inspections x WHERE x.panel_row_id = p.id ORDER BY x.id DESC LIMIT 1) AS last_disposition,
                          (SELECT final_route FROM inspections x WHERE x.panel_row_id = p.id ORDER BY x.id DESC LIMIT 1) AS last_route,
                          (SELECT panel_technology FROM inspections x WHERE x.panel_row_id = p.id ORDER BY x.id DESC LIMIT 1) AS last_panel_technology,
                          (SELECT frame_width_mm FROM inspections x WHERE x.panel_row_id = p.id ORDER BY x.id DESC LIMIT 1) AS frame_width_mm,
                          (SELECT frame_height_mm FROM inspections x WHERE x.panel_row_id = p.id ORDER BY x.id DESC LIMIT 1) AS frame_height_mm,
                          (SELECT rated_power_w FROM inspections x WHERE x.panel_row_id = p.id ORDER BY x.id DESC LIMIT 1) AS rated_power_w,
                          (SELECT junction_box_location FROM inspections x WHERE x.panel_row_id = p.id ORDER BY x.id DESC LIMIT 1) AS junction_box_location,
                          (SELECT COUNT(*) FROM stage_events s WHERE s.panel_row_id = p.id) AS stage_event_count,
                          (SELECT stage_code FROM stage_events s WHERE s.panel_row_id = p.id ORDER BY s.id DESC LIMIT 1) AS last_stage_code,
                          (SELECT event_type FROM stage_events s WHERE s.panel_row_id = p.id ORDER BY s.id DESC LIMIT 1) AS last_stage_event_type
                   FROM panels p LEFT JOIN inspections i ON i.panel_row_id = p.id
                   GROUP BY p.id ORDER BY COALESCE(MAX(i.created_at), p.created_at) DESC"""
            ).fetchall()
            return [dict(row) for row in rows]

    def list_inspections(self, limit=100):
        with closing(self._connect()) as connection:
            rows = connection.execute(
                """SELECT i.*, p.panel_id, p.external_ref FROM inspections i
                   JOIN panels p ON p.id = i.panel_row_id ORDER BY i.id DESC LIMIT ?""",
                (limit,),
            ).fetchall()
            return [self._inspection_dict(row) for row in rows]

    def get_inspection(self, inspection_id):
        with closing(self._connect()) as connection:
            row = connection.execute(
                """SELECT i.*, p.panel_id, p.external_ref FROM inspections i
                   JOIN panels p ON p.id = i.panel_row_id WHERE i.id = ?""",
                (inspection_id,),
            ).fetchone()
            return self._inspection_dict(row) if row else None

    def get_passport(self, panel_id):
        with closing(self._connect()) as connection:
            panel = connection.execute(
                "SELECT id, panel_id, external_ref, created_at FROM panels WHERE panel_id = ?",
                (panel_id,),
            ).fetchone()
            if panel is None:
                return None
            rows = connection.execute(
                """SELECT i.*, p.panel_id, p.external_ref FROM inspections i
                   JOIN panels p ON p.id = i.panel_row_id
                   WHERE i.panel_row_id = ? ORDER BY i.id""",
                (panel["id"],),
            ).fetchall()
            records = [dict(row) for row in rows]
            integrity = self._verify_records(records)
            event_rows = connection.execute(
                """SELECT e.*, p.panel_id FROM stage_events e
                   JOIN panels p ON p.id = e.panel_row_id
                   WHERE e.panel_row_id = ? ORDER BY e.id""",
                (panel["id"],),
            ).fetchall()
            events = [dict(row) for row in event_rows]
            return {
                "schema_version": "1.6",
                "workflow": "agastya_stage_1_eye",
                "panel": dict(panel),
                "inspection_count": len(rows),
                "integrity": integrity,
                "inspections": [self._inspection_dict(row) for row in rows],
                "stage_event_count": len(events),
                "event_integrity": self._verify_stage_events(events),
                "stage_events": [self._stage_event_dict(row) for row in events],
            }

    @staticmethod
    def _verify_stage_events(events):
        expected_previous = None
        integrity_error = None
        verified_events = 0
        for event in events:
            if event["previous_event_hash"] != expected_previous:
                integrity_error = f"Stage event {event['id']} has an unexpected previous-event hash"
                break
            projection = {key: event[key] for key in EVENT_HASH_FIELDS}
            actual_hash = hashlib.sha256(canonical_json(projection).encode("utf-8")).hexdigest()
            if actual_hash != event["event_hash"]:
                integrity_error = f"Stage event {event['id']} hash does not match its contents"
                break
            expected_previous = event["event_hash"]
            verified_events += 1
        return {
            "status": "integrity_error" if integrity_error else "verified",
            "verified_events": verified_events,
            "error": integrity_error,
        }

    @staticmethod
    def _stage_event_dict(row):
        if row is None:
            return None
        event = dict(row)
        event["measurements"] = json.loads(event.pop("measurements_json"))
        return event

    def _verify_records(self, records):
        expected_previous = None
        chain_started = False
        unverified_legacy_records = 0
        images_verified = 0
        integrity_error = None
        chain_start_id = None
        for record in records:
            if not record["record_hash"]:
                unverified_legacy_records += 1
                continue
            if not chain_started:
                chain_started = True
                chain_start_id = record["id"]
            if record["previous_record_hash"] != expected_previous:
                integrity_error = f"Inspection {record['id']} has an unexpected previous-record hash"
                break
            hash_version = record.get("hash_version") or "1.2"
            if hash_version not in ("1.2", "1.3", "1.4", "1.5"):
                integrity_error = f"Inspection {record['id']} uses unsupported hash version {hash_version}"
                break
            hash_fields = (
                HASH_FIELDS_V15 if hash_version == "1.5"
                else HASH_FIELDS_V14 if hash_version == "1.4"
                else HASH_FIELDS_V13 if hash_version == "1.3"
                else HASH_FIELDS
            )
            projection = {key: record[key] for key in hash_fields}
            actual_hash = hashlib.sha256(canonical_json(projection).encode("utf-8")).hexdigest()
            if actual_hash != record["record_hash"]:
                integrity_error = f"Inspection {record['id']} record hash does not match its contents"
                break
            image_path = (self.image_root / record["panel_id"] / Path(record["image_path"]).name).resolve()
            if not image_path.is_relative_to(self.image_root.resolve()) or not image_path.is_file():
                integrity_error = f"Inspection {record['id']} image is missing or outside the image store"
                break
            digest = hashlib.sha256(image_path.read_bytes()).hexdigest()
            if digest != record["image_sha256"]:
                integrity_error = f"Inspection {record['id']} image hash does not match its contents"
                break
            images_verified += 1
            expected_previous = record["record_hash"]

        if integrity_error:
            status = "integrity_error"
        elif unverified_legacy_records:
            status = "verified_with_legacy_records"
        else:
            status = "verified"
        return {
            "status": status,
            "verified_records": images_verified,
            "unverified_legacy_records": unverified_legacy_records,
            "chain_start_inspection_id": chain_start_id,
            "error": integrity_error,
        }

    def counts(self):
        with closing(self._connect()) as connection:
            panels = connection.execute("SELECT COUNT(*) FROM panels").fetchone()[0]
            inspections = connection.execute("SELECT COUNT(*) FROM inspections").fetchone()[0]
            labeled = connection.execute(
                "SELECT COUNT(*) FROM inspections WHERE confirmed_visual_label IS NOT NULL"
            ).fetchone()[0]
            return {"panels": panels, "inspections": inspections, "human_labeled_images": labeled}

    @staticmethod
    def _inspection_dict(row):
        if row is None:
            return None
        record = dict(row)
        record["predictions"] = json.loads(record.pop("predictions_json"))
        record["power_loss_estimate"] = json.loads(record.pop("power_loss_estimate_json", "{}"))
        record["inspection_estimates"] = calculate_panel_estimates(
            record.get("frame_width_mm"), record.get("frame_height_mm"),
            record.get("voltage"), record.get("current"), record.get("power"),
            record.get("rated_power_w"),
        )
        record["image_url"] = "/" + record["image_path"]
        record["sort_recommendation"] = {
            "route": record.get("recommended_route"),
            "destination": sort_destination(record.get("recommended_route")),
            "state": "RECOMMENDATION_ONLY",
            "actuator_commanded": False,
        }
        record["final_sort_destination"] = sort_destination(record.get("final_route"))
        record["sort_lane_decision"] = sort_lane_decision(
            record.get("final_route"),
            panel_technology=record.get("panel_technology", "unknown"),
            electrical_test=record.get("electrical_test", "not_tested"),
            stage2_isolation_confirmed=bool(record.get("stage2_isolation_confirmed")),
            confirmed_visual_label=record.get("confirmed_visual_label"),
        )
        return record
