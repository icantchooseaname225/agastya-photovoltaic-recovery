# Research Phase B/C

This folder contains reproducible evidence/data outputs and reports. It remains below Agastya Physics Simulation because scripts use the sibling Research Baseline directory.

## Start here

1. AGASTYA_PHASE_BC_REPORT.md — results and evidence limits.
2. evidence_database_v2.csv — 14 records.
3. separation_route_comparison_v2.csv — five routes.
4. scenario_results_v2.csv and sensitivity_analysis_v2.csv — two distinct reference cases and symbolic unknowns.
5. accounting_validation_report_v2.md and published_data_validation_v2.md.
6. electrostatic_stage_feasibility_v2.md.

## Reproduce

From this folder using Python 3.14.4 run: python build_evidence_database_v2.py; python published_data_reproduction_v2.py; python -m unittest -v accounting_unit_tests_v2.py; python validate_accounting_kernel_v2.py; python agastya_scenario_model_v2.py.

Literature result means a cited study's reported result; normalized arithmetic is a formula on a stated reference basis; symbolic means the numerical input is unknown; AGASTYA measurement means an actual sample result (none exists here). Only the separate thermal RC model is documented as executed; no electrostatic or chemistry solver is claimed.

