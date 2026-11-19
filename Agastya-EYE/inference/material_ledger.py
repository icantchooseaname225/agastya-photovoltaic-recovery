"""Append-only material lineage and assay calculations for Agastya pilot runs."""

import hashlib
import json
import math
import re
import sqlite3
import uuid
from contextlib import closing
from pathlib import Path

from inference.ledger import canonical_json, utc_now


RECORD_TYPES = {"stream", "batch", "fraction", "sample"}
ROUTES = {"direct_comminution", "delamination"}
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,95}$")
ANALYTE_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,39}$")


class MaterialLedger:
    def __init__(self, database_path):
        self.database_path = Path(database_path)
        with closing(self._connect()) as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS material_journal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    record_id TEXT NOT NULL UNIQUE,
                    record_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    previous_hash TEXT,
                    record_hash TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS material_journal_type_idx
                    ON material_journal(record_type, id);
                CREATE TRIGGER IF NOT EXISTS material_journal_no_update
                    BEFORE UPDATE ON material_journal BEGIN
                    SELECT RAISE(ABORT, 'material records are append-only');
                END;
                CREATE TRIGGER IF NOT EXISTS material_journal_no_delete
                    BEFORE DELETE ON material_journal BEGIN
                    SELECT RAISE(ABORT, 'material records are append-only');
                END;
                """
            )

    def _connect(self):
        connection = sqlite3.connect(self.database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @staticmethod
    def _number(value, label, *, optional=False, positive=False, maximum=None):
        if value is None and optional:
            return None
        try:
            number = float(value)
        except (TypeError, ValueError) as error:
            raise ValueError(f"{label} must be a number") from error
        if not math.isfinite(number) or (number <= 0 if positive else number < 0):
            raise ValueError(f"{label} must be finite and {'positive' if positive else 'non-negative'}")
        if maximum is not None and number > maximum:
            raise ValueError(f"{label} must not exceed {maximum}")
        return number

    @staticmethod
    def _id(value, label):
        value = str(value or "").strip()
        if not ID_PATTERN.fullmatch(value):
            raise ValueError(f"{label} is required and must use letters, numbers, '.', '_', ':' or '-'")
        return value

    @staticmethod
    def _id_list(value, label, *, required=False, maximum=100):
        if not isinstance(value, list) or len(value) > maximum:
            raise ValueError(f"{label} must be a list with at most {maximum} IDs")
        result = []
        for item in value:
            item = MaterialLedger._id(item, label)
            if item in result:
                raise ValueError(f"{label} cannot contain duplicate IDs")
            result.append(item)
        if required and not result:
            raise ValueError(f"{label} must contain at least one ID")
        return result

    def _append(self, connection, record_id, record_type, payload):
        previous = connection.execute(
            "SELECT record_hash FROM material_journal ORDER BY id DESC LIMIT 1"
        ).fetchone()
        previous_hash = previous["record_hash"] if previous else None
        hash_payload = {
            "record_id": record_id,
            "record_type": record_type,
            "payload": payload,
            "previous_hash": previous_hash,
        }
        record_hash = hashlib.sha256(canonical_json(hash_payload).encode("utf-8")).hexdigest()
        connection.execute(
            "INSERT INTO material_journal (record_id, record_type, payload_json, previous_hash, record_hash) "
            "VALUES (?, ?, ?, ?, ?)",
            (record_id, record_type, canonical_json(payload), previous_hash, record_hash),
        )
        return {"record_id": record_id, "record_type": record_type, **payload,
                "previous_hash": previous_hash, "record_hash": record_hash}

    def _load(self, connection):
        rows = connection.execute("SELECT * FROM material_journal ORDER BY id").fetchall()
        records = []
        previous_hash = None
        for row in rows:
            payload = json.loads(row["payload_json"])
            hash_payload = {
                "record_id": row["record_id"],
                "record_type": row["record_type"],
                "payload": payload,
                "previous_hash": previous_hash,
            }
            actual = hashlib.sha256(canonical_json(hash_payload).encode("utf-8")).hexdigest()
            if row["previous_hash"] != previous_hash or row["record_hash"] != actual:
                raise ValueError(f"Material ledger integrity failure at {row['record_id']}")
            records.append({"record_id": row["record_id"], "record_type": row["record_type"],
                            **payload, "previous_hash": row["previous_hash"],
                            "record_hash": row["record_hash"]})
            previous_hash = row["record_hash"]
        return records

    def create_material_record(self, data):
        if not isinstance(data, dict):
            raise ValueError("Material record must be an object")
        allowed = {"record_id", "record_type", "parent_record_ids", "panel_ids", "stage_event_ids",
                   "material_label", "mass_g", "mass_basis", "size_min_mm", "size_max_mm",
                   "route_code", "operator_id", "instrument_id", "calibration_ref", "occurred_at", "note"}
        if set(data) - allowed:
            raise ValueError("Unsupported material fields: " + ", ".join(sorted(set(data) - allowed)))
        record_id = self._id(data.get("record_id") or f"MAT-{uuid.uuid4().hex[:12]}", "record_id")
        record_type = str(data.get("record_type", "")).strip().lower()
        if record_type not in RECORD_TYPES:
            raise ValueError("record_type must be stream, batch, fraction, or sample")
        parents = self._id_list(data.get("parent_record_ids", []), "parent_record_ids")
        panel_ids = self._id_list(data.get("panel_ids", []), "panel_ids")
        event_ids = self._id_list(data.get("stage_event_ids", []), "stage_event_ids")
        if record_type == "stream" and not (panel_ids or event_ids or parents):
            raise ValueError("A source stream must link a panel, stage event, or parent material record")
        if record_type in {"batch", "fraction"} and not parents:
            raise ValueError(f"A {record_type} must link at least one parent material record")
        label = str(data.get("material_label", "")).strip()
        if not label or len(label) > 120:
            raise ValueError("material_label is required and must be 120 characters or fewer")
        mass_g = self._number(data.get("mass_g"), "mass_g", positive=True)
        mass_basis = str(data.get("mass_basis", "dry")).strip().lower()
        if mass_basis not in {"dry", "wet"}:
            raise ValueError("mass_basis must be dry or wet")
        size_min = self._number(data.get("size_min_mm"), "size_min_mm", optional=True)
        size_max = self._number(data.get("size_max_mm"), "size_max_mm", optional=True)
        if size_min is not None and size_max is not None and size_min > size_max:
            raise ValueError("size_min_mm cannot exceed size_max_mm")
        route_code = data.get("route_code")
        if route_code is not None:
            route_code = str(route_code).strip().lower()
            if route_code not in ROUTES:
                raise ValueError("route_code must be direct_comminution or delamination")
        operator_id = self._id(data.get("operator_id"), "operator_id")
        instrument_id = str(data.get("instrument_id", "")).strip()
        calibration_ref = str(data.get("calibration_ref", "")).strip()
        for value, label_name in ((instrument_id, "instrument_id"), (calibration_ref, "calibration_ref")):
            if value and not ID_PATTERN.fullmatch(value):
                raise ValueError(f"{label_name} contains unsupported characters")
        note = str(data.get("note", "")).strip()
        if len(note) > 2000:
            raise ValueError("note must be at most 2,000 characters")
        payload = {
            "parent_record_ids": parents, "panel_ids": panel_ids, "stage_event_ids": event_ids,
            "material_label": label, "mass_g": mass_g, "mass_basis": mass_basis,
            "size_min_mm": size_min, "size_max_mm": size_max, "route_code": route_code,
            "operator_id": operator_id, "instrument_id": instrument_id,
            "calibration_ref": calibration_ref,
            "occurred_at": str(data.get("occurred_at") or utc_now()), "note": note,
        }
        with closing(self._connect()) as connection:
            try:
                connection.execute("BEGIN IMMEDIATE")
                records = {row["record_id"]: row for row in self._load(connection)}
                for parent in parents:
                    if parent not in records:
                        raise ValueError(f"Parent material record not found: {parent}")
                if record_type == "sample" and len(parents) != 1:
                    raise ValueError("An assay sample must have exactly one parent material record")
                allowed_parent_types = {
                    "stream": {"stream", "batch", "fraction"},
                    "batch": {"stream", "fraction"},
                    "fraction": {"stream", "batch", "fraction"},
                    "sample": {"stream", "batch", "fraction"},
                }
                if any(records[parent]["record_type"] not in allowed_parent_types[record_type]
                       for parent in parents):
                    raise ValueError(f"Invalid parent record type for {record_type}")
                for panel_id in panel_ids:
                    if not connection.execute("SELECT 1 FROM panels WHERE panel_id = ?", (panel_id,)).fetchone():
                        raise ValueError(f"Unknown panel_id: {panel_id}")
                for event_id in event_ids:
                    if not connection.execute("SELECT 1 FROM stage_events WHERE event_id = ?", (event_id,)).fetchone():
                        raise ValueError(f"Unknown stage_event_id: {event_id}")
                result = self._append(connection, record_id, record_type, payload)
                connection.commit()
                return result
            except Exception:
                connection.rollback()
                raise

    def create_assay(self, data):
        if not isinstance(data, dict):
            raise ValueError("Assay record must be an object")
        allowed = {"record_id", "sample_id", "analyte", "mass_fraction", "uncertainty_fraction",
                   "detection_limit_fraction", "method", "laboratory", "instrument_id",
                   "calibration_ref", "operator_id", "occurred_at", "note"}
        if set(data) - allowed:
            raise ValueError("Unsupported assay fields: " + ", ".join(sorted(set(data) - allowed)))
        record_id = self._id(data.get("record_id") or f"ASSAY-{uuid.uuid4().hex[:12]}", "record_id")
        sample_id = self._id(data.get("sample_id"), "sample_id")
        analyte = str(data.get("analyte", "")).strip().lower()
        if not ANALYTE_PATTERN.fullmatch(analyte):
            raise ValueError("analyte must be a simple lowercase identifier such as ag, intact_cell, or polymer")
        mass_fraction = self._number(data.get("mass_fraction"), "mass_fraction", maximum=1)
        uncertainty = self._number(data.get("uncertainty_fraction"), "uncertainty_fraction", optional=True, maximum=1)
        detection_limit = self._number(data.get("detection_limit_fraction"), "detection_limit_fraction", optional=True, maximum=1)
        for key in ("method", "laboratory", "instrument_id", "calibration_ref", "operator_id"):
            if not str(data.get(key, "")).strip():
                raise ValueError(f"{key} is required for assay provenance")
        payload = {
            "sample_id": sample_id, "analyte": analyte, "mass_fraction": mass_fraction,
            "uncertainty_fraction": uncertainty, "detection_limit_fraction": detection_limit,
            "method": str(data["method"]).strip(), "laboratory": str(data["laboratory"]).strip(),
            "instrument_id": self._id(data["instrument_id"], "instrument_id"),
            "calibration_ref": self._id(data["calibration_ref"], "calibration_ref"),
            "operator_id": self._id(data["operator_id"], "operator_id"),
            "occurred_at": str(data.get("occurred_at") or utc_now()),
            "note": str(data.get("note", "")).strip(),
        }
        with closing(self._connect()) as connection:
            try:
                connection.execute("BEGIN IMMEDIATE")
                records = {row["record_id"]: row for row in self._load(connection)}
                sample = records.get(sample_id)
                if not sample or sample["record_type"] != "sample":
                    raise ValueError("sample_id must refer to a recorded sample material")
                result = self._append(connection, record_id, "assay", payload)
                connection.commit()
                return result
            except Exception:
                connection.rollback()
                raise

    def create_run(self, data):
        if not isinstance(data, dict):
            raise ValueError("Process run must be an object")
        allowed = {"record_id", "route_code", "feed_record_ids", "output_record_ids", "target_output_ids",
                   "outputs_complete", "target_description", "energy_kwh", "duration_min", "cost_inr",
                   "operator_id", "instrument_id", "calibration_ref", "method", "receiver_status", "note"}
        if set(data) - allowed:
            raise ValueError("Unsupported process run fields: " + ", ".join(sorted(set(data) - allowed)))
        record_id = self._id(data.get("record_id") or f"RUN-{uuid.uuid4().hex[:12]}", "record_id")
        route_code = str(data.get("route_code", "")).strip().lower()
        if route_code not in ROUTES:
            raise ValueError("route_code must be direct_comminution or delamination")
        feeds = self._id_list(data.get("feed_record_ids"), "feed_record_ids", required=True)
        outputs = self._id_list(data.get("output_record_ids"), "output_record_ids", required=True)
        targets = self._id_list(data.get("target_output_ids", []), "target_output_ids")
        if not set(targets).issubset(outputs):
            raise ValueError("target_output_ids must be included in output_record_ids")
        outputs_complete = data.get("outputs_complete", False)
        if not isinstance(outputs_complete, bool):
            raise ValueError("outputs_complete must be a boolean")
        energy = self._number(data.get("energy_kwh"), "energy_kwh", optional=True)
        duration = self._number(data.get("duration_min"), "duration_min", optional=True)
        cost = self._number(data.get("cost_inr"), "cost_inr", optional=True)
        for key in ("operator_id", "instrument_id", "calibration_ref", "method"):
            if not str(data.get(key, "")).strip():
                raise ValueError(f"{key} is required to preserve run provenance")
        receiver_status = str(data.get("receiver_status", "unknown")).strip().lower()
        if receiver_status not in {"unknown", "accepted", "rejected", "not_applicable"}:
            raise ValueError("receiver_status must be unknown, accepted, rejected, or not_applicable")
        payload = {
            "route_code": route_code, "feed_record_ids": feeds, "output_record_ids": outputs,
            "target_output_ids": targets, "outputs_complete": outputs_complete,
            "target_description": str(data.get("target_description", "")).strip(),
            "energy_kwh": energy, "duration_min": duration, "cost_inr": cost,
            "operator_id": self._id(data["operator_id"], "operator_id"),
            "instrument_id": self._id(data["instrument_id"], "instrument_id"),
            "calibration_ref": self._id(data["calibration_ref"], "calibration_ref"),
            "method": str(data["method"]).strip(), "receiver_status": receiver_status,
            "note": str(data.get("note", "")).strip(), "occurred_at": utc_now(),
        }
        with closing(self._connect()) as connection:
            try:
                connection.execute("BEGIN IMMEDIATE")
                records = {row["record_id"]: row for row in self._load(connection)}
                for feed in feeds:
                    if feed not in records or records[feed]["record_type"] not in {"stream", "batch", "fraction"}:
                        raise ValueError(f"Feed must be an existing stream, batch, or fraction: {feed}")
                for output in outputs:
                    if output not in records or records[output]["record_type"] != "fraction":
                        raise ValueError(f"Run output must be an existing fraction: {output}")
                    if not set(records[output]["parent_record_ids"]).intersection(feeds):
                        raise ValueError(f"Output {output} must link to at least one run feed as a parent")
                for target in targets:
                    if records[target]["mass_basis"] != "dry":
                        raise ValueError("Target output masses must use dry basis")
                result = self._append(connection, record_id, "run", payload)
                connection.commit()
                return result
            except Exception:
                connection.rollback()
                raise

    def list_records(self):
        with closing(self._connect()) as connection:
            return self._load(connection)

    def get_run_report(self, run_id):
        records = self.list_records()
        by_id = {record["record_id"]: record for record in records}
        run = by_id.get(run_id)
        if not run or run["record_type"] != "run":
            return None
        assays = [record for record in records if record["record_type"] == "assay"]

        def grade_for(material_id, analyte):
            samples = [item for item in records if item["record_type"] == "sample"
                       and item["parent_record_ids"] == [material_id] and item["mass_basis"] == "dry"]
            sample_assays = [assay for assay in assays if assay["analyte"] == analyte
                             and assay["sample_id"] in {sample["record_id"] for sample in samples}]
            total_assayed_mass = sum(by_id[assay["sample_id"]]["mass_g"] for assay in sample_assays)
            if not sample_assays or total_assayed_mass <= 0:
                return None
            value = sum(by_id[assay["sample_id"]]["mass_g"] * assay["mass_fraction"]
                        for assay in sample_assays) / total_assayed_mass
            return {"mass_fraction": value, "assayed_sample_count": len(sample_assays),
                    "sample_mass_g": total_assayed_mass}

        feed_records = [by_id[item] for item in run["feed_record_ids"]]
        output_records = [by_id[item] for item in run["output_record_ids"]]
        feed_dry_complete = all(item["mass_basis"] == "dry" for item in feed_records)
        output_dry_complete = all(item["mass_basis"] == "dry" for item in output_records)
        feed_mass = sum(item["mass_g"] for item in feed_records) if feed_dry_complete else None
        output_mass = sum(item["mass_g"] for item in output_records) if output_dry_complete else None
        closure = (100 * output_mass / feed_mass if run["outputs_complete"] and feed_mass and output_mass is not None
                   else None)
        flags = []
        if not run["outputs_complete"]:
            flags.append("output inventory not declared complete; mass closure withheld")
        if not feed_dry_complete or not output_dry_complete:
            flags.append("mass basis is not dry for every feed/output; dry-basis calculations withheld")
        report = {
            "run_id": run_id, "route_code": run["route_code"], "target_description": run["target_description"],
            "feed_record_ids": run["feed_record_ids"], "output_record_ids": run["output_record_ids"],
            "target_output_ids": run["target_output_ids"], "feed_mass_g": feed_mass,
            "output_mass_g": output_mass, "mass_closure_percent": closure,
            "mass_closure_formula": "100 * sum(all declared dry output masses) / sum(dry feed masses)",
            "energy_kwh": run["energy_kwh"], "duration_min": run["duration_min"],
            "cost_inr": run["cost_inr"], "receiver_status": run["receiver_status"],
            "integrity": self.verify_integrity(records), "flags": flags,
        }
        if feed_mass and run["energy_kwh"] is not None:
            report["specific_energy_kwh_per_kg_feed"] = run["energy_kwh"] / (feed_mass / 1000)
            report["specific_energy_formula"] = "measured process energy (kWh) / dry feed mass (kg)"
        else:
            report["specific_energy_kwh_per_kg_feed"] = None
        if feed_mass and run["cost_inr"] is not None:
            report["cost_inr_per_kg_feed"] = run["cost_inr"] / (feed_mass / 1000)
        else:
            report["cost_inr_per_kg_feed"] = None

        target_records = [by_id[item] for item in run["target_output_ids"]]
        if run["route_code"] == "direct_comminution":
            feed_grades = [grade_for(item["record_id"], "ag") for item in feed_records]
            target_grades = [grade_for(item["record_id"], "ag") for item in target_records]
            target_mass = sum(item["mass_g"] for item in target_records) if all(
                item["mass_basis"] == "dry" for item in target_records) else None
            if all(feed_grades) and feed_mass:
                feed_ag_fraction = sum(item["mass_g"] * grade["mass_fraction"]
                                       for item, grade in zip(feed_records, feed_grades)) / feed_mass
            else:
                feed_ag_fraction = None
            if target_records and all(target_grades) and target_mass:
                target_ag_mass = sum(item["mass_g"] * grade["mass_fraction"]
                                     for item, grade in zip(target_records, target_grades))
                target_ag_fraction = target_ag_mass / target_mass
            else:
                target_ag_mass = target_ag_fraction = None
            feed_ag_mass = feed_mass * feed_ag_fraction if feed_mass is not None and feed_ag_fraction is not None else None
            report["route_metrics"] = {
                "target": "silver-bearing product fraction",
                "feed_ag_grade_percent": feed_ag_fraction * 100 if feed_ag_fraction is not None else None,
                "target_ag_grade_percent": target_ag_fraction * 100 if target_ag_fraction is not None else None,
                "target_ag_mass_g": target_ag_mass,
                "ag_recovery_percent": 100 * target_ag_mass / feed_ag_mass if target_ag_mass is not None and feed_ag_mass else None,
                "enrichment_ratio": target_ag_fraction / feed_ag_fraction if target_ag_fraction is not None and feed_ag_fraction else None,
                "formulas": {
                    "Ag grade (%)": "100 * assayed Ag mass fraction",
                    "Ag recovery (%)": "100 * (target dry mass * target Ag fraction) / (feed dry mass * feed Ag fraction)",
                    "enrichment": "target Ag mass fraction / feed Ag mass fraction",
                },
            }
            if feed_ag_fraction is None or target_ag_fraction is None:
                report["flags"].append("Ag grade/recovery/enrichment need dry-basis Ag assays on feed and selected outputs")
            if target_ag_mass is not None and run["cost_inr"] is not None and target_ag_mass > 0:
                report["route_metrics"]["cost_inr_per_kg_recovered_ag"] = run["cost_inr"] / (target_ag_mass / 1000)
            else:
                report["route_metrics"]["cost_inr_per_kg_recovered_ag"] = None
        else:
            feed_cell = [grade_for(item["record_id"], "intact_cell") for item in feed_records]
            output_cell = [grade_for(item["record_id"], "intact_cell") for item in target_records]
            feed_cell_mass = (sum(item["mass_g"] * grade["mass_fraction"]
                                  for item, grade in zip(feed_records, feed_cell))
                              if feed_mass is not None and all(feed_cell) else None)
            output_cell_mass = (sum(item["mass_g"] * grade["mass_fraction"]
                                    for item, grade in zip(target_records, output_cell))
                                if target_records and all(output_cell)
                                and all(item["mass_basis"] == "dry" for item in target_records) else None)
            polymer_grades = [grade_for(item["record_id"], "polymer") for item in target_records]
            target_mass = sum(item["mass_g"] for item in target_records) if target_records and all(
                item["mass_basis"] == "dry" for item in target_records) else None
            polymer_fraction = (sum(item["mass_g"] * grade["mass_fraction"]
                                    for item, grade in zip(target_records, polymer_grades)) / target_mass
                                if target_mass and all(polymer_grades) else None)
            report["route_metrics"] = {
                "target": "intact-cell-bearing product; separate from Route A silver target",
                "intact_cell_recovery_percent": 100 * output_cell_mass / feed_cell_mass
                if output_cell_mass is not None and feed_cell_mass else None,
                "target_residual_polymer_grade_percent": polymer_fraction * 100 if polymer_fraction is not None else None,
                "formulas": {
                    "intact-cell recovery (%)": "100 * target dry mass * target intact_cell fraction / (feed dry mass * feed intact_cell fraction)",
                    "residual polymer grade (%)": "100 * assayed polymer mass / assayed target product mass",
                },
            }
            if feed_cell_mass is None or output_cell_mass is None:
                report["flags"].append("intact-cell recovery requires dry-basis intact_cell assays on feed and selected outputs")
            if polymer_fraction is None:
                report["flags"].append("residual-polymer grade requires dry-basis polymer assays on selected outputs")
        return report

    @staticmethod
    def verify_integrity(records):
        previous_hash = None
        for record in records:
            payload = {key: value for key, value in record.items()
                       if key not in {"record_id", "record_type", "previous_hash", "record_hash"}}
            projection = {"record_id": record["record_id"], "record_type": record["record_type"],
                          "payload": payload, "previous_hash": previous_hash}
            digest = hashlib.sha256(canonical_json(projection).encode("utf-8")).hexdigest()
            if record["previous_hash"] != previous_hash or record["record_hash"] != digest:
                return {"status": "integrity_error", "verified_records": 0,
                        "error": f"Material record chain failed at {record['record_id']}"}
            previous_hash = record["record_hash"]
        return {"status": "verified", "verified_records": len(records), "error": None}
