# Agastya Stage Software Roadmap

**Reviewed:** 20 October 2026  
**Purpose:** plan traceability and record software for Stages 1–4. This is a product/data roadmap; it does not authorize or control machinery.

**Current process map:** Stage 1 inspection/routing; Stage 2 manual mechanical preparation; Stage 3 thermal treatment/delamination; Stage 4 silver removal/recovery, with method and feed preparation open. The root current architecture controls. Earlier Stage 4 software/model research is route-comparison material and carries a 16 October correction banner.

## Recommendation

**Yes, continue software work, but focus on traceability and operator records across the stages. Do not prioritize robot automation, automatic stage control, or more AI classifiers yet.** EYE already has a panel passport, human-reviewed Stage 1 routing, and append-only Stage 2–4 events. The main software gap for recycling is lineage once one panel becomes multiple material streams, pooled batches, fractions and assay samples.

The present record model is centered on one `panel_id`. Stage 4 material may combine outputs from several panels, while a single Stage 3 output may split into several products. This data design does not select the Stage 4 process. A free-text note or spreadsheet manifest can bridge an early pilot, but it is fragile and cannot support reliable roll-up calculations without disciplined IDs. This is the best next software design target because it supports Stage 2 output, Stage 3 streams, and Stage 4 fractions without assuming a separator model.

## Current state by stage

| Stage | Current software support | Main gap | Priority |
|---|---|---|---|
| Stage 1 — inspect and route | Panel passport; image/view provenance; measured dimensions/electrical evidence; human review; recommended and final route; research classifiers kept advisory | Field validation and operator data quality remain more important than adding models. No automatic PLC motion or safety decision. | Maintain and improve provenance/field usability only when real pilot feedback exists. |
| Stage 2 — de-frame/de-junction | EYE requires approved Stage 1 route/isolation before accepting Stage 2 process events; event records carry measured mass and instrument provenance | No first-class material-output/stream tree; physical robot/tool recipe and safety controls do not exist in the software and should not be implied. | Capture parent panel, separate aluminium/J-box/cable outputs and residual laminate as traceable streams. |
| Stage 3 — thermal separation | Stage 3 completion is gated on Stage 2 completion; calibrated temperature/mass/duration observations can be recorded; app does not operate heater | Glass, laminate and any later liberated-cell stream need explicit child IDs and measured mass links; thermal trials still need instrumented records. | Add stream/child identity when a real Stage 3 trial establishes the outputs. |
| Stage 4 — silver removal/recovery | Stage 4 is gated on Stage 3 completion; events can include `rpm`, mass, energy and assay values with instrument/calibration provenance | Batch/aliquot/fraction lineage is external; no built-in mass-balance/recovery report; no verified trial dataset. | Highest-value software design after a real pilot defines the outputs: batch manifest and parent-child sample lineage, then a report using measured assays. |

## Proposed software sequence

### SW-1 — Define material lineage before changing the database

Specify stable IDs and parent-child relationships for:

```text
panel -> stage event -> material stream -> batch -> aliquot/fraction -> assay sample -> receiver lot
```

Rules:

- An output stream has exactly one operation/event as its parent.
- A batch may pool multiple streams only with a recorded list of parent IDs and input masses.
- An aliquot/fraction records its parent sample, preparation step, dry mass, size range and method.
- An assay result references the exact sample ID plus method, lab/instrument, calibration, date and units.
- A material stream can split into multiple outputs; retain all outputs and measured losses rather than overwriting the input.
- Preserve existing panel passports and event hashes; design migration/compatibility before implementation.

### SW-2 — Build an operator workflow for material hand-off

After the schema review, add forms that create stream IDs, record input/output mass, attach photos/files, link parent records, and flag incomplete mass closure. Keep scientific metrics separate:

- Mass closure needs every output and a declared loss/residue.
- Grade and recovery need measured assay values, not only mass.
- Enrichment compares assayed product grade to assayed feed grade.
- Estimated, unassayed results must be labeled estimates and cannot appear as measured recovery.

### SW-3 — Export and summarize

Provide a per-batch trace report with the parent-panel list, stage-event IDs, feed/stream masses, assay results, missing-data flags and calculated metrics. Export machine-readable CSV/JSON plus a human-readable summary. Do not add a revenue/payback calculation until a receiver specification and fee/price inputs are real.

### SW-4 — Fit forms to real pilots

Only after Stage 2/3 equipment and Stage 4 feed are defined, add stage-specific fields for actual station instruments, settings, holds and quality checks. Keep raw measurements immutable; corrections become reviewed amendments rather than silent edits.

### SW-5 — Defer automation and model expansion

Robot motion, hot-knife control, any selected Stage 4 equipment, interlocks, and emergency stops belong in qualified PLC/safety hardware and a site-approved system design. EYE can submit records or advisory results but must not own the safety function. Additional models should wait for representative, rights-cleared field data and validated target labels.

For Stage 4, implement an equation-based mass-balance and assay calculator before any ML. Potential later models are (1) process-outcome prediction from measured, repeated, panel/batch-linked trials and (2) NIR hyperspectral material classification if a partner provides calibrated spectra and physical labels. Neither model can infer silver grade from ordinary RGB images; elemental assay remains the ground truth. Evaluate any trained model by holding out complete panels/batches, not random fraction rows.

### SW-6 — Add an educational visual walkthrough

EYE includes **How stages work**, an explanatory visual walkthrough for Stage 2 preparation, Stage 3 front-glass separation, and a Stage 4 silver-removal route gate. The Stage 4 method and output form remain open. The animation does not operate equipment, simulate measured performance, or imply that conceptual stations are validated.

## Go/no-go for starting implementation

The batch/stream design can begin as a bounded, hardware-independent software task. Before database/API implementation, freeze:

1. ID formats and parent-child rules;
2. mass units and wet/dry basis;
3. pooling/splitting and correction behavior;
4. assay result provenance and uncertainty fields;
5. backward compatibility with panel passport schema 1.x;
6. export requirements for the first real trial.

Do not implement machine-specific controls or invent settings while the Stage 4 readiness audit remains open. The current status is **design now; implement lineage first; add process-specific screens after a real pilot protocol exists**.
