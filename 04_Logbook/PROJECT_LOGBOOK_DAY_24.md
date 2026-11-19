# Logbook — 10 October 2026
## Phase A research baseline for the integrated Agastya recovery system

### Objective
Read the user-provided research charter and establish an evidence-backed four-stage architecture, literature baseline, software access plan, material inventory, missing-input list and model roadmap before new solver runs.

### Work completed
- Adopted the latest charter's stage order: Stage 1 component disassembly; Stage 2 mechanical liberation; Stage 3 electrostatic separation; Stage 4 assay and material accounting.
- Recorded the stage-number conflict with earlier Agastya files. Legacy thermal delamination and comminution datasets were preserved and cross-referenced rather than renamed.
- Reviewed primary PV recycling studies and official software documentation.
- Added a one-kilogram literature composition scenario with an explicit 2.47% unassigned remainder; retained the separate 0.63 g/kg reported silver value as a distinct study reference.
- Compared electrostatic PV separation with a direct silver-focused flotation study. The electrostatic paper's cited result is for silicon, not silver.
- Documented published thermal coupon count and method as a reference design only, not an Agastya temperature recommendation.
- Documented no verified Agastya physical samples, coupons, particles, assays, facility access, or new solver runs.

### Outcome
Phase A is documented in the Research Baseline folder, with supporting source, inventory, software and missing-specification CSV files. The existing simulation's 200,080 rows remain virtual model/scenario records and are not reclassified as experimental results.

### Conclusion
An integrated recovery prediction is not yet defensible. The largest gating inputs are actual module identity and mass/composition, measured Stage 2 liberation/particle classes, Stage 3 separator/charge properties and validated assays. Local Python/NumPy can support the accounting model; external solver access and licenses remain unconfirmed. No physical experiment or commercial solver was run in this entry.

### Next action
Register one identified c-Si panel or controlled panel lot, establish the stage-1/thermal-pretreatment crosswalk with the project owner/supervisor, and confirm an assay provider and solver access. Then build the component mass model and instrumented validation plan before running coupled particle or fracture models.
## Phase B accounting model starter — 10 October 2026

- Added a reproducible Stage 4 accounting kernel using the Python standard library and executed it on the literature-normalized inventory scenarios.
- Run ID: AGASTYA-PHASE-B-ACCOUNTING-001. Output: two calculated literature benchmark rows, not solver output.
- The 2022 composition scenario closes to 1.000 kg only because the 24.7 g unassigned remainder is explicitly included; the arithmetic residual is 0.000 kg.
- The 2016 silver-only reference remains separate: 0.630 g Ag per normalized kg, with no full component balance.
- No stage recoveries or concentrate grades were calculated; no Agastya input/output assays or stage partition measurements exist.
- Local environment check found CPython 3.14.4 and NumPy 2.5.3; no MOOSE, Rocky, Maxwell, OpenFOAM, or Cantera executable; no browser solver session. WSL launcher was present but no Linux distribution was listed.

The model source, execution manifest, normalized arithmetic output, and blank stage input template are in Agastya Physics Simulation/Research Baseline. No new physical experiment or external solver run was performed.
- CSV structural validation passed after correcting the stage input template: all six CSVs have uniform row widths, ten inventory record IDs are unique, and the composition scenario sums to 1.000000000 kg on its normalized basis.