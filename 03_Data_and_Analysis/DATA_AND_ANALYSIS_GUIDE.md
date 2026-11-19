# Data and analysis guide

## Where to look

| Data or code | Authoritative location | Evidence type |
|---|---|---|
| Literature extraction | [Source register](../01_Research/03_Source_Evidence/SOURCE_EVIDENCE_REGISTER.csv); detailed `evidence_database_v2.csv` is a preserved source extract | Source-reported findings with per-record limitations |
| Route comparison | `Agastya Physics Simulation/Research Phase B-C/separation_route_comparison_v2.csv` | Literature comparison, not AGASTYA test data |
| Published-value arithmetic | `Agastya Physics Simulation/Research Phase B-C/published_data_validation_v3.csv` and `published_data_reproduction_v3.py` | Reproducible arithmetic from attributed paper values |
| Normalized reference scenarios | `scenario_results_v3.csv` and `scenario_model_run_v3.json` in the Phase B/C folder | Three source-qualified normalized records; process-stage outputs are blank |
| Historical sensitivity table | `sensitivity_analysis_v2.csv` and its report in the Phase B/C folder | Nine source/range and unknown-input rows; not a probability distribution or physical uncertainty estimate |
| Accounting implementation | `accounting_unit_tests_v2.py`, `validate_accounting_kernel_v2.py`, and their validation report/results | Code tests and legacy input checks; no process-performance validation |
| Historical simulation data | `Agastya Physics Simulation/` CSVs plus `README.md`, `PROCEDURES_AND_RESULTS.md`, scripts and JSON manifests | Virtual scenario/time-history model outputs; 200,080 rows, zero physical samples |
| Preliminary literature inventory | `Agastya Physics Simulation/Research Baseline/preliminary_material_inventory.csv` | Historical v1 source scenario; not an AGASTYA bill of materials |

The `v2` reference outputs are retained as a historical record. Use `v3` for source-qualified arithmetic: 300 ppm is a review scenario with unresolved basis; 600 g/t is stated in the Dias publisher abstract; 630 g/t is shown separately only as an unresolved secondary excerpt. These are not pooled and are not AGASTYA assay values.

## Quantities and equations

- **Mass yield** = target-stream mass ÷ feed mass × 100.
- **Ag grade** = Ag mass in product ÷ total product mass × 100.
- **Ag recovery** = Ag mass in target product ÷ Ag mass entering that stage × 100.
- **Mass residual** = input mass − sum(all measured outputs) − documented losses.
- **Ag residual** = Ag in feed − sum(Ag in all outputs) − documented Ag loss.
- **Concentration** (ppm or wt%) describes composition. It is not the same as recovery or purity.
- **Product purity** requires an appropriate final-product assay/definition; a silver-bearing concentrate is not pure silver metal.

The v3 literature arithmetic gives a normalized 1 kg case only to make units clear. The 300 ppm figure is a secondary-sourced scenario with unresolved denominator/provenance. The 600 g/t figure is directly stated in the Dias publisher abstract; a secondary 630 g/t value remains unreconciled. Neither is an AGASTYA assay or a confidence interval.

## Reproduce the saved checks

In PowerShell, from the project directory:

```powershell
Set-Location 'C:\Agastya\Agastya Physics Simulation\Research Phase B-C'
python .\published_data_reproduction_v3.py
python .\agastya_scenario_model_v3.py
python .\accounting_unit_tests_v2.py
python .\validate_accounting_kernel_v2.py
```

The first two commands regenerate current versioned CSV/JSON arithmetic. The unit suite should report 28 tests passing. The legacy kernel audit intentionally reports three known gaps: recovery above 100%, grade above 100%, and NaN acceptance. Do not treat that audit as a passing production validation.

## Interpretation limits

The historical 200,080 records are virtual scenario combinations and time histories; they are not independent specimens or measured trials. The five-node thermal RC model is a reduced numerical model with assumed properties/boundaries, not a validated heat-delamination or fracture engine. No electrostatic field solver, DEM, CFD, FEM, chemistry engine, assay instrument, or physical sample run is documented. No per-stage yields, grades, product masses, or AGASTYA recoveries exist; blanks are unknown, not zero.

Preserve raw source files. Put any future raw measurement in a clearly dated, sample-ID-labelled raw-data folder before processing it. Record units, transformations, assumptions, exclusions and software version with every derived output.
