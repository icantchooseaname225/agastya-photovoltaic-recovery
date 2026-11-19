# Stage 4 Software and Model Research


> **Architecture correction (16 Oct 2026):** Current Stage 4 is silver removal/recovery. This file's size-classification, ECS, assay, or hand-off descriptions are prior route research, not the current stage definition. Treat size reduction/classification as possible feed preparation; assay and mass accounting validate the stage. See [Stage 4 architecture and route decision](STAGE4_ARCHITECTURE_AND_ROUTE_DECISION_2026-10-16.md).

**Review date:** 7 October 2026  
**Scope:** software and data models that support both Stage 4 routes: (A) direct comminution and size classification of the Stage 3 laminate for a mixed silver-bearing hand-off, and (B) partner delamination where intact or cleaner cells are the target.  
**Evidence status:** desk research and review of the current Agastya-EYE implementation. No trial dataset or verified assay/receiver information is available.

## Recommendation

Build the missing **material lineage, assay and mass-balance workflow** into Agastya-EYE. Add a transparent Stage 4 calculation/reporting layer after the data model is agreed. Do not train a prediction model yet, and do not add a new image classifier to claim silver grade or recovery.

The same lineage system supports both physical routes, while their outputs and success criteria remain distinct. Route A needs size-fraction mass, Ag grade and recovery. Route B needs a record of which interfaces were removed, cell integrity, residual polymer and downstream output assay. The software should compare those measured outcomes and costs without presuming that either route is superior.

## Literature implications for software and ML

1. **NIR hyperspectral imaging is a plausible later material-sorting aid.** Neumaier et al. integrate NIR hyperspectral imaging into a PV layer-separation workflow and report detection of residual encapsulant on glass, cells and backsheet, with material mapping/classification. Their article says the supporting data are available from the corresponding author on request. It does not establish that low-level Ag concentration in a mixed fraction can be inferred from spectra, nor that the instrument is suitable for Agastya's vehicle. Treat HSI as a candidate for distinguishing material classes or EVA contamination after partner access, with laboratory assay as ground truth. [Neumaier et al. (2026)](https://doi.org/10.1002/adsu.202501602)

2. **Do not transfer headline accuracy from simulated spectral inputs.** Ragul et al. report a hybrid classification framework, but state that hyperspectral sensing infrastructure was unavailable and spectral features were generated in simulation; real measurements supplied electrical/environmental signals. This is not validated HSI performance on Stage 4 fractions and does not predict Ag grade or process recovery. [Ragul et al. (2026)](https://doi.org/10.1038/s41598-026-64233-0)

3. **Ag distribution and stream composition require measured material accounting.** The Stage 4 literature reviewed in the feed-gap report shows that fine cuts can capture much of the Ag while remaining mixed with Si or other solids. Therefore EYE should calculate Ag inventory from measured fraction mass and assay, not from an image label or a “silver-rich” classification.

4. **Validation must respect panel and batch lineage.** Multiple aliquots or sieve fractions from one panel/batch are related observations. Randomly splitting those rows between training and validation can overstate generalization. When a model is eventually evaluated, hold out entire source panels/batches (and later a site or campaign); grouped cross-validation is designed to keep each group out of both train and test in a fold. [scikit-learn GroupKFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html) [Cross-validation guidance for grouped data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data)

## Software to make now

### 1. Material lineage ledger (highest priority)

Extend the existing EYE record chain from a panel passport and stage event to:

```text
panel -> stage event -> material stream -> pooled batch -> aliquot -> process run
      -> output fraction -> assay sample -> result -> receiver lot
```

Required behaviors:

- Stable IDs; explicit parent IDs for every split, pool, sample and output.
- Record measured input/output mass, wet/dry basis, units, tare, scale/instrument, operator and timestamp.
- Keep raw assay values, method, laboratory, detection limit/uncertainty and chain-of-custody files linked to the exact sample.
- Record the process boundary, settings as observed, energy/time, equipment identity and method version. Do not control machinery from EYE.
- Track residues, dust/filter catch, rejected material and unaccounted loss as separate outputs; never silently make mass disappear.
- Preserve append-only corrections with author, reason and previous value.
- Keep Route A (size fractions) and Route B (delamination outputs) as distinct process-run types and output schemas under common lineage IDs.

This is compatible with the existing Stage 1–4 roadmap and closes its identified gap around one-to-many streams, pooling, aliquots, assays and mass-balance reporting.

### 2. Stage 4 calculation and experiment report (deterministic, not ML)

For each measured run, calculate and show inputs, equations, units and missing-data flags:

- **Mass closure (%)** = 100 × sum of recorded output masses / recorded input mass.
- **Ag inventory in stream** = dry stream mass × measured Ag mass fraction.
- **Ag recovery to selected output (%)** = 100 × Ag inventory in selected output / Ag inventory in feed.
- **Ag grade** = assayed Ag mass fraction in the selected output.
- **Enrichment ratio** = selected-output Ag grade / feed Ag grade.
- **Specific energy** = measured process energy / dry feed mass.
- **Cost per feed mass and cost per recovered Ag mass** only when actual quotes, assays, yields, transport, operator time and waste costs are entered; show every assumption and do not use spot silver price as a receiver quote.

Report each fraction separately, include uncertainty where supplied, and block a measured recovery claim if either required assay or mass is missing. A calculated mass-balance warning should flag closure outside a tolerance set by the supervisor before a trial, not invent a tolerance in software.

### 3. Route comparison worksheet

Compare the routes on the same feed or matched, documented aliquots. Display: accepted target product, mass yield, Ag grade/recovery, cell recovery/integrity where relevant, residual EVA/backsheet/glass, assay uncertainty, energy, time, cost and receiver acceptance. Delamination is not a success merely because EVA product is clean; comminution is not a success merely because Ag reports to fines.

## Model to consider later

### First candidate: process-outcome regression

After repeatable supervised trials, assess a small, interpretable model for measured outcomes such as Ag grade, Ag recovery, mass yield, specific energy and (for Route B) intact-cell fraction/residual-polymer level. Candidate inputs include module/feed type and condition, Stage 3 output description, feed moisture and size, process route, documented settings, cut sizes, duration, equipment, and sampled output mass. Train separate targets; do not collapse them into one opaque “recycling score.”

Start with a predeclared experimental design and simple baselines (mean/linear regression or a small tree model). Compare any more complex learner to those baselines using held-out source panels/batches, assay uncertainty, calibration and prediction intervals. Use a new campaign/site as external validation before using the model for process recommendations. Until then, present scenario calculations as scenarios, not predictions.

### Second candidate: HSI material-segmentation model

Consider only if a partner can provide calibrated NIR hyperspectral measurements paired to physically separated and assayed material labels. Its useful target is likely visible surface class or residual EVA/material mixture, with spot checks against laboratory composition. This may help sorting or quality screening; it cannot replace an elemental assay for silver. RGB photographs can support documentation and coarse visual classification, but should not be used to infer Ag content.

## Data gate before training

No ML model should be trained for Agastya until the project has:

1. A frozen target and decision the prediction will support.
2. Versioned and traceable input features and outputs from actual Stage 4 runs.
3. Representative feed from more than one independent panel/source batch and repeats across conditions; the required quantity should be set by a power/scope analysis once assay variability and expected effect are known, not guessed now.
4. Assay methods, sampling procedure, detection limits and uncertainty; reconciled masses for all outputs and residues.
5. Enough independent groups to hold out complete panels/batches and an untouched campaign/site for final validation.
6. A comparison against simple baselines, error ranges, data drift checks and a defined human review path.

Until the gate is met, the right model is a documented equation-based calculator plus a carefully designed data capture workflow. That is more useful and auditable than training on literature values, simulated spectra, or repeated fractions from a few panels.

## Cost and implementation boundary

No reliable software build cost can be stated until the implementation scope, current database/API constraints and developer effort are estimated. The economical sequence is to reuse EYE's current panel passport, event provenance and append-only records; design lineage first; then implement stream/batch forms, calculation/export and route comparison. Avoid buying HSI hardware or adding a paid ML service until a partner trial demonstrates an operational need and the required labels can be collected. Assay, calibration, partner access and data collection are likely to be the main new project costs, but require local quotes.

The software is a research record and decision-support tool. It must not operate crushers, heaters, lasers, electrical equipment, safety interlocks or emergency stops.

## Build sequence

1. Review the lineage schema and ID rules against EYE's current records and Stage 1–4 interoperability contract.
2. Implement material stream, pooled batch, aliquot, process run, fraction and assay records with audit history.
3. Add mass closure and assay-backed grade/recovery/enrichment calculations with downloadable CSV/JSON and a human-readable run report.
4. Use the same forms during supervised Route A and Route B comparisons; add fields only when the protocol defines a real measurement.
5. Reassess HSI access and ML only after the data gate is met.

## References

- Neumaier, L. et al. (2026). “NIR Hyperspectral Imaging for Advanced Identification and Quantification of Materials in PV Recycling Fractions.” *Advanced Sustainable Systems*. [DOI](https://doi.org/10.1002/adsu.202501602)
- Ragul, S. et al. (2026). “Hybrid spectral learning framework for real-time material classification of end-of-life photovoltaic panels.” *Scientific Reports*. [DOI](https://doi.org/10.1038/s41598-026-64233-0)
- scikit-learn documentation. [GroupKFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html); [cross-validation for grouped data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data)
- See [Stage 4 feed-gap repair research](STAGE4_FEED_GAP_REPAIR_RESEARCH.md) for the mechanical/delamination process evidence and PV recycling references.
