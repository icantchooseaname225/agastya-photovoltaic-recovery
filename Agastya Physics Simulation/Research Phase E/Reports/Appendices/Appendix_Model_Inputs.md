# Appendix A — Thermal model inputs and equations

**Applies to:** PE-SIM-001, PE-SIM-002 and PE-SIM-003.  
**Model boundary:** one-dimensional optional hot-knife pretreatment; no chemical conversion or measured AGASTYA feed.

## A1. Layer property sets inherited from the historical model

Values below are model inputs, not measurements of an AGASTYA module. The property labels are retained from the source script.

| Layer/property | Lizcano2024_A1 | Tomsic2025_Table1 | Unit |
|---|---:|---:|---|
| Glass conductivity | 1.80 | 1.40 | W m^(-1) K^(-1) |
| Glass density | 3,000 | 2,210 | kg m^(-3) |
| Glass heat capacity | 500 | 730 | J kg^(-1) K^(-1) |
| EVA conductivity | 0.35 | 0.34 | W m^(-1) K^(-1) |
| EVA density | 960 | 951 | kg m^(-3) |
| EVA heat capacity | 2,090 | 1,400 | J kg^(-1) K^(-1) |
| Silicon conductivity | 148 | 130 | W m^(-1) K^(-1) |
| Silicon density | 2,330 | 2,329 | kg m^(-3) |
| Silicon heat capacity | 677 | 700 | J kg^(-1) K^(-1) |
| Backsheet conductivity | 0.20 | 0.19 | W m^(-1) K^(-1) |
| Backsheet density | 1,200 | 1,430 | kg m^(-3) |
| Backsheet heat capacity | 1,250 | 1,550 | J kg^(-1) K^(-1) |
| Backsheet thickness | 0.10 | 0.34 | mm |

Fixed geometry: 3.2 mm front glass and 0.21 mm silicon cell. Total EVA thickness is 0.90 or 1.16 mm, split equally between front/rear half-layers. The thermal sweep uses interface resistance 0, 1e-4 or 5e-4 m² K W^(-1); blade contact conductance 100, 300, 1,000 or 3,000 W m^(-2) K^(-1); tool setpoint 180, 200, 220, 250 or 300 °C; ambient 15, 25 or 35 °C; and dwell 0.1, 0.25, 0.5, 1, 2, 5 or 10 s.

Outer surfaces use convection coefficient 8 W m^(-2) K^(-1) with emissivity 0.85 on the front and 0.93 at the rear. A single Stefan–Boltzmann constant is used. Properties are constant with temperature.

## A2. Governing equations

For control volume `i`, the sensible areal heat capacity is `C_i = rho_i cp_i dx_i` and

`C_i dT_i/dt = Σ_j G_ij(T_j - T_i) + q_i,blade - q_i,surface`.

Adjacent-center conductance is `G_ij = [dx_i/(2k_i) + dx_j/(2k_j) + R_int]^(-1)` across material interfaces. The zero-capacity blade/interface node is eliminated algebraically:

`T_if = (h_c T_tool + G_g T_g + G_e T_e)/(h_c + G_g + G_e)`.

Surface heat loss is `q_s = h(T_s - T_amb) + eps sigma[(T_s+273.15)^4-(T_amb+273.15)^4]`.

PE-SIM-001 uses the historical five-node explicit-Euler output data. PE-SIM-002 and PE-SIM-003 subdivide each material layer into finite volumes and use backward Euler with Picard iterations for the radiation boundary condition. Spatial meshes are 1, 2, 4, 8 and 16 volumes per layer; PE-SIM-002 uses 0.5 ms, and PE-SIM-003 compares 1.0, 0.5 and 0.25 ms on the 80-volume mesh.

## A3. Selected cases for spatial/timestep experiments

| Case | Tool (°C) | Contact h (W m^(-2) K^(-1)) | Dwell (s) | Ambient (°C) | EVA (mm) | Property set | Interface R (m² K W^(-1)) |
|---|---:|---:|---:|---:|---:|---|---:|
| low_short | 180 | 100 | 0.5 | 15 | 0.90 | Lizcano2024_A1 | 0 |
| nominal | 220 | 1,000 | 2 | 25 | 0.90 | Lizcano2024_A1 | 1e-4 |
| long_moderate | 250 | 300 | 5 | 25 | 1.16 | Tomsic2025_Table1 | 1e-4 |
| high_bound | 300 | 3,000 | 10 | 35 | 1.16 | Tomsic2025_Table1 | 5e-4 |

The labels identify the selected scenario only. They do not indicate experimentally determined low, nominal, or high operating limits.

## A4. Numerical checks and limitations

The first 0.5 ms explicit-Euler refinement is preserved in `Simulation_Campaign/raw/PE-SIM-002_failed_explicit_dt0p5ms.csv`. Its explicit row-sum stability ratio reached 544.65 at 16 volumes per layer and the solution diverged. The completed study uses backward Euler. One-volume-per-layer comparison and numerical heat balance are recorded in the processed results. Timestep sensitivity is checked only at nominal/high-bound cases. No physical validation, material loss, chemistry, delamination quality or machine energy is predicted.

## Reproducible artifacts

- Main analysis source: `Simulation_Campaign/models/run_phase_e_experiments.py`.
- Main-effect result and complete factor levels: `Simulation_Campaign/processed/PE-SIM-001_main_effect_variance.json` and `Appendix_B_Full_Main_Effects.csv`.
- Spatial data: `Simulation_Campaign/processed/PE-SIM-002_spatial_refinement.csv`.
- Timestep data: `Simulation_Campaign/processed/PE-SIM-003_timestep_refinement.csv`.
- Run environment: `Simulation_Campaign/processed/phase_e_experiment_summary.json`.
