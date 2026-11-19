# Agastya Project Logbook: Day 20

**Date:** 7 October 2026  
**Record status:** software/model literature review and roadmap update. No equipment was operated or purchased, no sample was processed, and no model was trained.

## Objective

Continue evaluating the two Stage 4 routes—direct processing of Stage 3 laminate and partner delamination—and decide what software or model Agastya should build or train.

## Work completed

- Reviewed recent NIR hyperspectral imaging research on PV recycling fractions. The study supports investigating material-class mapping and residual EVA detection, but does not establish silver-grade prediction from spectra.
- Reviewed a 2026 hybrid spectral-learning paper and recorded that its hyperspectral features were simulated because the authors lacked HSI hardware; its reported classification accuracy is not evidence of performance on Agastya's Stage 4 fractions.
- Checked the current Agastya-EYE roadmap. Its main gap remains lineage after panels split into streams, batches, aliquots, fractions and assay samples.
- Specified a hardware-independent software path: traceable material lineage, raw assay provenance, mass closure and transparent calculations for grade, recovery, enrichment, specific energy and cost.
- Defined future model candidates: measured process-outcome regression, followed conditionally by HSI material classification. No model should be trained before repeatable, assay-backed field data and validation on held-out panels/batches exist.
- Added a Stage 4 software/model research note and updated the software roadmap and project index.

## Recommendation

Build the lineage and calculation workflow now; defer ML, HSI hardware and machinery controls. Use laboratory assays—not RGB images or an unvalidated spectral classifier—to establish Ag grade and recovery. Keep Route A and Route B as separate process runs with shared traceable records and distinct outcome measures.

## Next step

Review EYE's material-lineage schema and map stream, batch, aliquot, fraction and assay records to the existing event API before implementation. In parallel, establish whether a supervised partner can support both route comparisons and provide the assays needed for a future dataset.
