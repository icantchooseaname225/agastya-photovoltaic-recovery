# Historical research baseline and accounting model

This folder preserves the 10 October 2026 Phase A/B baseline and its reproducible literature arithmetic. Its “latest charter” wording reflects the 10 October map and was superseded by the project owner's 16 October correction. The current stage source of truth is the root AGASTYA_ARCHITECTURE.md. Keep the baseline report unchanged for provenance.

## Files

- AGASTYA_PHASE_A_BASELINE_2026-10-10.md — fixed baseline: architecture as understood on 10 October, literature, software access, sample/facility leads, missing inputs, and roadmap.
- ARCHITECTURE_CROSSWALK_2026-10-10.md — historical map and pointer to the corrected current architecture.
- agastya_four_stage_process_flow.svg — flow diagram for the 10 October charter; do not use it as the current map.
- source_evidence_register.csv — the baseline's 13 source records.
- preliminary_material_inventory.csv — literature-normalized scenarios, not Agastya sample measurements.
- software_access_matrix.csv, missing_specifications.csv, and REAL_TEST_READINESS.md — baseline-era access and gap records.
- PHASE_B_ACCOUNTING_MODEL.md, stage4_accounting_kernel.py, reference_inventory_arithmetic.csv, and phase_b_accounting_run.json — reproducible literature arithmetic under the earlier Stage 4 assay/accounting scope.
- stage_balance_input_template.csv — blank stage data template; blanks mean unknown.

## Reproduce the calculation

From PowerShell in this folder, run: python stage4_accounting_kernel.py.

The script reads preliminary_material_inventory.csv and overwrites the normalized arithmetic CSV and run manifest. It does not generate thermal, fracture, particle-trajectory, electrostatic, or chemical solver output.

The one-kilogram scenario is a literature-based reference. A zero residual comes from an explicit unassigned remainder, not from a measured process balance. Stage recoveries and concentrate grade remain blank until actual stream masses and assays exist.
