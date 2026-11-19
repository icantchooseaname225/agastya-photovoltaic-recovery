"""Build machine-readable supplementary tables from Phase E processed outputs."""
from __future__ import annotations

import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
PHASE = BASE.parent
PROCESSED = PHASE / "Simulation_Campaign" / "processed"
APP = BASE / "Appendices"


def main():
    data = json.loads((PROCESSED / "PE-SIM-001_main_effect_variance.json").read_text(encoding="utf-8"))
    output = APP / "Appendix_B_Full_Main_Effects.csv"
    fields = ["metric", "rank", "factor", "levels", "sum_squares", "share_of_total_variance_pct", "level_means_json"]
    with output.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for metric, values in data["metrics"].items():
            for rank, effect in enumerate(values["main_effects"], start=1):
                writer.writerow({
                    "metric": metric,
                    "rank": rank,
                    "factor": effect["factor"],
                    "levels": effect["levels"],
                    "sum_squares": f"{effect['sum_squares']:.12g}",
                    "share_of_total_variance_pct": f"{effect['share_of_total_variance_pct']:.10g}",
                    "level_means_json": json.dumps(effect["level_means"], ensure_ascii=False),
                })
    print(f"Wrote full 21-row main-effect appendix: {output}")

    markdown = [
        "# Appendix B — Full main-effect results",
        "",
        "**Applies to:** PE-SIM-001; equal-weight decomposition of the 5,040-row archived scenario grid.",
        "**Interpretation:** Shares are design-grid variance shares, not probabilities or measured process uncertainty. Sum of squares use the squared units of each response. Display values are rounded; exact values and level means are retained in the CSV and JSON outputs.",
        "",
    ]
    for section, (metric, result) in enumerate(data["metrics"].items(), start=1):
        if section > 1:
            markdown.extend(["{{PAGEBREAK}}", ""])
        unit = "°C" if "temperature" in metric.lower() else "J m^(-2)"
        display_metric = metric.replace("⁻¹", "^(-1)").replace("⁻²", "^(-2)").replace("⁻³", "^(-3)")
        markdown.extend([
            f"## B{section}. {display_metric}",
            "",
            f"Response range in the scenario grid: {result['minimum']:.3f} to {result['maximum']:.3f} {unit}; equal-weight mean: {result['mean']:.3f} {unit}.",
            "",
            "| Factor | Main-effect share (%) | Sum of squares | Input level: marginal response mean (" + unit + ") |",
            "|---|---:|---:|---|",
        ])
        for effect in result["main_effects"]:
            factor = effect["factor"].replace("⁻¹", "^(-1)").replace("⁻²", "^(-2)").replace("⁻³", "^(-3)")
            means = "<br/>".join(
                f"{level}: {value:,.3f}"
                for level, value in effect["level_means"].items()
            )
            markdown.append(
                f"| {factor} | {effect['share_of_total_variance_pct']:.3f} | "
                f"{effect['sum_squares']:.6g} | {means} |"
            )
        markdown.extend([
            "",
            f"Unallocated interaction and residual share: {result['unallocated_interaction_and_residual_share_pct']:.3f}%.",
            "",
        ])
    markdown.extend([
        "## Reproducible source data",
        "",
        "Exact effect sums of squares, shares, factor levels and marginal means: `Appendix_B_Full_Main_Effects.csv` and `Simulation_Campaign/processed/PE-SIM-001_main_effect_variance.json`. The decomposition does not estimate interaction terms separately and assigns no probability distribution to any input.",
    ])
    md_output = APP / "Appendix_Main_Effect_Results.md"
    md_output.write_text("\n".join(markdown) + "\n", encoding="utf-8")
    print(f"Wrote print-source main-effect appendix: {md_output}")


if __name__ == "__main__":
    main()
