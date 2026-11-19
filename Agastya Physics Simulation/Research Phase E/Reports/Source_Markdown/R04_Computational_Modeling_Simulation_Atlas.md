# Computational Modeling and Simulation Atlas

**Report ID:** AG-R04  
**Version:** 1.0 | **Prepared:** 13 October 2026  
**Reproducibility:** Scripts, data and result registers are retained in `Research Phase E/Simulation_Campaign/`.

## 1. Computational scope

AGASTYA's repository contains an older 147,912-row master dataset and a 52,168-row follow-up dataset, for 200,080 virtual records in total. The rows represent deterministic scenario calculations and thermal traces, not laboratory observations. The current Phase D accounting model adds normalized source arithmetic and a software self-check. Phase E adds two analyses on the optional thermal pretreatment: variance decomposition of the existing factorial grid and a spatially refined finite-volume heat-transfer model with a targeted timestep study. No external multiphysics solver was installed or authenticated for this work.

## 2. Simulation directory and identifiers

| ID | Question | Execution | Main result |
|---|---|---|---|
| HIST-SIM-001 | What do legacy scenario calculations produce under their inputs? | Executed | 200,080 virtual/scenario records; no physical samples |
| HIST-S3-THERM | What temperature/energy does the five-node assumed thermal model predict? | Executed | 5,040 summaries plus time traces; energy residual near numerical precision; no physical validation |
| PH-D-ACCOUNTING | Do normalized source conversions/accounting equations run? | Executed | Separate 0.300, 0.600 and 0.630 g/kg reference cases; synthetic fixture checks formulas only |
| PE-SIM-001 | Which factors dominate variation across the thermal factorial grid? | Executed | Dwell and contact conductance rank highest for EVA/cell peak and contact energy |
| PE-SIM-002 | Does spatial resolution change modeled local temperatures? | Executed | 20 cases across 4 conditions and 5 meshes; peak EVA rises with refinement |
| PE-SIM-003 | Is the 80-node result sensitive to timestep? | Executed | 1.0/0.5/0.25 ms at nominal/high-bound conditions; numerical check, not validation |
| PE-SIM-STAGE3 | Can separator trajectories and Ag recovery be predicted? | Blocked | No AGASTYA geometry, particle properties, field, charge or assays |
| PE-SIM-INTEGRATED | Can total process recovery/energy be predicted? | Blocked | Feed, stream measurements, validated assays, operation settings and energy data absent |

The full machine-readable register is `Simulation_Register.csv`.

## 3. Historical thermal model

Source: `Agastya_Physics_Simulation_2026-10-10.py`. The model uses a five-node areal thermal resistance/capacitance network for glass, front EVA, cell, rear EVA, and backsheet. It uses explicit Euler at 5 ms in the principal sweep and combines conduction, an algebraic blade/interface heat split, and front/back convection/radiation. It evaluates two material-property sets and sweeps tool temperature, contact conductance and duration, ambient temperature, EVA thickness, and interfacial resistance. The model outputs temperatures, time above set thresholds, integrated contact energy per assumed area, and numerical energy residual.

The historical procedures report a 5 ms baseline and an eight-condition four-timestep comparison from 10 to 1.25 ms; the largest peak-EVA difference from the finest timestep in that study was 0.154541 °C. This checks time integration for the reduced equations only. The 1,944 time traces belong to a subset, not a spatial field solution.

## 4. Phase E experiment PE-SIM-001

The analysis reads the 5,040 `thermal_case_summary` records from `EXP-S3-02` using a CSV DictReader, preserving row alignment. It calculates for each factor `SS_factor = Σ_g n_g(mean_g − mean)^2` and divides by total sum of squares. The balanced full-factorial design makes these one-way main-effect components orthogonal; the unallocated remainder includes interactions. Scenario levels receive equal weight. No distributions or Monte Carlo assumptions are used.

Peak EVA temperature's largest shares are dwell 41.50%, contact conductance 35.82%, and blade setpoint 3.57%. Peak cell temperature's are dwell 51.29%, contact conductance 21.85%, and ambient 2.74%. Contact energy's are dwell 55.20%, contact conductance 19.71%, and blade setpoint 2.02%. The result shows sensitivity within the grid, not uncertainty in real contact conditions.

## 5. Phase E finite-volume model PE-SIM-002

The new mesh subdivides the same five material layers uniformly into 1, 2, 4, 8 or 16 control volumes per layer. It preserves the original layer properties, total layer thicknesses, interfacial resistance, front/back surface losses, and zero-capacitance algebraic blade node. Internal control volumes exchange heat by center-to-center conduction. The model is intentionally a spatial refinement of the same one-dimensional model form, not a new validated representation of a machine.

An initial explicit-Euler 0.5 ms run diverged as the mesh was refined. The estimated row-sum ratio at 16 subdivisions reached 544.65; the cause is the small heat capacity and high conductivity of the thin silicon control volumes. The unstable output is retained. The production refinement switched to backward Euler and iterated the nonlinear radiation boundary condition to a fixed point. At one control volume per layer, its output reproduces the original model at the same nominal timestep within 0.0044 °C for peak cell temperature; the contact-energy difference is 42.5 J m^(-2) (approximately 0.018% in the nominal case). Maximum absolute energy residual across the spatial runs is below 6.3e-10% of modeled contact energy.

The contact-side EVA peak changed from 79.98 to 104.25 °C in the nominal case and from 247.27 to 276.05 °C in the high-bound case between 1 and 16 cells per layer. This is meaningful model-resolution sensitivity. It does not show that those temperatures occur in actual equipment or imply delamination quality.

## 6. Verification, validation and reproduction

Verification performed: CSV row count/filter checks; one-cell limiting-case comparison; areal energy balance; explicit stability diagnosis; spatial refinement; and timestep comparison for nominal/high-bound cases. Validation against external measurements: none. Mesh convergence is assessed against a 16-cell-per-layer numerical reference; timestep convergence uses the 0.25 ms run as a numerical reference. A numerical reference is not physical truth.

Run with the bundled Python runtime or a Python environment containing NumPy, pandas and Pillow:

```powershell
python .\models\run_phase_e_experiments.py
```

The script imports the historical model and reads its master CSV at the fixed project path. Raw failed outputs are kept under `raw/`; processed CSV/JSON are under `processed/`; 300 dpi plot exports are under `figures/`. Python, NumPy, pandas and Pillow versions are recorded in `processed/phase_e_experiment_summary.json`.

## 7. Limitations

No temperature-dependent material properties, phase changes, EVA kinetics, heat of reaction, adhesion/fracture, moving knife, three-dimensional edge effects, clamping/contact pressure, tool heat capacity, machine energy, gas emissions, glass breakage or measured panel condition are modeled. The electrostatic model remains a specification only. No integrated silver-recovery simulation is identifiable from current evidence.

## 8. Appendices and supplementary data

The exact inherited layer properties, boundary assumptions, selected PE-SIM-002 case inputs, numerical equations and failed explicit-run rationale are retained in `Reports/Appendices/Appendix_Model_Inputs.md`. `Appendix_B_Full_Main_Effects.csv` contains all seven factor shares and level means for each tracked output. Complete spatial/timestep rows, runtime versions, failed raw output and reproduction code remain in the simulation campaign folders listed in the appendix README.
