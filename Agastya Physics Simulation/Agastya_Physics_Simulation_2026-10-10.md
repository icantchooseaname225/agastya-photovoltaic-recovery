# Agastya physics simulation and sensitivity sweep

> **Historical virtual model:** This report uses legacy stage numbering and assumed inputs. Its 200,080 records are scenarios/time histories, not experimental replicates. Conditional silver values depend on thesis/analyst assumptions; use the [current architecture crosswalk](Research%20Baseline/ARCHITECTURE_CROSSWALK_2026-10-10.md) and [source-qualified v3 arithmetic](Research%20Phase%20B-C/published_data_validation_v3.csv) for interpretation. No AGASTYA sample or recovery result is represented here.

**Generated:** 10 October 2026  
**Data file:** `Agastya_Physics_Simulation_2026-10-10.csv`  
**Reproducible model:** `Agastya_Physics_Simulation_2026-10-10.py`

## What was run

This is a first-principles and sensitivity simulation created because the existing Agastya browser walkthrough and Wokwi monitor are conceptual/UI demonstrations, not physics solvers. The run produced **147,912 rows**. It contains no physical trial observations; measured Agastya trial rows: **0**. The rows are deterministic parameter combinations and time-history outputs, not physical specimens or a Monte Carlo sample size. Every record carries an experiment ID and a procedure ID. See `experiment_register.csv` and `data_dictionary.csv` for the procedure index and column meanings. Follow-up virtual experiments are stored separately in `followup_virtual_experiments.csv` and described in `PROCEDURES_AND_RESULTS.md`.

## Programs and numerical method

The run uses **CPython 3.14.4** and **NumPy 2.5.3**. Python's built-in `csv` and `json` modules write the datasets and metadata; the standard library also supplies scenario enumeration and mathematical functions. Stage 3 uses a custom one-dimensional, five-node thermal resistance/capacitance model integrated with explicit forward Euler. Python/NumPy vectorize the batch calculation. No commercial finite-element, CFD, or process-simulation package was used. PowerShell was only the launch shell in this run; it did not calculate the physics.

| Block | Rows | What the rows contain |
|---|---:|---|
| Stage 2 manual mass balance | 384 | Frame/junction-box hand-off scenarios, Stage 3 feed mass, and idealized one-operator shift ceiling. |
| Stage 3 material balance | 1,152 | Glass and laminate output masses from a composition-based scenario sweep. |
| Stage 3 thermal transient summaries | 5,040 | Layer temperatures, heat input per assumed contact area, and time above comparison thresholds. |
| Stage 3 thermal time traces | 1,944 | 0.1 s snapshots for representative heating/cooling cases. |
| Stage 4 size-classification sensitivity | 129,024 | Fine/coarse mass split for a mass-weighted lognormal particle-size distribution across D50, spread and cut sizes. |
| Stage 4 literature Ag partition scenarios | 10,368 | Arithmetic scaling of published Ag-to-fines distributions, kept separate by source feed and method. |

## Main model boundaries

### Stage 2

Stage 2 follows the current project plan: a **supervised manual hand-off** after isolation, frame removal and junction-box/external-cable removal. Panel mass (10–30 kg), removable frame share (7–13 wt%), cable/J-box share (0.1–1 wt%) and elapsed manual time (2–15 minutes) are sensitivity inputs, not measured values. The 10 wt% central frame share comes from the thesis's composition graphic; the graphic's 1 wt% copper includes all panel wiring and cannot be treated as a measured junction-box share. The 8-hour capacity is an ideal arithmetic ceiling and excludes breaks, movement, inspection, jams, training and multiple operators.

The mass-balance rows conserve input mass by construction. They do not simulate electrical isolation, tool forces, manual labor variability, or the risks of handling damaged modules.

### Stage 3

The thermal run is a **one-dimensional, five-node transient thermal-resistance/capacitance model**: glass, front EVA, silicon cell, rear EVA and backsheet. It applies a fixed-temperature hot-knife contact at the glass/EVA interface, then calculates conduction through the layers plus natural convection and radiation at the two outer surfaces. It sweeps knife temperatures 180/200/220/250/300 °C; contact conductance 100/300/1,000/3,000 W m⁻² K⁻¹; assumed local dwell 0.1–10 s; ambient 15/25/35 °C; two total EVA thicknesses (0.90/1.16 mm); two literature property sets; and assumed interface thermal resistances 0/1×10⁻⁴/5×10⁻⁴ m² K W⁻¹. The 0.90 mm total uses the thesis's 2×0.45 mm; 1.16 mm interprets the literature table's 580 μm EVA (×2) as 0.58 mm per layer. Outer convection is fixed at an assumed 8 W m⁻² K⁻¹; emissivities are 0.85 (glass) and 0.93 (backsheet).

The materials-property sets follow tables from [Lizcano et al. (2024)](https://doi.org/10.1002/pip.3813) and [Tomšič et al. (2025)](https://doi.org/10.1002/adts.202401026). Project references for the hot-knife process and its limits are in [Stage 3 thermal development](../Build%20Files%20and%20Steps/Stage%203/STAGE3_THERMAL_DEVELOPMENT.md). Time above 100/140 °C is a comparison statistic, not a modeled peel result; EVA adhesion, viscoelastic fracture, and actual material-specific delamination strength are not modeled. The 280 °C time flag is only a comparison with reported TGA behavior for tested EVA ([Saitta et al. (2026)](https://doi.org/10.3390/green1010002)), not an operating limit or safety approval.

Thermal model outputs are **per square metre of assumed blade-contact area**. They are not electrical heater kWh per panel. The model excludes the heater/blade mass and control cycle, moving contact geometry, blade feed speed, full-panel heat distribution, latent heat, cross-linked EVA chemistry, damage, fumes, and quality scoring. Whole-panel hot-knife literature cycle times (about 50–60 s/module) do not define local contact dwell; the two quantities are kept separate.

### Stage 4

The Stage 4 mainline follows the latest project research decision: **contained comminution and dry size classification**, with ECS conditional on a characterized eligible feed. The size model assumes an overall *mass-weighted lognormal* particle-size distribution and computes the mass below each screen cut from its CDF. It sweeps assumed D50 values of 0.10–8 mm, geometric standard deviations of 1.4–2.8, and screen cuts of 0.25–2 mm. No Agastya crusher, feed particle-size distribution, component-specific liberation or sieve efficiency has been measured. Those rows predict only size mass partition, not Ag grade or recovery.

The separate Ag rows scale 70%, 80% and 94.12% source-reported Ag distributions to 10/20/30 g/panel scenario inputs. The reported distribution values come from different study feeds ([Sim et al. (2022)](https://doi.org/10.1016/j.wasman.2022.11.023); [Juyo Salazar et al. (2024)](https://doi.org/10.1016/j.susmat.2024.e01047)) and are **not a prediction of Agastya performance**. The 20 g/panel central input is from the thesis; 10 and 30 g are analyst sensitivity bounds. This arithmetic scenario allocates all assumed panel Ag to the modeled Stage 4 laminate; Stage 3 Ag partition is unknown and not simulated. Since product mass yield is unavailable, fine-fraction Ag grade is deliberately left blank. The conventional eddy-current mechanism is not numerically predicted: current feed is not demonstrated to be liberated conductive particles, and the project record does not provide the particle geometry, conductivity, magnetic-field map, rotor speed or splitter dimensions needed for a defensible trajectory model.

## Results range

- Stage 2 scenario Stage 3 feed mass: **8.600–27.870 kg/module**.
- Stage 3 peak modeled EVA-node temperature: **15.65–261.53 °C** across the swept interface conditions.
- Stage 3 net interface heat: **1379.7–1724155.2 J/m²** of assumed contact area.
- Stage 3 maximum absolute integrated energy-balance residual: **9.218e-12%**. Halving the 5 ms integration step changed peak EVA temperature by at most **0.009023 °C** on three representative checks.
- Stage 4 modeled fines mass fraction: **0.0000–1.0000** across assumed PSD/cut combinations. This large spread mainly shows the sensitivity to unknown post-comminution PSD; it is not an equipment performance interval.

The ranges describe parameter sweeps, not confidence intervals, likely operating windows, safe settings, or expected results. Do not use them as design approvals, safety limits, energy claims, or recovery forecasts. A parameter-combination count is not a physical sample size.

## Provisional conclusions about the process approaches

- **Stage 2:** retain supervised manual hand-off as the current baseline until panel/output weights and task time are measured. The 32–576 panels/shift range is an ideal arithmetic capacity ceiling, not a throughput estimate or automation case.
- **Stage 3:** use hot-knife front-glass separation as the instrumented coupon reference because it matches the current glass-plus-laminate process objective. The reduced model only maps assumed heat transfer; it cannot establish peel quality, select a setpoint, or verify EVA-free cells. The heated roller and heat reuse remain unverified.
- **Stage 4:** continue with contained comminution and dry classification as the measured-feed research path. The 0–1 fines range reflects the unknown PSD. Keep ECS conditional until the feed is characterized; no ECS performance was simulated.
- **Silver:** neither literature-normalized partition rows nor conditional grade arithmetic establishes Agastya grade or recovery. Measure Stage 3 silver partition, feed assay, fraction masses and product assays before making a recovery claim.

These are provisional development directions, not a validated process ranking or safety/design decision. See `PROCEDURES_AND_RESULTS.md` for the full scenario counts, physical sample-size statement and procedure-by-procedure conclusions.

## Reproduce

Run from the main Agastya folder with Python 3 and NumPy:

```powershell
python ".\Agastya Physics Simulation\Agastya_Physics_Simulation_2026-10-10.py"
```

The script regenerates the consolidated CSV and this report. A machine-readable run summary is in `Agastya_Physics_Simulation_2026-10-10_metadata.json`.

## Most useful real measurements to collect next

1. Stage 2: weigh one identified panel, removed frame, junction box/cables and Stage 3 hand-off; record actual supervised task time.
2. Stage 3: on supervisor-approved coupons, log blade temperature, interface temperature, contact geometry/feed speed, energy meter trace, force and output-quality scores. These measurements are needed to replace contact and loss assumptions.
3. Stage 4: obtain supervised/contained access, characterize the actual laminate feed PSD and dryness, retain and weigh every fraction, and assay representative feed/products. Do not add ECS unless the measured feed meets an accepted device envelope.

## Source notes

- Agastya Stage 2 manual and Stage 3 process boundaries: `../Build Files and Steps/Stage 3/STAGE3_BUILD_PLAN.md`, `../Build Files and Steps/Stage 3/STAGE3_THERMAL_DEVELOPMENT.md`, and `../04_Logbook/PROJECT_LOGBOOK_DAY_3_4.md`.
- Stage 3 material properties: [Lizcano et al., 2024](https://doi.org/10.1002/pip.3813), Table A1; [Tomšič et al., 2025](https://doi.org/10.1002/adts.202401026), Table 1.
- Stage 4 literature distribution values and interpretation: `../Build Files and Steps/Stage 4/STAGE4_METHOD_COMPARISON_AND_CALCULATIONS.md` and `../Build Files and Steps/Stage 4/STAGE4_RESEARCH_COMPLETION_BRIEF_2026-10-08.md`.
- The published 70/80 and 94.12% values are normalized distributions into the finest fraction, not product grade or purity. All Agastya-specific feed masses and material shares in this file remain unverified scenarios.

