"""Source-qualified, normalized literature arithmetic; not a process simulation."""
from __future__ import annotations

import csv
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence_database_v2.csv"
OUT = ROOT / "scenario_results_v3.csv"
MANIFEST = ROOT / "scenario_model_run_v3.json"

CASES = [
    {
        "scenario_id": "REF-COMP-2022-300PPM-1KG",
        "evidence_id": "EV-007",
        "ppm": 300.0,
        "class": "SECONDARY_SOURCE_NORMALIZED_ARITHMETIC",
        "basis": "Review-reported 0.03 wt% composition scenario, normalized to 1 kg.",
        "note": "Underlying sample, denominator and provenance unresolved; not an AGASTYA feed assay.",
    },
    {
        "scenario_id": "REF-DIAS-2016-ABSTRACT-600GT-1KG",
        "evidence_id": "EV-001",
        "ppm": 600.0,
        "class": "PUBLISHER_ABSTRACT_NORMALIZED_ARITHMETIC",
        "basis": "Publisher abstract wording of 600 g/t, normalized to 1 kg for arithmetic only.",
        "note": "Separate study basis; denominator relation unresolved; not an AGASTYA feed assay.",
    },
    {
        "scenario_id": "REF-DIAS-2016-SECONDARY-630GT-1KG",
        "evidence_id": "EV-001",
        "ppm": 630.0,
        "class": "UNRESOLVED_SECONDARY_EXCERPT_ARITHMETIC",
        "basis": "Secondary conclusion excerpt reports 630 g/t; arithmetic shown only to preserve the discrepancy.",
        "note": "Not independently re-extracted from the full-text conclusion; do not use as a verified benchmark or AGASTYA feed assay.",
    },
]


def main() -> None:
    with EVIDENCE.open(encoding="utf-8-sig", newline="") as handle:
        ids = {row["Evidence ID"] for row in csv.DictReader(handle)}
    if any(case["evidence_id"] not in ids for case in CASES):
        raise ValueError("A scenario evidence ID is absent from evidence_database_v2.csv")

    fields = [
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
    output_rows = []
    for case in CASES:
        silver_g = case["ppm"] / 1000.0
        row = {field: "" for field in fields}
        row.update({
            "scenario_id": case["scenario_id"],
            "evidence_id": case["evidence_id"],
            "calculation_class": case["class"],
            "normalized_feed_mass_kg": "1.000000",
            "initial_silver_ppm": f"{case['ppm']:.3f}",
            "silver_basis": case["basis"],
            "initial_silver_mass_g": f"{silver_g:.9f}",
            "stage1_silver_in_g": f"{silver_g:.9f}",
            "uncertainty": "NOT_AVAILABLE; source basis unresolved or study-specific; no AGASTYA distribution",
            "physical_sample_count": "0",
            "notes": case["note"] + " All measured stage outputs, yields, recovery, grade, purity and mass-balance terms remain unknown.",
        })
        output_rows.append(row)

    with OUT.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output_rows)

    manifest = {
        "run_id": "AGASTYA-LITERATURE-ARITHMETIC-V3",
        "executed_utc": datetime.now(timezone.utc).isoformat(),
        "software": f"CPython {platform.python_version()} standard library",
        "script": Path(__file__).name,
        "input": EVIDENCE.name,
        "output": OUT.name,
        "model_class": "source-qualified normalized arithmetic; not a physics/chemistry solver or process simulation",
        "physical_samples": 0,
        "scenarios": [case["scenario_id"] for case in CASES],
        "process_stage_predictions": False,
        "limitations": [
            "300 ppm review composition scenario has unresolved source population and denominator provenance.",
            "Dias publisher abstract says 600 g/t; 630 g/t is retained only as an unresolved secondary-excerpt discrepancy.",
            "No Agastya panels, coupons, particles, assays, stream masses or separator inputs were provided.",
            "All stage outcomes, recovery, grade, purity, uncertainty and process mass balance are blank by design.",
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.name} with {len(output_rows)} source-qualified rows; no process physics was simulated.")


if __name__ == "__main__":
    main()
