# Scenario and sensitivity analysis

| Source basis | Input | Ag per normalized 1 kg feed | Interpretation |
|---|---:|---:|---|
| Mulazzani et al. 2022 composition scenario | 300 ppm (0.03 wt%) | 0.300 g | Secondary-source scenario; source provenance and denominator need care. |
| Dias et al. 2016 study benchmark | 630 g/t | 0.630 g | Separate reported average; denominator is not resolved in accessible metadata. |

These values are not pooled and do not form a confidence interval or distribution. For feed mass M in kg and concentration C in ppm, initial Ag inventory (g) = M × C / 1000. Stage i output equals Stage i input Ag mass × measured recovery fraction. Product grade = 100 × product Ag mass / total product mass. Mass and silver residuals are distinct.

Unknown feed mass, stage recoveries, product mass, grade and balance residuals stay blank or symbolic. Feed mass scales inventory linearly after a real assay; it cannot determine the Ag in an output stream. Outputs: scenario_results_v2.csv, sensitivity_analysis_v2.csv and scenario_model_run_v2.json.

