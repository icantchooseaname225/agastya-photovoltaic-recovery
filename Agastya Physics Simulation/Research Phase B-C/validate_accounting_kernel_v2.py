from __future__ import annotations

import csv
import importlib.util
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASELINE = ROOT.parent / "Research Baseline"
ORIGINAL_KERNEL = BASELINE / "stage4_accounting_kernel.py"


def _finite_number(value, name: str) -> float:
    if value is None or isinstance(value, bool):
        raise ValueError(f"{name} is missing or not numeric")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def ppm_to_mass_fraction(ppm: float) -> float:
    value = _finite_number(ppm, "ppm")
    if value < 0 or value > 1_000_000:
        raise ValueError("ppm must lie between 0 and 1,000,000")
    return value / 1_000_000.0


def mass_fraction_to_ppm(fraction: float) -> float:
    value = _finite_number(fraction, "mass fraction")
    if value < 0 or value > 1:
        raise ValueError("mass fraction must lie between 0 and 1")
    return value * 1_000_000.0


def percent_to_fraction(percent: float) -> float:
    value = _finite_number(percent, "percent")
    if value < 0 or value > 100:
        raise ValueError("percent must lie between 0 and 100")
    return value / 100.0


def fraction_to_percent(fraction: float) -> float:
    value = _finite_number(fraction, "fraction")
    if value < 0 or value > 1:
        raise ValueError("fraction must lie between 0 and 1")
    return value * 100.0


def silver_mass_kg(feed_mass_kg: float, ag_ppm: float) -> float:
    mass = _finite_number(feed_mass_kg, "feed mass")
    if mass < 0:
        raise ValueError("feed mass cannot be negative")
    return mass * ppm_to_mass_fraction(ag_ppm)


def stream_mass_sum(stream_masses_kg: list[float]) -> float:
    if stream_masses_kg is None:
        raise ValueError("stream masses are missing")
    values = [_finite_number(item, "stream mass") for item in stream_masses_kg]
    if any(item < 0 for item in values):
        raise ValueError("stream mass cannot be negative")
    return math.fsum(values)


def mass_balance_discrepancy_kg(
    input_mass_kg: float,
    output_masses_kg: list[float],
    documented_loss_kg: float,
    unit: str = "kg",
) -> float:
    if unit != "kg":
        raise ValueError("all masses must be normalized to kg before balance")
    input_mass = _finite_number(input_mass_kg, "input mass")
    loss = _finite_number(documented_loss_kg, "documented loss")
    if input_mass < 0 or loss < 0:
        raise ValueError("input mass and documented loss cannot be negative")
    return input_mass - stream_mass_sum(output_masses_kg) - loss


def stage_recovery_percent(ag_target_kg: float, ag_input_kg: float) -> float:
    target = _finite_number(ag_target_kg, "target-stream Ag mass")
    incoming = _finite_number(ag_input_kg, "stage-input Ag mass")
    if incoming <= 0:
        raise ValueError("recovery is undefined when stage-input Ag mass is zero")
    if target < 0 or target > incoming:
        raise ValueError("target Ag mass must be between zero and incoming Ag mass")
    return 100.0 * target / incoming


def silver_grade_percent(ag_mass_kg: float, concentrate_mass_kg: float) -> float:
    ag = _finite_number(ag_mass_kg, "concentrate Ag mass")
    total = _finite_number(concentrate_mass_kg, "concentrate total mass")
    if total <= 0:
        raise ValueError("grade is undefined when concentrate mass is zero")
    if ag < 0 or ag > total:
        raise ValueError("Ag mass must be between zero and total concentrate mass")
    return 100.0 * ag / total


def cumulative_recovery_percent(stage_recoveries_percent: list[float]) -> float:
    if stage_recoveries_percent is None or not stage_recoveries_percent:
        raise ValueError("stage recoveries are missing")
    return 100.0 * math.prod(percent_to_fraction(value) for value in stage_recoveries_percent)


def validate_streams(rows: list[dict]) -> list[str]:
    if rows is None:
        raise ValueError("stream rows are missing")
    seen: set[str] = set()
    warnings: list[str] = []
    for row in rows:
        stream_id = str(row.get("stream_id", "")).strip()
        destination = str(row.get("destination", "")).strip()
        if not stream_id:
            raise ValueError("stream identifier is missing")
        if stream_id in seen:
            raise ValueError(f"duplicate stream identifier: {stream_id}")
        seen.add(stream_id)
        if not destination:
            raise ValueError(f"destination is missing for {stream_id}")
        unit = row.get("unit", "")
        if unit != "kg":
            raise ValueError(f"mass unit for {stream_id} must be kg")
        mass = _finite_number(row.get("mass_kg"), f"{stream_id} mass")
        ag = _finite_number(row.get("ag_mass_kg"), f"{stream_id} Ag mass")
        if mass < 0 or ag < 0:
            raise ValueError(f"negative mass for {stream_id}")
        if ag > mass:
            raise ValueError(f"Ag mass exceeds total stream mass for {stream_id}")
    return warnings


def load_original_kernel():
    spec = importlib.util.spec_from_file_location("phase_a_accounting_kernel", ORIGINAL_KERNEL)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load the preserved Phase A kernel")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validation_cases() -> list[dict[str, str]]:
    cases: list[dict[str, str]] = []

    def add(case_id: str, area: str, expected: str, actual: str, passed: bool, note: str = "") -> None:
        cases.append({
            "case_id": case_id,
            "implementation": area,
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "note": note,
        })

    # Independent arithmetic identities for the preserved Phase A kernel.
    old = load_original_kernel()
    add(
        "ORIG-MASS-01",
        "Phase A mass residual",
        "1.0 - (0.2 + 0.3) - 0.1 = 0.4 kg",
        f"{old.mass_closure_residual(1.0, [0.2, 0.3], 0.1):.12g} kg",
        math.isclose(old.mass_closure_residual(1.0, [0.2, 0.3], 0.1), 0.4, rel_tol=0, abs_tol=1e-12),
    )
    add(
        "ORIG-REC-01",
        "Phase A recovery",
        "0.35 / 0.5 = 70%",
        f"{old.stage_recovery_percent(0.35, 0.5):.12g}%",
        math.isclose(old.stage_recovery_percent(0.35, 0.5), 70.0, rel_tol=0, abs_tol=1e-12),
    )
    add(
        "ORIG-GRADE-01",
        "Phase A grade",
        "0.2 / 1.0 = 20%",
        f"{old.silver_grade_percent(0.2, 1.0):.12g}%",
        math.isclose(old.silver_grade_percent(0.2, 1.0), 20.0, rel_tol=0, abs_tol=1e-12),
    )
    for case_id, fn, args, name in [
        ("ORIG-REC-OVER-100", old.stage_recovery_percent, (1.25, 1.0), "recovery >100%"),
        ("ORIG-GRADE-OVER-100", old.silver_grade_percent, (1.5, 1.0), "grade >100%"),
        ("ORIG-NAN", old.mass_closure_residual, (float("nan"), [], 0.0), "non-finite mass"),
    ]:
        rejected = False
        try:
            fn(*args)
        except (ValueError, TypeError):
            rejected = True
        add(
            case_id,
            "Phase A validation gap",
            f"reject {name}",
            "rejected" if rejected else "accepted/returned a value",
            rejected,
            "FAIL records missing guard in preserved Phase A implementation" if not rejected else "",
        )

    # Revised utility cases used for deterministic independent reproduction.
    for case_id, fn, args, expected, tol in [
        ("UNIT-PPM-300", ppm_to_mass_fraction, (300,), 0.0003, 1e-15),
        ("UNIT-PPM-630", ppm_to_mass_fraction, (630,), 0.00063, 1e-15),
        ("UNIT-MF-ROUNDTRIP", mass_fraction_to_ppm, (0.0003,), 300.0, 1e-12),
        ("UNIT-PCT-ROUNDTRIP", fraction_to_percent, (percent_to_fraction(25.0),), 25.0, 1e-12),
        ("UNIT-AG-MASS", silver_mass_kg, (1.0, 300), 0.0003, 1e-15),
        ("UNIT-RECOVERY", stage_recovery_percent, (0.35, 0.5), 70.0, 1e-12),
        ("UNIT-GRADE", silver_grade_percent, (0.2, 1.0), 20.0, 1e-12),
        ("UNIT-CUMULATIVE", cumulative_recovery_percent, ([80.0, 50.0],), 40.0, 1e-12),
    ]:
        actual = fn(*args)
        add(case_id, "Phase B/C independent arithmetic", str(expected), str(actual), math.isclose(actual, expected, rel_tol=0, abs_tol=tol))

    for case_id, fn, args, name in [
        ("UNIT-NEGATIVE-MASS", silver_mass_kg, (-1.0, 300), "negative mass"),
        ("UNIT-AG-OVER-100-PCT", stage_recovery_percent, (1.1, 1.0), "recovery above 100%"),
        ("UNIT-ZERO-INPUT-AG", stage_recovery_percent, (0.0, 0.0), "undefined recovery with zero Ag input"),
        ("UNIT-GRADE-OVER-100-PCT", silver_grade_percent, (2.0, 1.0), "Ag mass above total product mass"),
        ("UNIT-MISSING", ppm_to_mass_fraction, (None,), "missing concentration"),
        ("UNIT-NAN", ppm_to_mass_fraction, (float("nan"),), "non-finite concentration"),
        ("UNIT-INVALID-UNIT", mass_balance_discrepancy_kg, (1.0, [0.5], 0.0, "g"), "inconsistent unit"),
        ("UNIT-DUPLICATE-STREAM", validate_streams, ([{"stream_id":"x","destination":"a","mass_kg":1,"ag_mass_kg":0.1,"unit":"kg"},{"stream_id":"x","destination":"b","mass_kg":1,"ag_mass_kg":0.1,"unit":"kg"}],), "duplicate stream identifier"),
        ("UNIT-MISSING-DESTINATION", validate_streams, ([{"stream_id":"x","destination":"","mass_kg":1,"ag_mass_kg":0.1,"unit":"kg"}],), "missing stream destination"),
    ]:
        rejected = False
        try:
            fn(*args)
        except ValueError:
            rejected = True
        add(case_id, "Phase B/C input guard", f"reject {name}", "rejected" if rejected else "accepted", rejected)

    # Reproduce the two stored Phase A normalized reference values without rewriting them.
    with (BASELINE / "reference_inventory_arithmetic.csv").open(encoding="utf-8-sig", newline="") as handle:
        source = {row["scenario_id"]: row for row in csv.DictReader(handle)}
    checks = [("PUB-COMP-2022", 300.0, 0.3), ("DIAS-2016", 630.0, 0.63)]
    for scenario_id, ppm, grams in checks:
        row = source[scenario_id]
        actual_ppm = float(row["silver_reference_ppm"])
        actual_g = float(row["silver_reference_g"])
        ok = math.isclose(actual_ppm, ppm, abs_tol=1e-9) and math.isclose(actual_g, grams, abs_tol=1e-9)
        add(
            f"REFERENCE-{scenario_id}",
            "Read-only Phase A output reproduction",
            f"{ppm:g} ppm and {grams:g} g Ag per normalized kg",
            f"{actual_ppm:g} ppm and {actual_g:g} g",
            ok,
            "Separate literature scenarios; not a pooled estimate",
        )
    return cases


if __name__ == "__main__":
    results = validation_cases()
    fields = ["case_id", "implementation", "expected", "actual", "status", "note"]
    with (ROOT / "accounting_validation_results_v2.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)
    total = len(results)
    passed = sum(row["status"] == "PASS" for row in results)
    failed = total - passed
    print(f"validation rows={total}; pass={passed}; fail={failed}")
    for row in results:
        if row["status"] == "FAIL":
            print(f"FAIL {row['case_id']}: {row['note'] or row['actual']}")
