# Agastya Project Logbook: Day 16

**Date:** 7 October 2026  
**Record status:** software architecture review and roadmap only. No EYE source code or database was modified; no tests were run.

## Objective

Assess whether software work for the other Agastya stages should continue while Stage 4 equipment/feed readiness is unresolved.

## Work completed

- Reviewed the EYE README and stage interoperability contract, plus the Stage 1 readiness/build notes and current Stage 4 readiness documents.
- Confirmed EYE already records Stage 1 inspection and human-reviewed routing, and accepts Stage 2, 3 and 4 append-only measurement/process events with instrument provenance and stage-order checks.
- Identified the main cross-stage software limitation: records are panel-passport centered. Once a panel's material splits into several streams or several panels' streams are pooled into a Stage 4 batch, sample lineage relies on a separate manifest rather than first-class IDs.
- Created `../Agastya-EYE/docs/STAGE_SOFTWARE_ROADMAP.md` with staged recommendations for material-stream lineage, operator hand-off workflow, mass-balance/assay exports, pilot-specific forms and deferred automation.
- Added the software roadmap and Days 15–16 entries to the project index.

## Recommendation

Yes, continue software work, but prioritize a hardware-independent data-model design for panel → process event → material stream → batch → aliquot/fraction → assay sample → receiver lot. Implement that lineage only after ID, pooling/splitting, correction, unit, assay-provenance and backward-compatibility rules are frozen.

Do not spend the next software effort on robotics, thermal/ECS control, PLC safety functions or additional AI classifiers. EYE is a passport and measurement interface; physical safety and machine controls require separate qualified hardware. Screen-specific workflows should follow an actual Stage 2/3/4 pilot protocol.

## Logbook continuity note

The project folder contains entries through Day 13 and did not contain a Day 14 entry during this review. Day 14 has not been reconstructed because its work and date are not documented. Days 15 and 16 record two work-log sessions completed on 7 October 2026; they do not claim separate calendar dates.

## Next step

Draft the batch/stream data model and migration plan before editing the EYE database or API. Keep physical trial plans gated on feed, equipment, supervisor, assay and receiver confirmation.
