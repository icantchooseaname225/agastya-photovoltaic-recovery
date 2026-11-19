#!/usr/bin/env python3
"""Fail-closed accounting and reference normalization for AGASTYA Phase D.

This script does not predict separation performance. Missing measurements stay
null. Literature reference conversions are explicitly separate from measured
process results. Only Python's standard library is required.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def ag_g_per_kg(value: float, unit: str) -> float:
    """Convert mass concentration to grams Ag per kilogram feed."""
    if unit == "mg_per_kg":
        return value / 1000.0
    if unit == "g_per_tonne":
        # One metric tonne is 1,000 kg.
        return value / 1000.0
    if unit == "g_per_kg":
        return value
    raise ValueError(f"Unsupported reference unit: {unit}")


def reference_inventory(data: dict[str, Any]) -> list[dict[str, Any]]:
    feed_mass = data.get("normalized_feed_mass_kg")
    if not is_number(feed_mass) or feed_mass <= 0:
        raise ValueError("normalized_feed_mass_kg must be a positive finite number")

    results = []
    for row in data.get("ag_grade_references", []):
        value, unit = row.get("value"), row.get("unit")
        if not is_number(value) or value < 0:
            raise ValueError(f"Invalid source value for {row.get('id')}")
        concentration = ag_g_per_kg(float(value), str(unit))
        results.append({
            "id": row.get("id"),
            "source_basis": row.get("source_basis"),
            "source_register_id": row.get("source_register_id"),
            "reported_value": value,
            "reported_unit": unit,
            "normalized_feed_mass_kg": float(feed_mass),
            "normalized_ag_inventory_g": concentration * float(feed_mass),
            "status": "normalized literature arithmetic; not AGASTYA measurement"
        })
    return results


def measured_process(data: dict[str, Any]) -> dict[str, Any]:
    process = data.get("measured_process", {})
    feed = process.get("feed", {})
    feed_mass = feed.get("mass_kg")
    feed_grade = feed.get("ag_grade_wt_percent")
    outputs = process.get("output_streams", [])
    target_id = process.get("target_stream_id")
    target = next((s for s in outputs if s.get("id") == target_id), None)

    result: dict[str, Any] = {
        "feed_ag_mass_g": None,
        "target_mass_yield_fraction": None,
        "target_ag_grade_wt_percent": None,
        "target_ag_recovery_fraction": None,
        "mass_balance_residual_kg": None,
        "ag_balance_residual_g": None,
        "output_stream_ag_mass_g": None,
        "status": "not calculable until measured feed/output masses and assays are supplied"
    }

    valid_feed = is_number(feed_mass) and feed_mass > 0 and is_number(feed_grade) and 0 <= feed_grade <= 100
    if valid_feed:
        feed_ag_g = float(feed_mass) * float(feed_grade) / 100.0 * 1000.0
        result["feed_ag_mass_g"] = feed_ag_g

        if target is not None:
            target_mass, target_grade = target.get("mass_kg"), target.get("ag_grade_wt_percent")
            if is_number(target_mass) and target_mass >= 0:
                result["target_mass_yield_fraction"] = float(target_mass) / float(feed_mass)
            if is_number(target_grade) and 0 <= target_grade <= 100:
                result["target_ag_grade_wt_percent"] = float(target_grade)
            if (is_number(target_mass) and target_mass >= 0 and
                    is_number(target_grade) and 0 <= target_grade <= 100):
                target_ag_g = float(target_mass) * float(target_grade) / 100.0 * 1000.0
                if feed_ag_g > 0:
                    result["target_ag_recovery_fraction"] = target_ag_g / feed_ag_g

        all_output_masses_known = bool(outputs) and all(
            is_number(s.get("mass_kg")) and s["mass_kg"] >= 0 for s in outputs
        )
        all_output_assays_known = bool(outputs) and all(
            is_number(s.get("ag_grade_wt_percent")) and 0 <= s["ag_grade_wt_percent"] <= 100
            for s in outputs
        )

        mass_loss = process.get("documented_mass_loss_kg")
        if all_output_masses_known and is_number(mass_loss) and mass_loss >= 0:
            result["mass_balance_residual_kg"] = (
                float(feed_mass) - sum(float(s["mass_kg"]) for s in outputs) - float(mass_loss)
            )

        ag_loss = process.get("documented_ag_loss_g")
        if all_output_masses_known and all_output_assays_known and is_number(ag_loss) and ag_loss >= 0:
            output_ag = sum(
                float(s["mass_kg"]) * float(s["ag_grade_wt_percent"]) / 100.0 * 1000.0
                for s in outputs
            )
            result["output_stream_ag_mass_g"] = output_ag
            result["ag_balance_residual_g"] = feed_ag_g - output_ag - float(ag_loss)

        if result["target_ag_recovery_fraction"] is not None:
            result["status"] = "calculated from supplied measured values; review QA/QC and closure before interpretation"
    return result


def build_results(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": data.get("schema_version", "unknown"),
        "run_label": data.get("run_label"),
        "model_scope": "stream accounting and reference unit conversion only; no separation physics",
        "normalized_literature_inventory": reference_inventory(data),
        "measured_agastya_process": measured_process(data),
        "interpretation": data.get("interpretation")
    }


def self_check() -> None:
    """Use a synthetic fixture to check arithmetic; never project evidence."""
    fixture = {
        "schema_version": "self-check",
        "run_label": "synthetic software fixture only",
        "normalized_feed_mass_kg": 1.0,
        "ag_grade_references": [
            {"id": "ppm", "source_basis": "fixture", "value": 300, "unit": "mg_per_kg"},
            {"id": "gt", "source_basis": "fixture", "value": 600, "unit": "g_per_tonne"}
        ],
        "measured_process": {
            "feed": {"mass_kg": 1.0, "ag_grade_wt_percent": 0.1},
            "output_streams": [
                {"id": "product", "mass_kg": 0.2, "ag_grade_wt_percent": 0.4},
                {"id": "tail", "mass_kg": 0.8, "ag_grade_wt_percent": 0.025}
            ],
            "documented_mass_loss_kg": 0.0,
            "documented_ag_loss_g": 0.0,
            "target_stream_id": "product"
        }
    }
    result = build_results(fixture)
    refs = result["normalized_literature_inventory"]
    metrics = result["measured_agastya_process"]
    assert math.isclose(refs[0]["normalized_ag_inventory_g"], 0.3, abs_tol=1e-12)
    assert math.isclose(refs[1]["normalized_ag_inventory_g"], 0.6, abs_tol=1e-12)
    assert math.isclose(metrics["target_mass_yield_fraction"], 0.2, abs_tol=1e-12)
    assert math.isclose(metrics["target_ag_grade_wt_percent"], 0.4, abs_tol=1e-12)
    assert math.isclose(metrics["target_ag_recovery_fraction"], 0.8, abs_tol=1e-12)
    assert math.isclose(metrics["mass_balance_residual_kg"], 0.0, abs_tol=1e-12)
    assert math.isclose(metrics["ag_balance_residual_g"], 0.0, abs_tol=1e-12)
    assert measured_process({"measured_process": {}})["feed_ag_mass_g"] is None
    print("Self-check passed: normalized conversions, synthetic balance formulas, and null propagation.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Input JSON; defaults to inputs/reference_inventory.json")
    parser.add_argument("--output", type=Path, help="Output JSON path; stdout if omitted")
    parser.add_argument("--self-check", action="store_true", help="Run synthetic formula checks only")
    args = parser.parse_args()

    if args.self_check:
        self_check()
        return

    default_input = Path(__file__).parent / "inputs" / "reference_inventory.json"
    input_path = args.input or default_input
    with input_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    results = build_results(data)
    serialized = json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    else:
        print(serialized, end="")


if __name__ == "__main__":
    main()
