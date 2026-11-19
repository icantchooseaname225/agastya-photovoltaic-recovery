# Agastya virtual experiment procedures and results

**Run date:** 10 October 2026  
**Data location:** this folder  
**Evidence status:** all records are simulations, scenario arithmetic or literature-normalized calculations. There are no physical trial rows.

## Scope and interpretation

The project’s current process is represented as Stage 2 supervised manual hand-off, Stage 3 hot-knife front-glass separation to a cell/EVA/backsheet laminate, and Stage 4 contained comminution plus dry size classification with ECS conditional on a characterized feed. These studies do not verify machine performance, safe operating conditions, delamination quality, EVA-free cells, roller heat reuse, or silver recovery.

Every data row has an `experiment_id` and `procedure_id`. The [experiment register](experiment_register.csv) gives a compact index and the [data dictionary](data_dictionary.csv) defines all columns in the main and follow-up CSVs. In both datasets, blank fields are not zero; they mean not applicable, unknown, or not calculated.

## Programs used

The current run used **CPython 3.14.4 (64-bit)** and **NumPy 2.5.3**. The initial and follow-up thermal calculations use the project's own five-node, 1-D thermal resistance/capacitance solver. It computes node heat flows and integrates temperatures with explicit forward Euler; NumPy vectorizes the parameter sweep. Python's standard library (`csv`, `json`, `itertools`, `math`, `statistics.NormalDist` and related utilities) writes files, enumerates factor combinations and performs mass-balance/lognormal calculations. PowerShell **7.6.5** launched the scripts in this run but did not calculate the thermal physics. No ANSYS, COMSOL, CFD, finite-element or other external physics package was used.

## Virtual setting counts and physical sample sizes

All `virtual cases` below are prescribed parameter combinations or model histories. A row is not a physical sample, a random draw, or an independent replicate. Thermal trace rows are time snapshots from the same history. There were **0 physical panels, 0 coupons, 0 particle samples, and 0 physical assay samples**.

| Study | Virtual settings / histories | CSV output rows | What the count represents |
|---|---:|---:|---|
| EXP-S2-01 — Stage 2 mass balance | 384 | 384 | 8 panel masses × 3 frame shares × 4 J-box/cable shares × 4 manual times |
| EXP-S3-01 — Stage 3 material balance | 1,152 | 1,152 | 384 Stage 2 combinations × 3 glass shares |
| EXP-S3-02 — Stage 3 thermal sweep | 5,040 | 5,040 | 5 knife temperatures × 4 conductances × 7 dwells × 3 ambients × 2 EVA thicknesses × 2 property sets × 3 interface resistances; each integrated at 5 ms (20–2,000 steps over the dwell) |
| EXP-S3-03 — Stage 3 temperature traces | 24 histories | 1,944 | 4 knife temperatures × 3 conductances × 2 dwells; 12 histories have 41 snapshots and 12 have 121 snapshots at 0.1 s spacing |
| EXP-S4-01 — Stage 4 size split | 129,024 | 129,024 | 1,152 laminate feeds × 7 D50 values × 4 GSD values × 4 screen cuts |
| EXP-S4-02 — Stage 4 literature Ag arithmetic | 10,368 | 10,368 | 1,152 laminate feeds × 3 assumed Ag masses × 3 literature partitions |
| EXP-CAP-01 — Stage 2/3 capacity | 36 | 36 | 4 manual times × 3 operator counts × 3 Stage 3 cycles |
| EXP-S3-04 — Timestep convergence | 8 conditions | 32 | 8 thermal conditions × 4 time steps |
| EXP-S3-05 — Cooldown heat | 8 conditions | 64 | 4 knife temperatures × 2 dwells × 8 delays |
| EXP-S4-03 — Inverse screen cuts | 196 | 196 | 7 D50 values × 4 GSD values × 7 target fines fractions |
| EXP-S4-04 — Conditional Ag grade | 51,840 | 51,840 | 1,152 laminate feeds × 3 assumed Ag masses × 3 literature partitions × 5 assumed fines yields |
| **Total** | — | **200,080** | Two CSVs; all rows virtual/model/scenario calculations |

For the Stage 3 time traces, 2 s contact + 2 s cooldown gives 41 snapshots including time zero; 10 s contact + 2 s cooldown gives 121. These are time points, not 41 or 121 separate samples. The timestep convergence study is eight conditions re-solved at four integration steps; the 32 rows do not represent 32 panels.

## Stage 2 — supervised manual hand-off

### EXP-S2-01 / PROC-S2-01: mass balance and one-operator ceiling

**Procedure.** Enumerate panel masses 10, 12, 15, 18, 20, 24, 28 and 30 kg; frame shares 7%, 10% and 13%; removable J-box/external-cable shares 0.1%, 0.25%, 0.5% and 1%; and assumed manual times 120, 300, 600 and 900 s. For each combination, calculate frame and cable masses, Stage 3 hand-off mass, mass closure, and `28,800 s / manual time` as an ideal one-operator 8-hour ceiling. The thesis’s 10 wt% frame and 70 wt% glass composition values are central references; ranges around them are sensitivity inputs.

**Outcome.** The master CSV contains 384 rows. Calculated Stage 3 input mass spans **8.60–27.87 kg/panel**. Mass closure is 100% by construction.

**Conclusion.** This estimates bookkeeping consequences of stated mass shares and task times. It is not an observed panel balance or a staffing/throughput measurement. Current Stage 2 remains a supervised manual hand-off.

**Not modeled.** Electrical isolation, work hazards, operator-to-operator variation, transport, queueing, breaks, inspection, failed removals and actual labor time.

## Stage 3 — mass balance and thermal delamination model

### EXP-S3-01 / PROC-S3-01: glass and laminate mass balance

**Procedure.** For every Stage 2 row, apply front-glass shares of 65%, 70% and 75% of original panel mass. Subtract scenario glass mass from Stage 2 output mass to obtain the cell/EVA/backsheet laminate balance.

**Outcome.** The master CSV contains **1,152 rows**. Glass plus laminate closes to the scenario Stage 3 input by construction.

**Conclusion.** This is a composition-based mass split, not a measured hot-knife yield. Stage 3’s represented output is front glass plus laminate; the calculation does not claim EVA-free cells.

### EXP-S3-02 / PROC-S3-02: five-node hot-knife thermal sweep

**Procedure.** Integrate a 1-D five-node thermal resistance/capacitance network for glass, front EVA, silicon cell, rear EVA and backsheet. Each node’s sensible heat capacity is its literature density × heat capacity × assumed thickness. Conductive heat transfers between nodes; the assumed knife boundary applies at the glass/EVA interface; convection and radiation remove heat at the front and rear surfaces. Sweep tool temperature 180/200/220/250/300 °C, contact conductance 100/300/1,000/3,000 W/(m²·K), local dwell 0.1/0.25/0.5/1/2/5/10 s, ambient 15/25/35 °C, total EVA thickness 0.90/1.16 mm, two literature property sets, and interface resistance 0/1×10⁻⁴/5×10⁻⁴ m²·K/W. The integration step is 5 ms.

**Outcome.** The master CSV contains **5,040 cases**. Modeled peak EVA-node temperature spans **15.65–261.53 °C**. Modeled contact heat spans **1.38 kJ–1.72 MJ per m² of assumed contact area**. Maximum absolute integrated energy-balance residual is **9.218×10⁻¹²%**.

**Conclusion.** The solver is internally energy-balanced for these idealized cases, but the wide output range follows deliberately broad assumptions. Heat is per assumed contact area, not electrical heater energy per panel. These figures do not predict whether glass will peel or what material quality will result.

**Not modeled.** Actual knife/blade mass and power control, panel motion, full-panel heat flow, latent heat, EVA chemistry, adhesion and fracture, fumes, damage, peel force or quality scoring. The 280 °C comparison flag is not a safety limit.

### EXP-S3-03 / PROC-S3-03: representative temperature traces

**Procedure.** Save 0.1-second snapshots from the same 5 ms five-node solver for 24 settings: tool 180/200/220/300 °C; contact conductance 100/1,000/3,000 W/(m²·K); dwell 2/10 s; then 2 s of modeled cooling after switching off blade contact.

**Outcome.** The master CSV contains **1,944 trace rows**.

**Conclusion.** These traces illustrate how the assumed local boundary and layer properties affect modeled temperature over time. No trace is an instrument recording.

### EXP-S3-04 / PROC-S3-04: timestep convergence

**Procedure.** Re-run eight representative cases at time steps 10, 5, 2.5 and 1.25 ms. Compare the maximum of the front/rear EVA peak temperatures at each step to the 1.25 ms result for the same case.

**Outcome.** The follow-up CSV contains **32 rows**. The maximum absolute peak-EVA difference from the 1.25 ms result is **0.154541 °C** across these eight conditions.

**Conclusion.** This measures integration-step sensitivity for the implemented reduced model. It does not validate the chosen contact conductance, layer properties, boundary conditions or model form against a real panel.

### EXP-S3-05 / PROC-S3-05: retained-heat cooldown

**Procedure.** For each tool temperature 180/200/220/300 °C and dwell 2/10 s, run the five-node model at 5 ms with contact conductance 1,000 W/(m²·K), ambient 25 °C, 0.90 mm total EVA, the Lizcano property set and 1×10⁻⁴ m²·K/W interface resistance. Switch the blade boundary off after dwell. At delays 0, 1, 5, 10, 30, 60, 120 and 300 s, record node temperatures and sensible heat above ambient, `Σ Cᵢ(Tᵢ−Tₐₘᵦ)`.

**Outcome.** The follow-up CSV contains **64 rows**. At contact-off (0 s), modeled stored stack heat spans **193–1,179 kJ/m²**. After 300 s of modeled cooling, it spans **61–304 kJ/m²** across the eight configurations.

**Conclusion.** Heat remains in the modeled layers during cooldown under the assumed surface losses. This does **not** show that a roller can capture that heat, that it reaches EVA where needed, that delamination quality is preserved, or that any external heater energy is saved.

## Stage 4 — assumed size classification and conditional Ag arithmetic

### EXP-S4-01 / PROC-S4-01: lognormal fines mass sensitivity

**Procedure.** Treat particle size as a mass-weighted lognormal distribution. For each of 1,152 scenario laminate feeds, evaluate the cumulative fraction below screen cuts 0.25/0.50/1/2 mm for D50 0.10/0.25/0.50/1/2/4/8 mm and geometric standard deviation (GSD) 1.4/1.8/2.2/2.8. Compute `fines fraction = Φ[ln(cut/D50) / ln(GSD)]` and partition feed mass into fine and coarse bins.

**Outcome.** The master CSV contains **129,024 rows**; modeled fines fraction spans **0–1**.

**Conclusion.** Results are dominated by assumed post-comminution particle size. The range is a sensitivity result, not a screen or crusher performance interval. The current Stage 4 research direction remains contained comminution and dry classification; ECS is conditional on a suitable measured feed.

**Not modeled.** Agastya crusher behavior, screen efficiency, shape, moisture, agglomeration, component liberation, sample assay, or ECS particle trajectory.

### EXP-S4-02 / PROC-S4-02: source-specific literature Ag partition

**Procedure.** Scale 10/20/30 g/panel Ag assumptions by three source-specific published Ag-to-fines distribution fractions (70%, 80%, and 94.12%) over the Stage 3 laminate scenarios. Keep the study-feed categories distinct.

**Outcome.** The master CSV contains **10,368 rows**. Baseline product-grade columns are blank because fines mass yield was not supplied.

**Conclusion.** This is arithmetic normalization of literature distributions. The cited figures are not Agastya recovery, grade or purity. The calculation conditionally puts all scenario silver in the Stage 4 laminate; Stage 3 Ag partition is unknown.

### EXP-S4-03 / PROC-S4-03: inverse screen-cut sensitivity

**Procedure.** For D50 0.10/0.25/0.50/1/2/4/8 mm, GSD 1.4/1.8/2.2/2.8, and target fines fractions 5/10/25/50/75/90/95%, invert the assumed lognormal CDF: `cut = D50 × GSD^(Φ⁻¹(target fraction))`.

**Outcome.** The follow-up CSV contains **196 rows**; the calculated cuts span **0.0184–43.511 mm**.

**Conclusion.** The spread shows why screen selection should follow a measured feed PSD. These values are mathematical cuts for assumed lognormal PSDs, not recommended screen apertures or physical trial settings.

### EXP-S4-04 / PROC-S4-04: conditional Ag grade versus assumed fines yield

**Procedure.** For each of 1,152 laminate feed scenarios, combine 10/20/30 g Ag/panel, each of the three literature partition fractions, and assumed fines mass yields 5/10/20/40/60%. Calculate fines mass and `100 × Ag-in-fines (g) / fines mass (g)`.

**Outcome.** The follow-up CSV contains **51,840 rows**. Conditional fine-grade arithmetic spans **0.139–51.338 wt%** across this deliberately broad input set.

**Conclusion.** Product grade depends strongly on assumed fines mass yield and on applying a literature partition to a non-matching, unassayed Agastya feed. These results are conditional arithmetic only; none are product-grade predictions.

## Cross-stage capacity sensitivity

### EXP-CAP-01 / PROC-CAP-01: idealized Stage 2/3 bottleneck

**Procedure.** For manual time 120/300/600/900 s, Stage 2 operators 1/2/3, and Stage 3 cycle 50/60/90 s, calculate Stage 2 team capacity `operators × 28,800 / manual time`, Stage 3 station capacity `28,800 / cycle`, and the lower capacity as the idealized bottleneck.

**Outcome.** The follow-up CSV contains **36 rows**. The idealized bottleneck spans **32–576 panels per 8-hour shift**.

**Conclusion.** The arithmetic identifies which assumed station would constrain that idealized two-station line. It is not a throughput forecast: it assumes independent full-shift operators and a single Stage 3 station with no breaks, transport, setup, downtime, defects, or queueing.

## Conclusions about the current approaches

| Approach | What these runs support | What remains unknown / development conclusion |
|---|---|---|
| Stage 2 supervised manual hand-off | The scenario mass balance and assumed task-time grid are internally consistent; the modeled hand-off mass spans 8.60–27.87 kg/panel. | Keep the current supervised manual step as the documented baseline until actual module masses and task times are recorded. The 32–576 panels/shift capacity range is an ideal arithmetic ceiling, not a throughput forecast or a reason to automate. |
| Stage 3 hot-knife glass separation | The reduced thermal model maps how its chosen contact and material assumptions affect layer temperatures. The main sweep gives 15.65–261.53 °C peak EVA-node temperatures. Refining eight selected cases from 10 ms to 1.25 ms changes peak EVA temperature by at most 0.154541 °C. | Use hot-knife glass-to-laminate separation as the reference for instrumented coupon comparisons, consistent with the existing project plan. Numerical step stability does not validate model physics. The model does not calculate adhesion/fracture or peel quality, so it cannot choose a setpoint or confirm delamination. The heated roller, EVA-free cells, and heat reuse remain unverified. |
| Stage 4 contained comminution + dry classification | The lognormal sweeps and inverse-cut calculations show that fines split depends strongly on the assumed PSD; fines range from 0 to 1 in the baseline, and inverse cuts span 0.0184–43.511 mm. | Keep this as the Stage 4 research path, then measure a real laminate PSD and mass balance before selecting a screen. The broad sensitivity does not indicate likely yield. ECS stays conditional on an eligible measured feed; no ECS behavior was simulated. |
| Stage 4 silver recovery | Literature-normalized arithmetic and assumed fines yields make the mass-balance dependencies visible. | No Agastya grade or recovery conclusion is supported. The 0.139–51.338 wt% conditional range is driven by assumed feed silver, literature fractions from different feeds, and assumed fines yield; assay the feed and products and establish Stage 3 Ag partition first. |

These runs do **not** compare physical alternatives or establish a validated best process. They support a measurement-first development plan: weigh and time Stage 2; instrument Stage 3 coupons for tool/material temperatures, energy, force and output quality; then characterize and assay contained Stage 4 fractions. No simulated temperature, capacity, screen cut or grade is a safety setting or purchase specification.

## How to use the results

Use the CSVs to trace scenario calculations and compare sensitivity to assumptions. Before treating any result as a process conclusion, replace assumptions with measured panel composition, Stage 2 hand-off weights/times, instrumented Stage 3 coupon temperatures and energy, and Stage 4 feed PSD/mass assays. Keep observed measurements in a separately identified trial dataset with actual instrument, sample, date, calibration and procedure records.
