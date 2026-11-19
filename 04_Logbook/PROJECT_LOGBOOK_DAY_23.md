# Day 23 — Multistage Physics Simulation and Sensitivity Data

**Date:** 10 October 2026  
**Record status:** numerical modeling and scenario calculations only. No physical panel, coupon, heater, crusher, sieve, or separator was operated; no Agastya trial data were entered.

## Objective

Run a reproducible model across the current Stage 2 manual hand-off, Stage 3 thermal glass separation, and the Stage 4 size-classification research hypothesis. Produce a substantial, machine-readable dataset while keeping simulated outputs separate from measurements and literature benchmarks.

## Work completed

- Inspected the existing browser process walkthrough and Wokwi monitor simulation. Both are conceptual/UI demonstrations, not process-physics solvers.
- Built and ran a Python/NumPy parameter sweep with 147,912 consolidated records in `Agastya Physics Simulation`:
  - **384 Stage 2 scenarios** for panel mass, frame/J-box-cable fractions, manual time, mass closure, and an idealized one-operator shift ceiling.
  - **1,152 Stage 3 material-balance scenarios** for front-glass and cell/EVA/backsheet laminate mass using the thesis composition graphic with an explicit ±5 percentage-point glass sensitivity.
  - **5,040 Stage 3 transient thermal cases** using a five-node 1-D thermal resistance/capacitance model (glass, front EVA, silicon cell, rear EVA, backsheet).
  - **1,944 Stage 3 time-trace rows** at 0.1-second output spacing for representative heat-up and cooldown conditions.
  - **129,024 Stage 4 size-classification scenarios** using an assumed mass-weighted lognormal PSD, varied D50, distribution spread, and screen aperture.
  - **10,368 separate Stage 4 literature-normalized scenarios** scaling published silver-to-fines distributions against 10/20/30 g/panel assumptions. Product grade is left blank because the fine-product mass yield is not available.
- Recorded thermal material properties from two published PV module model tables. Contact conductance, interfacial resistance, local dwell, Stage 2 removal shares/time, composition sensitivities, and Stage 4 PSD parameters remain explicitly labeled assumptions.
- Added a model report, source script, and machine-readable metadata next to the CSV. The initial schema now has 62 columns, including experiment and procedure IDs, and retains provenance/evidence labels per row.
- Checked CSV record counts and unique IDs, schema width, and mass-closure rows. The 5 ms thermal time step had a maximum absolute integrated energy-balance residual of 9.22×10⁻¹²%; halving the step changed peak EVA temperature by at most 0.0091 °C in three representative cases. These checks establish numerical consistency only; they do not validate the physical model.

## Results and interpretation

- The Stage 3 thermal sweep produced peak modeled EVA-node temperatures from **15.65 to 261.53 °C** and net interface heat from **1.38 kJ/m² to 1.72 MJ/m²** of assumed blade-contact area. These are not panel-level energy estimates, measured heater draw, validated delamination outcomes, or approved operating settings.
- Stage 4 modeled fines mass fraction ranged from **0 to 1** across deliberately broad unknown PSD and cut-size combinations. This shows how strongly results depend on the unmeasured feed PSD; it is not a performance range for Agastya.
- The published 70%, 80%, and 94.12% Stage 4 figures remain source-specific distributions of silver into fine fractions. They are not Agastya silver recovery, product grade, or purity. The scaling scenario assumes all silver in its 10/20/30 g per-panel input reaches the modeled Stage 4 laminate; Stage 3 silver partition is unknown and not simulated.
- The Stage 4 model follows the latest project direction of contained comminution and dry size classification, with eddy-current separation conditional on a characterized eligible feed. It does not simulate an ECS trajectory because the required Agastya feed and separator parameters are unknown.

## Project files

- Initial dataset: `../Agastya Physics Simulation/Agastya_Physics_Simulation_2026-10-10.csv`
- Model report: `../Agastya Physics Simulation/Agastya_Physics_Simulation_2026-10-10.md`
- Reproducible script: `../Agastya Physics Simulation/Agastya_Physics_Simulation_2026-10-10.py`
- Run metadata: `../Agastya Physics Simulation/Agastya_Physics_Simulation_2026-10-10_metadata.json`

## Next steps

Replace assumptions with real records when available: weigh one isolated panel and Stage 2 outputs; run supervisor-approved, instrumented Stage 3 coupons; then characterize Stage 3 laminate particle-size distribution and assay retained Stage 4 fractions at a qualified facility. Do not convert this simulation into an experimental result or performance claim.

## Follow-up simulation organization and virtual experiments

- Moved all simulation outputs and scripts into `D:\Agastya\Agastya Physics Simulation`; logbook records remain in `Logbook`.
- Added `experiment_id` and `procedure_id` to every initial CSV row. Built a field-by-field dictionary for both CSV schemas and an experiment register with procedure, inputs, outcome, conclusion, evidence class, limitations, row count and physical-trial count.
- Added and ran 52,168 follow-up rows: 36 Stage 2/3 ideal capacity scenarios; 32 timestep convergence cases across 8 thermal conditions; 64 retained-heat cooldown outputs; 196 inverse lognormal screen-cut scenarios; and 51,840 conditional Ag-grade calculations across assumed fines yields.
- Combined data volume is 200,080 scenario/model rows in two CSVs. The cooldown model leaves 61.0 kJ–1.179 MJ/m² of sensible heat in its assumed layer stack across the sampled cases and delays; it does not model roller contact or usable energy recovery. The finer timestep comparison spans a maximum 0.154541 °C peak-EVA difference from 1.25 ms across the selected cases. The conditional Ag-grade range is 0.139–51.338 wt% and depends on unverified feed silver, literature partition transfer, and analyst-set fines yield.
- Added `PROCEDURES_AND_RESULTS.md` with repeatable methods, outcomes and conclusions, plus a README that states the project process boundaries, model exclusions, blank-value semantics and rerun commands.
- No panel, coupon, thermal tool, roller, crusher, sieve or separator was operated. Physical trial rows remain zero; all new records are explicitly virtual or scenario calculations.
- The run used CPython 3.14.4 (64-bit) and NumPy 2.5.3. A custom five-node 1-D thermal RC model uses explicit forward Euler integration; Python standard-library code handles scenario grids, CSV/JSON output, capacity arithmetic and lognormal calculations. PowerShell 7.6.5 launched the scripts but was not a physics solver. No commercial FEM/CFD/process simulator was used.
- Clarified sample counts: the 200,080 rows represent deterministic parameter combinations, thermal histories, or time snapshots—not physical specimens, random draws, or statistical replicates. Physical sample size was zero panels, coupons, particle samples, and assays.
- Approach conclusion: retain Stage 2 supervised manual work as the current baseline pending actual mass/time records; use hot-knife glass-to-laminate separation as the Stage 3 instrumented comparison baseline, without treating the heat model as proof of peel quality; keep contained Stage 4 comminution and dry classification as the measured-feed research path, with ECS conditional. No grade, recovery, safe setpoint, throughput or heat-reuse result is established.

**Updated project files:** `../Agastya Physics Simulation/README.md`, `../Agastya Physics Simulation/PROCEDURES_AND_RESULTS.md`, `../Agastya Physics Simulation/experiment_register.csv`, `../Agastya Physics Simulation/data_dictionary.csv`, and `../Agastya Physics Simulation/dataset_checks_and_summary.json`.

## Follow-up — requested physical validation and engine access

**Date:** 10 October 2026  
**Status:** inventory details pending; no physical measurements added.

- The user asked to test actual physics/chemistry engines using panels, coupons, particles, samples, and assays, and confirmed that an inventory can be provided.
- Checked the local runtime for common command-line physics/chemistry solvers and specialist packages; none were found in the checked runtime. This does not establish what is installed at an external lab. No lab instrument-control or assay connector is available in this workspace.
- The simulation folder now contains `REAL_TEST_READINESS.md`, with the verified state, requested inventory fields, evidence-linkage requirements, and the staged validation sequence based on the existing Stage 3 and Stage 4 plans.
- No engine was newly installed or run, and no physical sample or assay was tested. Current numerical data remain virtual. Actual outcomes must be entered only from traceable facility records and instrument exports.
- Next step: review the user's facility, software, sample, equipment, and assay inventory; then determine which solver runs can be performed from this workspace and what laboratory measurements must be carried out by the supervised facility.

## Follow-up — public resource search

**Date:** 10 October 2026  
**Status:** desk research only; no samples acquired, facilities contacted, or physical experiments performed.

- Searched the project records for sample IDs, coupon/particle inventories, assay results, and trial measurements. Found blank Stage 3/Stage 4 logs and digital research datasets, but no verified Agastya physical sample IDs or assay results. The EYE source-study cell count is from an external research benchmark and is not an Agastya sample inventory.
- Identified MOOSE as the leading open-source candidate for future coupled Stage 3 heat-transfer/solid-mechanics work, COMSOL as a licensed cohesive-zone alternative, OpenFOAM as a thermal-only cross-check, and Cantera only for a defined chemistry question with a validated reaction mechanism. None was found installed in the checked local runtime.
- A fresh shell check confirmed Python 3.14.4 and NumPy 2.5.3; `arduino-cli`, `foamVersion`, `mpiexec`, and `moose-opt` were not on PATH. The Stage 1 readiness note was corrected so it no longer claims Arduino CLI availability without current evidence. Its proposed 3 V mini panel and the Stage 3 thermocouple monitor hardware remain unverified physical inventory.
- Found public regional leads: CSIR-CMERI Durgapur lists solar PV recycling activity; CSIR-CGCRI Kolkata lists ICP-MS/ICP-AES/XRF and external characterization services; STQC ERTL(East) Kolkata lists PV module testing; NISE Gurugram lists PV module and cell/material testing. Public pages establish their stated activities only, not Agastya access, sample supply, assay LOD, or a confirmed test booking.
- Added `resource_inventory_and_leads.csv` and expanded `REAL_TEST_READINESS.md` with the verified-vs-unknown boundaries, recommended engine fit, potential facilities, and questions to confirm. No enquiries were sent.
