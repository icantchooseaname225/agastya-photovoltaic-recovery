# Accounting validation report — Phase B/C

Prepared 2026-10-11 with CPython 3.14.4.

## Results

- The 25 legacy probes of the preserved Phase A kernel contain 22 passes and 3 flagged gaps.
- The Phase B/C accounting functions passed all 28 unit tests.
- Physical AGASTYA samples and assays: zero documented.
- Solver runs in this phase: zero.

The three legacy findings are ORIG-REC-OVER-100, ORIG-GRADE-OVER-100 and ORIG-NAN. The old implementation accepts recovery or grade above 100% and non-finite input. These are findings in preserved historical code, not failures in the separately unit-tested Phase B/C functions.

## Definitions

Stage recovery (%) = 100 × Ag mass in target output / Ag mass entering the stage. Product grade (wt%) = 100 × Ag mass in product / total product mass. Mass residual = input mass − accounted output masses − documented loss. Silver residual uses assay-derived Ag masses. A particle-mass split is not an Ag recovery; an assay concentration is not an Ag mass until multiplied by stream mass. Residuals are reported, never forced to zero.

## Reproduction

From this directory run: python -m unittest -v accounting_unit_tests_v2.py; python validate_accounting_kernel_v2.py; python agastya_scenario_model_v2.py. The three legacy findings are intentional issue flags. Case detail is in accounting_validation_results_v2.csv.

