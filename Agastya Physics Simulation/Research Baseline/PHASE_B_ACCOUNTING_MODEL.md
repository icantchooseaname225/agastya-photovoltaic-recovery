# Stage 4 accounting kernel — Phase B starter

**Status:** executed against published normalized inventory data on 10 October 2026.  
**Run ID:** AGASTYA-PHASE-B-ACCOUNTING-001.

> **Historical Phase B note (updated 2026-10-11):** This v2 starter preserves its original 630 g/t arithmetic. Source review found the Dias et al. publisher abstract states 600 g/t, while 630 g/t appears in secondary conclusion excerpts; the denominator and discrepancy are not resolved. Treat the 630 row only as historical source-specific arithmetic, not a verified or typical feed value. The v3 source-qualified reproduction separates 300 ppm, 600 g/t and the unresolved 630 g/t excerpt and supersedes the interpretation, not the preserved v2 result.

## Model question

What silver content and full component mass closure follow arithmetically from the literature inventory scenarios already registered in this folder?

## Software and method

The script stage4_accounting_kernel.py uses CPython's standard library only. It reads preliminary_material_inventory.csv and writes reference_inventory_arithmetic.csv plus phase_b_accounting_run.json. It does not use NumPy, MOOSE, Rocky, Maxwell, Aspen, or another commercial or multiphysics solver.

The kernel defines the charter's balance equations:
- mass residual = input mass − sum(output masses) − documented losses
- Stage Ag recovery (%) = 100 × target-stream Ag mass / stage-input Ag mass
- Ag grade (%) = 100 × Ag mass in concentrate / total concentrate mass

The first run applies only the published normalized inventory arithmetic. Stage recovery and concentrate grade are not calculated because no stage output masses or Ag assays exist. The stage input form is stage_balance_input_template.csv; blank process values mean unknown, never zero.

## Results

- The published composition scenario sums to 1.000 kg per normalized 1 kg basis because it includes a 24.7 g unassigned remainder. Its reported Ag reference is 0.300 g/kg, or 300 ppm.
- The separate Dias et al. study benchmark is 0.630 g/kg, or 630 ppm. It is a separate Ag-only reference and does not have a complete component balance in this calculation.
- Physical Agastya samples: 0.
- Stage yields, liberation, separator partition, assay concentration and solver outputs: none.

## Numerical checks and limits

The composition sum is an arithmetic closure check on a literature scenario. It is not a physical mass-balance measurement and should not be described as a successful process closure. The 2.47% remainder is not assigned to known components. The 300 ppm and 630 ppm Ag references are from different study bases and are kept in separate rows.

No uncertainty distribution was fitted because the literature records do not provide a shared sampling distribution for Agastya. No Monte Carlo or optimization was run. The next model needs an identified panel or batch, measured Stage 1 streams, Stage 2 particle/liberation characterization, Stage 3 geometry and particle electrical properties, and Stage 4 laboratory assay results.
## Data-file verification

A Python CSV-reader check found consistent header/row field counts in the source register (13 rows), material inventory (10 rows), software matrix (7 rows), missing-specification table (20 rows), arithmetic output (2 rows), and stage input template (4 rows). All ten inventory record IDs are unique. The 2022 composition scenario sums to 1.000000000 kg per normalized 1 kg basis.
