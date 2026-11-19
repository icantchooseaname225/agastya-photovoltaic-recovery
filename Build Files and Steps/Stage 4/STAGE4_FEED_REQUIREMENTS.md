# Stage 4 Feed Requirements and Next Steps


> **Architecture correction (16 Oct 2026):** Current Stage 4 is silver removal/recovery. This file's size-classification, ECS, assay, or hand-off descriptions are prior route research, not the current stage definition. Treat size reduction/classification as possible feed preparation; assay and mass accounting validate the stage. See [Stage 4 architecture and route decision](STAGE4_ARCHITECTURE_AND_ROUTE_DECISION_2026-10-16.md).

**Prepared:** 3 October 2026  
**Status:** design decision and experiment definition; no Stage 4 feed has been processed.

## Decision needed before a Stage 4 machine can be specified

The Stage 4 separator cannot be sized until its input is defined. The current Stage 3 baseline produces two streams:

1. front glass; and
2. cell/EVA/backsheet laminate.

The thesis instead assumes that Stage 3 supplies EVA-stripped cell material. The current research recommendation does not require that assumption for size-based pre-concentration. The proposed heated roller has not been validated, and the hot-knife literature does not by itself create liberated metal particles. The current Stage 3 output is therefore **not an eligible Stage 4 ECS feed**, but it is the proposed feed for a separate, assay-based comminution and size-classification study.

## Recommended first Stage 4 objective

Start with a narrow objective: characterize the Stage 3 output and determine the target product before selecting a separator. The thesis's eddy-current objective only makes sense for a defined, dry, liberated conductive-particle feed. It cannot be used to infer silver separation from intact cell fragments.

The new [Feed-Gap Repair Research](STAGE4_FEED_GAP_REPAIR_RESEARCH.md) resolves the first design ambiguity: complete EVA removal need not be a prerequisite if Stage 4 targets a mixed silver-bearing concentrate. The first hypothesis is contained, controlled comminution and multi-cut size classification directly on traceable Stage 3 laminate, with representative assay of every fraction. If supervised equipment becomes available, compare size classification alone with controlled comminution plus classification on equivalent feed. Then match any additional separator to the measured stream: ECS only for eligible liberated coarse conductors; electrostatic sorting only for dry, prepared fines; flotation only through a qualified lab route. This is not permission to improvise a crusher or process PV glass without controls.

The study feed should be a traceable Stage 3 output; initially document chemistry/module identity, particle-size distribution, dryness, and polymer/glass carryover. Do not describe it as EVA-free or liberated unless that state is measured. Do not call a mixture of cell fragments and printed contacts a silver-rich metal feed without composition analysis.

## Feed classes and claims

| Feed class | Suitable purpose | Claims it can support | Claims it cannot support |
|---|---|---|---|
| Known reference Al/Cu pieces plus inert nonconductive media | Check sample tracking, mass balance, separator trajectory and repeatability using safe, known constituents | Performance on the specific reference blend and separator settings | PV module recycling performance, silver recovery, or silicon recovery |
| Characterized liberated PV-derived conductors and nonconductive fragments | Research the actual Stage 4 pathway once the upstream process and lab controls exist | Measured mass split and composition-based grade/recovery for the documented feed | Broad performance across all module designs or pure products without adequate evidence |
| Current Stage 3 glass-separated cell/EVA/backsheet laminate | Candidate input for controlled comminution + multi-cut sieving; not an ECS feed | Assay-based size-fraction distribution and measured Ag grade/recovery for this documented feed | EVA-free cells, free Ag particles, or ECS separation performance |

## Minimum acceptance checks for a future PV feed

Before loading material, a supervisor-approved protocol must confirm all of the following:

- chemistry is identified as c-Si; unknown and thin-film materials are excluded;
- the material is dry, contained, and sampled under appropriate glass/dust controls;
- the feed comes from a documented process and the remaining EVA/backsheet fraction is measured or described;
- particle-size bins and liberation state are recorded;
- all feed, product, middlings and residue can be retained, labelled, weighed and reconciled;
- a suitable assay (for example, calibrated XRF or a qualified laboratory method) is available to identify metals and quantify composition;
- the separator is enclosed/guarded and its electrical, rotating-part, dust and emergency controls have been reviewed for the actual site.

If any item is missing, keep the Stage 4 feed at the reference-mixture stage and record the PV feed as not ready.

## Experiment variables to freeze before a pilot

For each aliquot, set and record:

- sample identity, source and upstream Stage 3 event;
- particle-size range and mass;
- moisture/dryness condition and visible contamination;
- ECS model/configuration, rotor speed (rpm), belt/feed speed, feed rate, splitter position and magnetic arrangement;
- number of passes and whether the feed was screened or pre-cleaned;
- feed, conductive product, nonconductive product, middlings and retained residue masses;
- energy used, timing, operator, scale/meter IDs and calibration/check references;
- composition assay method, sample preparation, laboratory/instrument ID and result uncertainty.

Keep one untreated aliquot as the baseline. Repeat each selected condition on independent aliquots. Do not adjust multiple separator settings at once during initial comparisons.

## Calculations and reporting

- `mass_closure_percent = 100 × (sum of all collected output masses / input mass)`
- `target_metal_recovery_percent = 100 × (target metal mass in selected product / target metal mass in feed)`
- `product_grade_percent = 100 × (target metal mass in selected product / selected product mass)`
- `enrichment_ratio = product grade / feed grade`
- `specific_energy = measured electrical energy / input feed mass`

Mass closure needs a scale; metal grade and recovery need composition data. A mass split, photograph, or magnet response alone is not an assay. Always report both grade and recovery because improving one can reduce the other.

## EYE software hand-off

EYE's existing passport is keyed by stable `panel_id`; a Stage 4 record is appended to the same panel passport after a Stage 3 completion event. Use a unique `event_id`, timezone-aware time, station and operator IDs, plus instrument and calibration references. `rpm` is now a supported unit. EYE stores the record; it does not authorize the separator or act as a safety controller.

For batch feed derived from multiple panels, do not hide the batch identity in free-text alone. Preserve a batch manifest mapping every source `panel_id` and Stage 3 output event to the Stage 4 aliquot/run IDs. A later schema change could give batch IDs first-class support; until then, keep that manifest as a linked research record and include its stable ID in each event note.

## Next actions

1. Use [the Stage 4 method comparison and calculations](STAGE4_METHOD_COMPARISON_AND_CALCULATIONS.md) to choose the target product and compare published yields without treating them as Agastya results.
2. Inventory available school/lab equipment without purchasing anything using [the equipment-access template](STAGE4_EQUIPMENT_INVENTORY_TEMPLATE.csv); identify supervised access to size classification, guarded separators and composition assay.
3. Ask the supervisor to review the feed acceptance checklist and available facility controls.
4. Close the Stage 3-to-Stage 4 boundary: record whether the actual output is laminate, delaminated pieces, liberated fragments or powder; do not assume the proposed roller works.
5. If appropriate supervised equipment and eligible feed exist, adapt [the blank trial-log template](STAGE4_TRIAL_LOG_TEMPLATE.csv) and EYE event record to their real instruments and ranges. Otherwise continue with design research and no-spend planning.


