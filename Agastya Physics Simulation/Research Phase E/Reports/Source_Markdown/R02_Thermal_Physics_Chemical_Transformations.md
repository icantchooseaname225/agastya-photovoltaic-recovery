# Thermal Physics and Chemical Transformations

**Report ID:** AG-R02  
**Version:** 1.0 | **Prepared:** 13 October 2026  
**Scope note:** This is an optional hot-knife pretreatment investigation. Current AGASTYA Stage 3 is electrostatic separation.

## Executive finding

The legacy thermal model is a useful reduced heat-transfer scenario model, not a chemical-treatment model and not a validated delamination predictor. The existing 5,040-case sweep was reanalyzed, and a spatial finite-volume extension was executed on four representative input combinations. A first explicit-Euler refinement run diverged as the mesh was refined; the failed output is retained. Backward Euler with nonlinear-radiation iterations then produced finite results, exact reproduction of the original model for one control volume per layer, very small calculated energy residuals, and a clear mesh dependence in peak temperature. No experimental validation exists.

## 1. Mechanism boundary

Hot-knife delamination adds heat locally at the glass/encapsulant interface so the glass and cell-bearing laminate can be separated. This operation is physically distinct from furnace pyrolysis intended to degrade EVA. Frischknecht et al.'s IEA PVPS inventory describes the hot cutter as adding heat to EVA while separating glass from the cell/EVA laminate; the reported pilot process takes about 50 seconds per module, but that machine cycle is not a measured blade dwell time for the AGASTYA model. The same report treats later laminate processing and Ag/Cu recovery as further operations, outside its delamination unit boundary.

Thermal decomposition studies answer a different question. Tammaro et al. heated three c-Si panel samples in a furnace to 600 °C to fully degrade EVA and then examined mass losses and cell-surface composition ([2015 paper record](https://www.sciencedirect.com/science/article/pii/S0960148115001962)). Shang et al. compare encapsulant-dependent pollutant generation during thermal treatment and fit kinetic/emission models, but their abstract is not a hot-knife validation dataset ([2026 article](https://doi.org/10.1016/j.jece.2026.121479)). No kinetics parameters from these different regimes are imported into the AGASTYA heat-transfer model.

## 2. Historical five-node formulation

The model has five areal-capacitance nodes: cover glass, front EVA half-layer, silicon cell, rear EVA half-layer and backsheet. For node `i`,

`C_i dT_i/dt = Σ_j G_ij (T_j - T_i) + q_i,contact - q_i,surface`,

with `C_i = rho_i cp_i d_i` (J m^(-2) K^(-1)). Conductance between adjacent layer centers is

`G_ij = 1 / [d_i/(2 k_i) + d_j/(2 k_j) + R_int]`.

The blade/interface temperature is algebraic: `T_if = (h_c T_tool + G_g T_g + G_e T_e)/(h_c + G_g + G_e)`. Surface losses combine convection and radiation:

`q_s = h (T_s - T_amb) + eps sigma [(T_s + 273.15)^4 - (T_amb + 273.15)^4]`.

The source uses two property sets (Lizcano 2024 and Tomšič 2025), 3.2 mm glass, 0.21 mm silicon, two total EVA thicknesses, two emissivities, and interface-resistance cases. Assumed outer convection is 8 W m^(-2) K^(-1). These are literature/scenario inputs, not material characterization of an AGASTYA panel. There is no latent heat, temperature-dependent property table, adhesive/fracture law, reaction term, gas-generation model or blade motion.

## 3. Existing design sweep and new sensitivity analysis

The archived `EXP-S3-02` design contains 5,040 complete factorial scenarios: tool setpoint 180–300 °C (5 levels), contact conductance 100–3,000 W m^(-2) K^(-1) (4), dwell 0.1–10 s (7), ambient 15–35 °C (3), EVA thickness 0.90/1.16 mm (2), two property sets, and interface resistance 0/1e-4/5e-4 m² K W^(-1) (3). The historical output spans 15.65–261.53 °C for peak EVA node temperature and 1.38 kJ m^(-2)–1.72 MJ m^(-2) for integrated contact energy.

The new decomposition computes balanced-grid main-effect sums of squares. Equal weight is given to each designed scenario. The remaining share is the combined interaction/unallocated term; none of these percentages is a probability or uncertainty interval.

| Output | Largest main effect | Share | Second main effect | Share | Third main effect | Share |
|---|---|---:|---|---:|---|---:|
| Peak EVA temperature | Dwell time | 41.50% | Contact conductance | 35.82% | Tool setpoint | 3.57% |
| Peak cell temperature | Dwell time | 51.29% | Contact conductance | 21.85% | Ambient temperature | 2.74% |
| Contact energy per area | Dwell time | 55.20% | Contact conductance | 19.71% | Tool setpoint | 2.02% |

{{FIGURE:anova}}

The sensitivity rank says which assumed inputs deserve measurements if the pretreatment is pursued: actual contact time/kinematics and effective thermal contact are more consequential in this grid than the nominal tool setpoint alone. It does not show that these factors can be independently set or that the chosen ranges represent a machine.

## 4. Spatial refinement and numerical behavior

Four selected cases were simulated using 1, 2, 4, 8 and 16 control volumes in each of the five material layers (5–80 nodes total). The 1-cell case reproduces the five-node model exactly when both use the same explicit solver. An explicit 0.5 ms run on the refined grid diverged: the estimated explicit row-sum stability ratio reached 544.65 at 16 cells per layer in the low-EVA-thickness case, driven by the thin, high-conductivity silicon volumes. The failed data are retained under `Simulation_Campaign/raw/`.

The refinement was rerun with backward Euler. For the nominal case, peak EVA temperature rose from 79.98 °C at one cell per layer to 104.25 °C at 16 cells per layer. For the high-bound case, it rose from 247.27 °C to 276.05 °C. The 8-to-16-cell peak EVA change is about 2.1% in the nominal case; contact energy is already nearly unchanged by that refinement. This indicates that integral energy and local peak temperature have different mesh sensitivity. The 16-cell result is a numerical reference for this model, not proof that the actual panel reaches that temperature.

{{FIGURE:mesh}}

One-cell-per-layer results from the backward-Euler solver differ from the archived explicit result at 0.5 ms by at most 0.0044 °C in peak cell temperature and 42.5 J m^(-2) in integrated contact energy (about 0.018% of the nominal contact energy; relative difference depends on case). This is a solver/timestep cross-check, not spatial validation. A separate timestep study compares 1.0, 0.5 and 0.25 ms at 80 control volumes in nominal and high-bound cases. The largest relative difference from 0.5 to 0.25 ms among peak EVA temperature, peak cell temperature and contact energy is 0.00126%; the maximum energy residual is below 7.6e-10% for those six runs. These values support timestep stability only for the selected conditions and remain separate from model-form and physical uncertainty.

## 5. Chemical pathways and data limits

No chemical conversion is computed. EVA thermolysis and combustion can release organic compounds and carbon oxides; their rates and products depend on formulation, atmosphere, heating rate, and temperature history. The accessible 2026 study reports different emission behavior for transparent EVA, white EVA and alternatives, but its abstract does not supply enough conditions or data to parameterize a hot-knife model. Heating an encapsulant to separate an interface is not equivalent to full degradation. The model cannot predict polymer residue, interfacial adhesion, silver oxidation, metallization loss, or airborne emissions.

## 6. Verification and next measurements

- **Energy accounting:** the refined model's maximum absolute numerical energy residual is below 6.3e-10% of integrated contact energy for the 20 spatial runs. This checks implementation consistency under the equations used.
- **Coarse-limit check:** N=1 matches the five-node model within floating-point/reported discretization agreement; recorded diffs are preserved.
- **Explicit stability:** the refined explicit step fails the estimated criterion and visibly diverges; explicit integration was rejected for this mesh.
- **Mesh check:** 8-to-16 differences are reported per case/output in `PE-SIM-002_spatial_refinement.csv`; local peak temperature remains more mesh-sensitive than integrated energy.
- **Independent validation:** none. Required data include instrumented layer/interface temperatures, measured tool temperature and power, actual contact time, coupon stackup, contact pressure/speed, and a defined separation-quality endpoint.

## References

- Frischknecht, R., Komoto, K. & Doi, T. (2023). IEA PVPS T12-25:2023. [Report](https://iea-pvps.org/wp-content/uploads/2023/07/Report_IEA-PVPS_T12-25-2023_LCA-PV-Recycling-Hot-Knife.pdf).
- Shang, Y. et al. (2026). *J. Environ. Chem. Eng.* 14(2), 121479. [DOI](https://doi.org/10.1016/j.jece.2026.121479). Abstract-level review.
- Tammaro, M. et al. (2015). Thermal treatment of waste photovoltaic module for recovery and recycling. *Renewable Energy*, 81, 103–112. [DOI](https://doi.org/10.1016/j.renene.2015.03.014).
- Historical model and procedures: `Agastya_Physics_Simulation_2026-10-10.py`, `PROCEDURES_AND_RESULTS.md`, and `Research Phase D/Validation_Report.md`.
