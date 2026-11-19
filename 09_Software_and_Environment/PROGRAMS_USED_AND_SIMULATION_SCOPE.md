# Programmes and simulation scope

## Actual programmes

- CPython 3.14.4 — evidence builder, deterministic scenario arithmetic, published-data checks and accounting validation.
- NumPy 2.5.3 — available and used in the earlier thermal simulation workflow.
- Python standard library — CSV/JSON handling and Phase B/C arithmetic.
- PowerShell 7.6.5 — script launch and file orchestration.
- PptxGenJS — new PowerPoint decks; python-pptx — structure/text inspection; ReportLab — poster/A4 PDFs; Poppler pdftoppm — poster page rendering.

Presentation/document tools are not physics engines.

## Simulation models and row counts

The historical simulation dataset contains 200,080 virtual parameter-scenario or time-history rows: 147,912 initial records and 52,168 follow-up records. It includes Stage 2 scenario arithmetic, a five-node lumped thermal RC model with explicit forward Euler, time traces, timestep comparisons, and assumed particle-size distribution/screen-cut scenarios. Some later silver-grade calculations are conditional on stated assumptions. These rows are not physical specimens, measurements, random samples or statistical replicates.

Phase B/C contains v2 historical scenario/sensitivity outputs and a v3 source-qualified arithmetic run: 300 ppm is an unresolved review scenario, Dias's publisher abstract states 600 g/t, and 630 g/t is retained only as an unresolved secondary excerpt. The v3 output is normalized arithmetic, not a process simulation. It leaves actual process yields and assays blank. The evidence base has 14 records and the route comparison covers five candidates.

## Physical sample counts

Actual AGASTYA physical testing in the available records: 0 panels, 0 coupons, 0 particle samples and 0 assays. No actual sample size was tested. NCSC proposal materials describe possible future sample work only.

## Solver status

No FEM, CFD, DEM, electrostatic field, chemical process or assay solver was run in this continuation. The earlier thermal RC model is a simplified numerical model, not a validated delamination engine. See the run manifests and phase reports for provenance and limitations.

