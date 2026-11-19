"""Reproduce source-qualified arithmetic only; no AGASTYA sample data are used."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "published_data_validation_v3.csv"


def main() -> None:
    rows = []
    # Saffarian et al. table values are rounded means. These derived ratios are
    # diagnostics and must not be represented as replicate-level study means.
    feed_g, feed_grade = 110.0, 0.75
    conc_g, conc_grade = 3.11, 24.0
    tail_g, tail_grade = 106.74, 0.019
    feed_ag = feed_g * feed_grade / 100
    conc_ag = conc_g * conc_grade / 100
    tail_ag = tail_g * tail_grade / 100
    rows.extend([
        ["SFF-01", "Saffarian 2026 rounded mean", "110 × 0.75%", "feed Ag mass", f"{feed_ag:.6f} g", "reproduced", "Prepared cell feed; not whole panel."],
        ["SFF-02", "Saffarian 2026 rounded mean", "3.11 × 24.0%", "concentrate Ag mass", f"{conc_ag:.6f} g", "reproduced", "Rounded table means."],
        ["SFF-03", "Saffarian 2026 rounded mean", "106.74 × 0.019%", "tail Ag mass", f"{tail_ag:.7f} g", "reproduced", "Low tail assay is sensitive to rounding."],
        ["SFF-04", "Saffarian 2026 rounded mean", "100 × (1 − tail Ag/feed Ag)", "tail-depletion recovery", f"{100*(1-tail_ag/feed_ag):.4f}%", "close to reported 97.55%", "Rounded table means; source reports per-test calculations."],
        ["SFF-05", "Saffarian 2026 rounded mean", "100 × concentrate Ag/feed Ag", "ratio-of-means concentrate recovery", f"{100*conc_ag/feed_ag:.4f}%", "diagnostic only", "Not a substitute for the mean of replicate-level recovery."],
        ["SFF-06", "Saffarian 2026 rounded mean", "100 × (concentrate Ag + tail Ag)/feed Ag", "ratio-of-means Ag closure", f"{100*(conc_ag+tail_ag)/feed_ag:.4f}%", "diagnostic only", f"Residual {feed_ag-conc_ag-tail_ag:.7f} g; raw replicate data needed."],
        ["SFF-07", "Saffarian 2026 rounded mean", "110 − 3.11 − 106.74", "total mass residual", f"{feed_g-conc_g-tail_g:.4f} g", "rounded mean row", "Separately averaged/rounded values."],
        ["SFF-08", "Saffarian 2026 rounded mean", "24.0 / 0.75", "ratio-of-means upgrade", f"{conc_grade/feed_grade:.2f}×", "diagnostic only", "Mean of ratios can differ from ratio of mean assays."],
        ["COMP-01", "Mulazzani 2022 review scenario", "1 kg × 300 ppm / 1,000,000", "normalized inventory", "0.300 g/kg", "arithmetic only", "Secondary-source scenario; sample/denominator provenance unresolved; not AGASTYA assay."],
        ["DIAS-ABSTRACT-01", "Dias et al. 2016 publisher abstract", "1 kg × 600 g/t", "normalized inventory", "0.600 g/kg", "arithmetic only", "Publisher abstract wording; distinct study basis; not AGASTYA assay."],
        ["DIAS-EXCERPT-01", "Dias et al. 2016 secondary conclusion excerpt", "1 kg × 630 g/t", "normalized excerpt arithmetic", "0.630 g/kg", "unresolved source discrepancy", "630 g/t has not been independently re-extracted from the full-text conclusion; do not treat as verified input."],
    ])
    with OUTPUT.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(["case_id", "reference", "equation", "metric", "reproduced_value", "check", "limitation"])
        writer.writerows(rows)
    print(f"Wrote {OUTPUT.name}: {len(rows)} arithmetic rows; physical AGASTYA observations: 0")


if __name__ == "__main__":
    main()
