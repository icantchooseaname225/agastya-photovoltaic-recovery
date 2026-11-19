# Agastya physics simulation data

> **Historical model package.** The CSVs and reports were built for the 10 October 2026 study map. Their row labels and conclusions stay as generated. The current architecture is in the root AGASTYA_ARCHITECTURE.md: Stage 1 vision triage, Stage 2 robotic mechanical disassembly, Stage 3 hot-knife/foam-roller thermal separation, and Stage 4 material liberation, separation and silver recovery. This historical package retains its earlier manually prepared Stage 2 assumptions. Historical “Stage 4” size-classification calculations describe possible feed preparation; they do not model silver removal. The Phase A baseline itself is unchanged.

This folder contains a Python/NumPy design study and follow-up virtual sensitivities. Its outputs are not physical trials, independent replicates, a validated machine model, or silver-recovery evidence.

## Files and results

The initial CSV has 147,912 rows and followup_virtual_experiments.csv has 52,168, for 200,080 data rows in total. The experiment register, data dictionary, metadata, procedure report, and Python sources describe their assumptions and output meanings. The word “experiment” means a virtual scenario or calculation, not an equipment trial.

The model run represented historical Stage 2 manual component removal, Stage 3 hot-knife front-glass separation to a cell/EVA/backsheet laminate, and Stage 4 size-classification arithmetic. The Stage 4 size calculations do not simulate silver removal, assay, or recovery. The Stage 3 five-node thermal model does not model EVA removal, adhesive fracture, peel quality, machine power, safe operation, or measured heater energy per panel.

The original thermal sweep used CPython 3.14.4, NumPy 2.5.3 and explicit forward Euler. Phase E added backward-Euler spatial refinement and timestep checks. These are numerical checks, not physical validation. No panel, coupon, particle, process mass, Ag assay, or recovery value was measured by these files. Blank cells mean unknown, not zero.

## Current project boundary

Use the root current architecture and REAL_TEST_READINESS.md for present definitions and physical-data gates. Hot-knife literature supports design review, not an Agastya operating window. Stage 4 remains an open silver-removal/recovery route selected against measured Stage 3 feed, qualified facility capability, safety/waste controls, assay QA/QC, and receiver requirements.

The Phase A baseline in Research Baseline/AGASTYA_PHASE_A_BASELINE_2026-10-10.md remains untouched as a historical baseline. Its folder README explains that the 10 October charter was superseded on 16 October.

## Reproduce the historical files

These commands regenerate historical study outputs and can overwrite corresponding CSV, report, metadata, and documentation files. Run them only when intentionally reproducing the 10 October study. Preserve the existing outputs first. From the project root, run the initial model, then followup_virtual_experiments.py, then build_dataset_docs.py with Python 3 and NumPy installed.

## Project links

- Main project index: ../AGASTYA_PROJECT_INDEX.md
- Current architecture: ../AGASTYA_ARCHITECTURE.md
- Project understanding audit: ../00_Project_Management/PROJECT_UNDERSTANDING_AUDIT.md
- Latest logbook question: ../00_Project_Management/OPEN_QUESTIONS.md
- Detailed Day 23 entry: ../04_Logbook/PROJECT_LOGBOOK_DAY_23.md
- Stage 3 thermal development: ../Build Files and Steps/Stage 3/STAGE3_THERMAL_DEVELOPMENT.md
- Stage 4 silver-removal research: ../Build Files and Steps/Stage 4/README.md

