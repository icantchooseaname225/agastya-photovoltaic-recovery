from __future__ import annotations

import csv
import json
import platform
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / "preliminary_material_inventory.csv"
OUTPUT = HERE / "reference_inventory_arithmetic.csv"
MANIFEST = HERE / "phase_b_accounting_run.json"


def mass_closure_residual(input_mass_kg: float, output_masses_kg: list[float], documented_loss_kg: float) -> float:
    """Residual = input - accounted outputs - documented losses."""
    return input_mass_kg - sum(output_masses_kg) - documented_loss_kg


def stage_recovery_percent(ag_target_kg: float, ag_input_kg: float) -> float:
    """Stage Ag recovery; inputs must be assay-derived Ag masses, not particle masses."""
    if ag_input_kg <= 0:
        raise ValueError("Ag mass entering a stage must be positive.")
    if ag_target_kg < 0:
        raise ValueError("Ag mass in target output cannot be negative.")
    return 100.0 * ag_target_kg / ag_input_kg


def silver_grade_percent(ag_mass_kg: float, concentrate_mass_kg: float) -> float:
    """Ag grade; requires concentrate Ag mass and total concentrate mass."""
    if concentrate_mass_kg <= 0:
        raise ValueError("Concentrate mass must be positive.")
    if ag_mass_kg < 0:
        raise ValueError("Ag mass cannot be negative.")
    return 100.0 * ag_mass_kg / concentrate_mass_kg


def main() -> None:
    with INPUT.open("r", encoding="utf-8-sig", newline="") as handle:
        source_rows = list(csv.DictReader(handle))

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in source_rows:
        grouped[row["scenario_id"]].append(row)

    results: list[dict[str, str]] = []
    for scenario_id, rows in sorted(grouped.items()):
        listed_kg = sum(float(row["reference_mass_kg_per_1kg"]) for row in rows)
        ag_rows = [row for row in rows if row["material"].lower() == "silver"]
        ag_kg = sum(float(row["reference_mass_kg_per_1kg"]) for row in ag_rows)
        ag_g = ag_kg * 1000.0
        ag_ppm = ag_kg * 1_000_000.0
        has_full_component_basis = scenario_id == "PUB-COMP-2022"
        basis_kg = 1.0
        residual = mass_closure_residual(basis_kg, [listed_kg], 0.0) if has_full_component_basis else None
        results.append({
            "scenario_id": scenario_id,
            "calculation_class": "CALCULATED_FROM_PUBLISHED_DATA",
            "normalized_basis_kg": f"{basis_kg:.6f}",
            "sum_of_registered_reference_rows_kg": f"{listed_kg:.9f}",
            "component_inventory_complete": "YES" if has_full_component_basis else "NO",
            "silver_reference_kg": f"{ag_kg:.9f}",
            "silver_reference_g": f"{ag_g:.6f}",
            "silver_reference_ppm": f"{ag_ppm:.3f}",
            "full_component_mass_closure_residual_kg": "" if residual is None else f"{residual:.9f}",
            "mass_closure_scope": "Full listed composition plus explicit unassigned remainder" if has_full_component_basis else "Ag benchmark only; full component balance not reported in source register",
            "uncertainty_distribution": "NOT_SPECIFIED",
            "physical_sample_count": "0",
            "stage_yields_applied": "NO",
            "solver_output": "NO",
            "source_reference": "; ".join(sorted({row["source"] for row in rows})),
        })

    fields = list(results[0].keys()) if results else []
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    manifest = {
        "run_id": "AGASTYA-PHASE-B-ACCOUNTING-001",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "model": "Deterministic literature-normalized inventory arithmetic; not a physics solver",
        "software": {
            "python": platform.python_version(),
            "dependencies": "Python standard library only",
            "numpy_used": False,
            "external_solver_used": False,
        },
        "input": INPUT.name,
        "outputs": [OUTPUT.name],
        "scenario_count": len(results),
        "physical_samples": 0,
        "stage_1_yield": None,
        "stage_2_liberation": None,
        "stage_3_partition": None,
        "stage_4_assay": None,
        "interpretation": "Values reproduce published normalized composition benchmarks only. They are not Agastya measurements, model predictions, recovery yields, or assay results.",
        "accounting_functions_defined": [
            "mass_closure_residual(input mass, outputs, documented loss)",
            "stage_recovery_percent(target-stream Ag mass, stage-input Ag mass)",
            "silver_grade_percent(concentrate Ag mass, total concentrate mass)",
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()