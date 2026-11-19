# AGASTYA research Phase E

**Prepared:** 13 October 2026  
**Status:** Historical numerical research snapshot. Phase E inherits the 13 October stage map, which the project owner corrected on 16 October. Use the root current architecture for present stage definitions. The preserved Phase E calculations concern the historical thermal model now used as current Stage 3; the old Stage 4 size model does not simulate current silver removal.

**Report collection warning:** The seven source reports and generated PDFs under `Reports/` are preserved from 13 October and contain the then-current electrostatic Stage 3 / assay Stage 4 framing. They are historical records, not current architecture references. The root `AGASTYA_ARCHITECTURE.md`, updated project status and 20 October presentation supersede those stage definitions.

**Scope:** second-round scientific review, focused numerical studies, progress tracking, report collection, and concise Day 24 onward logbook versions.

## Research and computation completed

- Added four source records (E25–E28) to the Phase D evidence register: a full IEA PVPS 2023 hot-knife LCA review, a peer-reviewed PV silver-use paper, and abstract-level thermal-treatment studies from 2015 and 2026.
- Executed PE-SIM-001 on all 5,040 historical thermal cases. Dwell time and contact conductance are the largest main effects for selected model outputs. Equal-weight shares describe the scenario grid only.
- Executed PE-SIM-002 on four selected thermal cases and five mesh levels. An explicit-Euler trial became unstable on finer meshes and is preserved. A backward-Euler finite-volume rerun reproduced the coarse model limit and closed its numerical energy balance.
- Executed PE-SIM-003 for two conditions at 80 control volumes and three timestep values. The largest reported 0.5-to-0.25 ms relative difference across selected outputs was approximately 0.00126%; this is a numerical check, not physical validation.
- Drafted seven technical report sources, generated their A4 PDFs and supplementary appendices, and recorded structural/page/font/text checks in Reports/PDF_QA_REPORT.csv.
- Preserved original Day 24/Day 25 entries and created concise versions. No missing day was invented.

## Evidence boundary

The thermal numerical checks describe the current Stage 3 model concept only. They do not simulate adhesive fracture, peel quality, actual equipment energy, safe operating conditions, Stage 4 silver removal, an assay, or recovered silver. The historical size-classification calculations are at most route/feed-preparation arithmetic. No AGASTYA feed, physical stream, assay, separator trial, recovery, product purity, throughput, process energy, or environmental benefit has been measured.

## Folder map

- Simulation_Campaign/models — reproducible source code and model notes.
- Simulation_Campaign/raw — preserved unstable explicit-Euler outputs.
- Simulation_Campaign/processed — sensitivity, mesh, timestep, and summary data.
- Simulation_Campaign/figures — data plots and diagram sources.
- Reports/Source_Markdown — historical technical report sources.
- Reports/PDFs — A4 report copies.
- Reports/QA_Previews — rendered pages used for visual inspection.
- Logbook — Phase E logbook handling notes.
