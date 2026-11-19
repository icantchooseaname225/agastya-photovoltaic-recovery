from pathlib import Path
import csv

p = Path(__file__).resolve().parent
feed_g, feed_grade = 110.0, 0.75
conc_g, conc_grade = 3.11, 24.0
tail_g, tail_grade = 106.74, 0.019
feed_ag = feed_g * feed_grade / 100
conc_ag = conc_g * conc_grade / 100
tail_ag = tail_g * tail_grade / 100
rows = [
["SFF-01","Saffarian 2026 mean","110 × 0.75%","feed Ag mass",f"{feed_ag:.6f} g","reproduced","Prepared cell feed; not whole panel."],
["SFF-02","Saffarian 2026 mean","3.11 × 24.0%","concentrate Ag mass",f"{conc_ag:.6f} g","reproduced","Rounded mean values."],
["SFF-03","Saffarian 2026 mean","106.74 × 0.019%","tail Ag mass",f"{tail_ag:.7f} g","reproduced","Low tail assay is sensitive to rounding."],
["SFF-04","Saffarian 2026 mean","100 × (1 − tail Ag/feed Ag)","tail-depletion recovery",f"{100*(1-tail_ag/feed_ag):.4f}%","close to reported 97.55%","Rounded table means; study reports per-test calculations."],
["SFF-05","Saffarian 2026 mean","100 × concentrate Ag/feed Ag","ratio-of-means concentrate recovery",f"{100*conc_ag/feed_ag:.4f}%","does not reproduce reported mean","Diagnostic only; not a substitute for per-test metric."],
["SFF-06","Saffarian 2026 mean","100 × (concentrate Ag + tail Ag)/feed Ag","ratio-of-means Ag closure",f"{100*(conc_ag+tail_ag)/feed_ag:.4f}%","not reported as mean-row closure",f"Residual {feed_ag-conc_ag-tail_ag:.6f} g; raw replicate data needed."],
["SFF-07","Saffarian 2026 mean","110 − 3.11 − 106.74","total mass residual",f"{feed_g-conc_g-tail_g:.4f} g","rounded mean row","Separately averaged/rounded values."],
["SFF-08","Saffarian 2026 mean","24.0 / 0.75","ratio-of-means upgrade",f"{conc_grade/feed_grade:.2f}×","close to reported 32.2×","Mean of ratios can differ from ratio of mean assays."],
["COMP-01","Mulazzani 2022 scenario","1 kg × 300 ppm / 1,000,000","normalized inventory","0.300 g/kg","arithmetic only","Separate source basis; not AGASTYA assay."],
["DIAS-01","Dias 2016 benchmark","1 kg × 630 g/t","normalized inventory","0.630 g/kg","arithmetic only","Study-specific basis; not pooled with 300 ppm."],
]
with (p/"published_data_validation_v2.csv").open("w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f)
    w.writerow(["case_id","reference","equation","metric","reproduced_value","check","limitation"])
    w.writerows(rows)
print("Wrote published_data_validation_v2.csv with",len(rows),"calculation rows")
