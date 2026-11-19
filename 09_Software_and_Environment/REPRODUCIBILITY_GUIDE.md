# Reproducibility guide

## What can be reproduced now

1. Literature arithmetic in `Agastya Physics Simulation\Research Phase B-C\published_data_validation_v3.csv`.
2. Three normalized 1 kg records in `scenario_results_v3.csv`: the 300 ppm review scenario, the 600 g/t publisher-abstract wording, and the unresolved 630 g/t secondary excerpt. The latter is retained to expose the discrepancy, not treated as verified.
3. Nine historical source/range and unknown-input rows in `sensitivity_analysis_v2.csv`; this is not a v3 uncertainty model.
4. The v2 accounting unit suite and legacy-kernel probes.
5. The historical thermal/model dataset using its original scripts and `PROCEDURES_AND_RESULTS.md`.
6. The eight A1/A4 PDFs by running `06_NCSC_Display\Posters\poster_generator.py`, then checking them with `06_NCSC_Display\validate_print_outputs.py`.

Re-run commands and input boundaries are in [Data and analysis guide](../03_Data_and_Analysis/DATA_AND_ANALYSIS_GUIDE.md). Inputs, code, run manifests and outputs should stay together.

## Reproduction checks

- Confirm source ID, DOI and source qualifier before interpreting any literature number.
- Confirm each CSV header and row field count; do not fill empty process values with zero.
- Confirm the v3 model manifest lists its input and outputs, Python version, physical sample count and that process physics was not simulated.
- Confirm 28 v2 accounting tests pass. The separate legacy audit should still show the three recorded validation gaps.
- Compare regenerated files by values, not modification time. Run timestamps may differ.

## Not reproducible as physical claims

No physical test or external solver run is available to reproduce. No raw assay files or sample chain-of-custody records exist. Literature results require their cited study's own methods and feed; reproducing a formula from a paper table does not reproduce that paper's experiment.
