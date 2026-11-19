from __future__ import annotations

import csv
import json
import math
import platform
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence_database_v2.csv"
OUT_SCENARIOS = ROOT / "scenario_results_v2.csv"
OUT_SENSITIVITY = ROOT / "sensitivity_analysis_v2.csv"
MANIFEST = ROOT / "scenario_model_run_v2.json"


def ppm_to_g_per_kg(ppm: float) -> float:
    if not math.isfinite(ppm) or ppm < 0 or ppm > 1_000_000:
        raise ValueError("ppm must be a finite value from 0 to 1,000,000")
    return ppm / 1000.0


def main() -> None:
    evidence_by_id = {}
    with EVIDENCE.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            evidence_by_id[row["Evidence ID"]] = row

    reference_cases = [
        {
            "scenario_id": "REF-COMP-2022-1KG",
            "evidence_id": "EV-007",
            "ppm": 300.0,
            "basis": "Review-reported 0.03 wt% composition scenario, normalized to 1 kg by prior project arithmetic",
            "note": "Secondary-source scenario; underlying composition provenance unresolved; not AGASTYA feed.",
        },
        {
            "scenario_id": "REF-DIAS-2016-1KG",
            "evidence_id": "EV-001",
            "ppm": 630.0,
            "basis": "Study-specific average module benchmark reported by Dias et al.; normalized to 1 kg only for arithmetic",
            "note": "Separate study benchmark; denominator relation to removed frame is not resolved; not AGASTYA feed.",
        },
    ]
    for case in reference_cases:
        if case["evidence_id"] not in evidence_by_id:
            raise ValueError(f"missing evidence ID {case['evidence_id']}")

    scenario_fields = [
        "scenario_id", "evidence_id", "calculation_class", "normalized_feed_mass_kg",
        "initial_silver_ppm", "silver_basis", "initial_silver_mass_g",
        "stage1_silver_in_g", "stage1_silver_out_g", "stage1_recovery_percent",
        "stage2_silver_in_g", "stage2_silver_out_g", "stage2_recovery_percent",
        "stage3_silver_in_g", "stage3_silver_out_g", "stage3_recovery_percent",
        "stage4_silver_in_g", "stage4_silver_out_g", "stage4_recovery_percent",
        "final_product_mass_g", "final_product_silver_grade_wt_percent",
        "total_mass_discrepancy_g", "silver_mass_discrepancy_g", "uncertainty",
        "physical_sample_count", "notes",
    ]
    scenario_rows = []
    for case in reference_cases:
        initial_g = ppm_to_g_per_kg(case["ppm"])
        scenario_rows.append({
            "scenario_id": case["scenario_id"],
            "evidence_id": case["evidence_id"],
            "calculation_class": "PUBLISHED_REFERENCE_NORMALIZED_ARITHMETIC",
            "normalized_feed_mass_kg": "1.000000",
            "initial_silver_ppm": f"{case['ppm']:.3f}",
            "silver_basis": case["basis"],
            "initial_silver_mass_g": f"{initial_g:.9f}",
            "stage1_silver_in_g": f"{initial_g:.9f}",
            "stage1_silver_out_g": "",
            "stage1_recovery_percent": "",
            "stage2_silver_in_g": "",
            "stage2_silver_out_g": "",
            "stage2_recovery_percent": "",
            "stage3_silver_in_g": "",
            "stage3_silver_out_g": "",
            "stage3_recovery_percent": "",
            "stage4_silver_in_g": "",
            "stage4_silver_out_g": "",
            "stage4_recovery_percent": "",
            "final_product_mass_g": "",
            "final_product_silver_grade_wt_percent": "",
            "total_mass_discrepancy_g": "",
            "silver_mass_discrepancy_g": "",
            "uncertainty": "NOT_AVAILABLE; no shared AGASTYA distribution",
            "physical_sample_count": "0",
            "notes": case["note"] + " Every process output and process recovery remains unknown.",
        })

    sensitivity_fields = [
        "parameter", "evidence_type_or_range_class", "defensible_numeric_input",
        "unit", "symbolic_relationship_or_calculation", "evaluated_result",
        "effect_on_conclusion", "limit",
    ]
    sensitivity_rows = [
        {
            "parameter": "Initial Ag concentration: review composition scenario",
            "evidence_type_or_range_class": "Published secondary-source reference scenario",
            "defensible_numeric_input": "300",
            "unit": "ppm in stated composition scenario",
            "symbolic_relationship_or_calculation": "Ag mass in g = feed mass kg x ppm / 1000",
            "evaluated_result": "0.300 g Ag per normalized 1 kg",
            "effect_on_conclusion": "Sets inventory arithmetic only; no process recovery follows",
            "limit": "Not pooled with Dias benchmark; source denominator and underlying provenance need confirmation",
        },
        {
            "parameter": "Initial Ag concentration: Dias study benchmark",
            "evidence_type_or_range_class": "Published study-specific experimental benchmark",
            "defensible_numeric_input": "630",
            "unit": "g/t, numerically ppm on the reported mass basis",
            "symbolic_relationship_or_calculation": "Ag mass in g = feed mass kg x ppm / 1000",
            "evaluated_result": "0.630 g Ag per normalized 1 kg",
            "effect_on_conclusion": "Sets a separate benchmark arithmetic only; no process recovery follows",
            "limit": "Not a distribution endpoint or interchangeable with the review scenario",
        },
        {
            "parameter": "Physical feed mass",
            "evidence_type_or_range_class": "Unconstrained unknown",
            "defensible_numeric_input": "",
            "unit": "kg",
            "symbolic_relationship_or_calculation": "Ag mass g = M x C / 1000, with M in kg and C in ppm",
            "evaluated_result": "Symbolic only",
            "effect_on_conclusion": "Linearly scales the initial inventory after an actual feed assay is available",
            "limit": "No AGASTYA panel or feed mass is documented",
        },
        {
            "parameter": "Stage 1 Ag retention or partition",
            "evidence_type_or_range_class": "Unconstrained unknown",
            "defensible_numeric_input": "",
            "unit": "fraction",
            "symbolic_relationship_or_calculation": "Ag after Stage 1 = Ag feed x r1; r1 requires measured stream assays",
            "evaluated_result": "Unknown",
            "effect_on_conclusion": "Could move Ag across the cell, ribbon and residue streams",
            "limit": "No Stage 1 masses or assays",
        },
        {
            "parameter": "Stage 2 Ag liberation/partition",
            "evidence_type_or_range_class": "Unconstrained unknown for AGASTYA; published values are study-specific",
            "defensible_numeric_input": "",
            "unit": "fraction",
            "symbolic_relationship_or_calculation": "Ag available to Stage 3 = Ag after Stage 1 x r2",
            "evaluated_result": "Unknown",
            "effect_on_conclusion": "Controls whether Ag-bearing contacts occur as separable particles",
            "limit": "Published size distributions are not transfer coefficients for AGASTYA",
        },
        {
            "parameter": "Particle size, shape, conductivity, charge and moisture",
            "evidence_type_or_range_class": "Unconstrained unknown for AGASTYA",
            "defensible_numeric_input": "",
            "unit": "multiple",
            "symbolic_relationship_or_calculation": "Stage 3 trajectory depends on field, charge-to-mass, particle geometry, drag, contact and feed rate",
            "evaluated_result": "No numerical solve",
            "effect_on_conclusion": "Could determine whether electrostatic separation is even physically selective",
            "limit": "No particle samples, characterization or separator geometry",
        },
        {
            "parameter": "Stage 3 Ag separation selectivity",
            "evidence_type_or_range_class": "Unconstrained unknown for AGASTYA",
            "defensible_numeric_input": "",
            "unit": "fraction or partition",
            "symbolic_relationship_or_calculation": "Ag recovery = Ag mass in target product / Ag mass entering Stage 3",
            "evaluated_result": "Unknown",
            "effect_on_conclusion": "Directly controls claimed silver recovery",
            "limit": "EV-003 reports co-concentration but not accessible mass-based Ag recovery",
        },
        {
            "parameter": "Stage losses and mass closure",
            "evidence_type_or_range_class": "Unconstrained unknown",
            "defensible_numeric_input": "",
            "unit": "kg or g",
            "symbolic_relationship_or_calculation": "Discrepancy = input mass - sum(all output streams) - documented losses",
            "evaluated_result": "Not calculable",
            "effect_on_conclusion": "Required for credible recovery and routing claims",
            "limit": "No measured AGASTYA stream masses",
        },
        {
            "parameter": "Assay and sampling uncertainty",
            "evidence_type_or_range_class": "Unconstrained unknown",
            "defensible_numeric_input": "",
            "unit": "method-specific",
            "symbolic_relationship_or_calculation": "Propagate validated assay, subsampling and mass uncertainties after method performance data exist",
            "evaluated_result": "Not calculable",
            "effect_on_conclusion": "Could change apparent grade, recovery and closure",
            "limit": "No lab, sampling design, method detection limit or replicate data",
        },
    ]

    with OUT_SCENARIOS.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=scenario_fields)
        writer.writeheader()
        writer.writerows(scenario_rows)
    with OUT_SENSITIVITY.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=sensitivity_fields)
        writer.writeheader()
        writer.writerows(sensitivity_rows)

    manifest = {
        "run_id": "AGASTYA-SCENARIO-MODEL-V2-001",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy_used": False,
        "model_class": "Deterministic reference arithmetic plus symbolic unknown-stage relationships",
        "evidence_input": EVIDENCE.name,
        "outputs": [OUT_SCENARIOS.name, OUT_SENSITIVITY.name],
        "normalized_scenarios": len(scenario_rows),
        "physical_samples": 0,
        "solver_run": False,
        "unknown_parameters_left_blank": True,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"wrote {len(scenario_rows)} reference scenarios and {len(sensitivity_rows)} sensitivity rows")


if __name__ == "__main__":
    main()
