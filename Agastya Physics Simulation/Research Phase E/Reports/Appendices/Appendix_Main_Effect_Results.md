# Appendix B — Full main-effect results

**Applies to:** PE-SIM-001; equal-weight decomposition of the 5,040-row archived scenario grid.
**Interpretation:** Shares are design-grid variance shares, not probabilities or measured process uncertainty. Sum of squares use the squared units of each response. Display values are rounded; exact values and level means are retained in the CSV and JSON outputs.

## B1. Peak EVA temperature (°C)

Response range in the scenario grid: 15.649 to 261.535 °C; equal-weight mean: 68.115 °C.

| Factor | Main-effect share (%) | Sum of squares | Input level: marginal response mean (°C) |
|---|---:|---:|---|
| Dwell (s) | 41.503 | 4.55428e+06 | 0.1: 32.618<br/>0.25: 40.810<br/>0.5: 49.848<br/>1.0: 60.454<br/>2.0: 72.674<br/>5.0: 96.710<br/>10.0: 123.693 |
| Contact conductance (W m^(-2) K^(-1)) | 35.824 | 3.93106e+06 | 100: 34.918<br/>300: 50.193<br/>1000: 79.710<br/>3000: 107.640 |
| Blade setpoint (°C) | 3.569 | 391681 | 180: 57.607<br/>200: 61.811<br/>220: 66.015<br/>250: 72.320<br/>300: 82.823 |
| Ambient (°C) | 1.906 | 209167 | 15: 60.225<br/>25: 68.115<br/>35: 76.005 |
| Total EVA thickness (mm) | 0.246 | 27034.9 | 0.9: 70.431<br/>1.16: 65.799 |
| Property set | 0.173 | 18953.1 | Lizcano2024_A1: 66.176<br/>Tomsic2025_Table1: 70.055 |
| Interface resistance (m² K W^(-1)) | 0.041 | 4536.92 | 0.0: 67.205<br/>0.0001: 67.717<br/>0.0005: 69.424 |

Unallocated interaction and residual share: 16.737%.

{{PAGEBREAK}}

## B2. Peak cell temperature (°C)

Response range in the scenario grid: 15.064 to 251.958 °C; equal-weight mean: 55.632 °C.

| Factor | Main-effect share (%) | Sum of squares | Input level: marginal response mean (°C) |
|---|---:|---:|---|
| Dwell (s) | 51.290 | 4.53547e+06 | 0.1: 26.046<br/>0.25: 29.407<br/>0.5: 35.250<br/>1.0: 44.314<br/>2.0: 56.853<br/>5.0: 83.484<br/>10.0: 114.074 |
| Contact conductance (W m^(-2) K^(-1)) | 21.847 | 1.93191e+06 | 100: 32.175<br/>300: 43.162<br/>1000: 64.054<br/>3000: 83.138 |
| Ambient (°C) | 2.742 | 242506 | 15: 47.137<br/>25: 55.632<br/>35: 64.128 |
| Blade setpoint (°C) | 2.231 | 197319 | 180: 48.172<br/>200: 51.158<br/>220: 54.143<br/>250: 58.618<br/>300: 66.070 |
| Total EVA thickness (mm) | 0.334 | 29576.2 | 0.9: 58.055<br/>1.16: 53.210 |
| Property set | 0.048 | 4207.4 | Lizcano2024_A1: 54.719<br/>Tomsic2025_Table1: 56.546 |
| Interface resistance (m² K W^(-1)) | 0.033 | 2936.09 | 0.0: 56.357<br/>0.0001: 55.963<br/>0.0005: 54.577 |

Unallocated interaction and residual share: 21.473%.

{{PAGEBREAK}}

## B3. Net contact energy (J m^(-2))

Response range in the scenario grid: 1379.740 to 1724155.200 J m^(-2); equal-weight mean: 214399.565 J m^(-2).

| Factor | Main-effect share (%) | Sum of squares | Input level: marginal response mean (J m^(-2)) |
|---|---:|---:|---|
| Dwell (s) | 55.198 | 2.65196e+14 | 0.1: 11,966.811<br/>0.25: 29,152.015<br/>0.5: 56,334.872<br/>1.0: 107,031.220<br/>2.0: 198,702.776<br/>5.0: 421,095.303<br/>10.0: 676,513.956 |
| Contact conductance (W m^(-2) K^(-1)) | 19.712 | 9.47062e+13 | 100: 50,150.761<br/>300: 127,054.501<br/>1000: 273,461.641<br/>3000: 406,931.355 |
| Blade setpoint (°C) | 2.022 | 9.71331e+12 | 180: 162,083.567<br/>200: 183,006.067<br/>220: 203,930.835<br/>250: 235,322.486<br/>300: 287,654.868 |
| Ambient (°C) | 0.076 | 3.66187e+11 | 15: 224,838.961<br/>25: 214,399.867<br/>35: 203,959.866 |
| Property set | 0.036 | 1.7532e+11 | Lizcano2024_A1: 220,297.508<br/>Tomsic2025_Table1: 208,501.621 |
| Interface resistance (m² K W^(-1)) | 0.002 | 1.19948e+10 | 0.0: 215,870.848<br/>0.0001: 215,059.047<br/>0.0005: 212,268.798 |
| Total EVA thickness (mm) | 0.001 | 3.53257e+09 | 0.9: 215,236.767<br/>1.16: 213,562.362 |

Unallocated interaction and residual share: 22.952%.

## Reproducible source data

Exact effect sums of squares, shares, factor levels and marginal means: `Appendix_B_Full_Main_Effects.csv` and `Simulation_Campaign/processed/PE-SIM-001_main_effect_variance.json`. The decomposition does not estimate interaction terms separately and assigns no probability distribution to any input.
