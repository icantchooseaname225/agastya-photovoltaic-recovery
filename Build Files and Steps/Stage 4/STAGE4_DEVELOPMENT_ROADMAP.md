# Stage 4 Development Roadmap


> **Architecture correction (16 Oct 2026):** Current Stage 4 is silver removal/recovery. This file's size-classification, ECS, assay, or hand-off descriptions are prior route research, not the current stage definition. Treat size reduction/classification as possible feed preparation; assay and mass accounting validate the stage. See [Stage 4 architecture and route decision](STAGE4_ARCHITECTURE_AND_ROUTE_DECISION_2026-10-16.md).

**Updated:** 7 October 2026  
**Status:** next-step plan; no equipment, feed processing or separation performance has been demonstrated.

## Decision from the thesis and literature review

See [Stage 4 Model Critique and Alternatives](STAGE4_MODEL_CRITIQUE_AND_ALTERNATIVES.md) for the detailed risk review, alternative routes, evidence notes and qualitative cost comparison.

The current Stage 4 goal is silver removal/recovery from Stage 3-derived cell-bearing material. The earlier “mobile, chemical-free pre-processing” framing is not the controlling architecture. The thesis's rotating eddy-current separator, dry size classification, flotation and extraction studies are candidate route or feed-preparation evidence; none is selected for AGASTYA. Silver-specific studies use prepared feed and specialist equipment, and results cannot be transferred without a matched feed and assay.

**Current Stage 4 design question:** which qualified process can remove/recover silver from the actual Stage 3 output, and what additional feed preparation does it require? Characterize the laminate first, define the desired silver-bearing product form, then compare the documented physical and chemical routes with a qualified facility and receiver. Dry comminution/sieving may prepare or preconcentrate feed; they do not by themselves meet the silver-removal objective. See [Feed-Gap Repair Research](STAGE4_FEED_GAP_REPAIR_RESEARCH.md) for evidence that remains useful as route analysis.

This is a research direction, not a final technology selection. The next decision depends on actual Stage 3 output, sample characterization, partner-lab access and a receiver's acceptance specification.

## Candidate flowsheet and material boundaries

```text
Stage 2: isolated, identified c-Si module
  -> Stage 3: front glass + cell/EVA/backsheet laminate
  -> define route-specific feed preparation, if needed
  -> Stage 4 silver-removal/recovery process at a qualified facility
       -> silver-bearing product/solution or recovered solid, as specified
       -> residual solids, residues and waste streams, all measured and routed

Optional partner route if intact cells are the target:
  Stage 3 laminate -> backsheet/EVA delamination study -> characterize remaining layers
  -> documented solid fraction(s) handed to qualified central refiner
```

The Stage 3 output is not proven EVA-free and the heated roller is not validated. This is a feed-interface gap for Stage 4. Specify any added delamination, liberation or size-classification operation as feed preparation for the selected silver-removal method; do not label pre-concentration alone as silver removal.

## Work sequence and gates

### Step 1 — Freeze the output question

Keep the target aligned to the system: produce a **smaller, dry, traceable silver-bearing solid fraction**, not elemental silver. Write the receiving partner's required material form, prohibited contaminants, packaging, minimum batch mass and assay requirements once a real receiver is identified. Until then, treat “central-refiner hand-off” as a design requirement with an open acceptance specification.

### Gate 1 — Feed readiness

Before any separator selection, verify from the real process or a qualified partner:

- c-Si identity and source module;
- actual Stage 3 output state (laminate, delaminated cells, liberated fragments or powder);
- dry mass, moisture condition, size distribution and visible glass/polymer carryover;
- whether silver-bearing conductors are still attached to silicon or polymer;
- safe containment, supervision, guarding and site controls for any downstream size reduction.

**Pass:** traceable, eligible material and approved method for preparing it. **Fail:** remain at design review; no PV crushing, screening or separator trial.

### Step 2 — Freeze the comparison and measurement plan

On paper, define a baseline dry size classification and one alternative that addresses the chosen target. Record before a test: feed provenance, sample division method, size bins, scale resolution, all expected output streams, assay method, repeat plan, energy boundary and acceptance criteria. A mass-only split cannot demonstrate silver enrichment; assay must quantify silver in representative feed and output samples.

**Pass:** all feed and product streams can be retained, weighed, sampled and reconciled; assay access is confirmed. **Fail:** do not claim a recovery or grade result.

### Step 3 — Access and cost check (no procurement yet)

Verify whether a university, recycling partner or supervised school facility can provide the necessary guarded equipment, sieves, balance, containment and assay. Mark each item `available`, `borrowable`, `quote requested`, or `unavailable` in the equipment inventory. Do not replace unknown values with online hobby-machine prices.

**Pass:** named equipment, responsible supervisor, safe operating envelope and written access/quote status. **Fail:** keep Stage 4 as a design study and do not build.

### Step 4 — Baseline demonstration, then method comparison

If Gates 1–3 pass, use the facility-approved protocol to establish mass closure on traceable feed, then compare the baseline size split with the selected candidate method on equivalent aliquots. A known reference mixture can validate the weighing and record workflow but does not count as PV performance. If an ECS is included, first confirm it accepts the actual size, shape and material range; test it separately and determine whether it improves the target fraction's assay result relative to size classification alone.

Record all products, middlings and retained losses. Report feed/product grade, target recovery, enrichment, mass closure, uncertainty and measured energy separately. Stop or revise if the method fails the receiver specification or adds no measured benefit.

### Step 5 — Mobile integration decision

Only after a repeatable bench result, assess envelope, mass, power, dust containment, collection/packaging, operator handling and service needs against the mobile chassis. Build a Stage 4 equipment specification and cost estimate from actual supplier or lab quotes. Do not claim full mobile throughput or profitability until the integrated line is measured.

## How methods fit the Agastya target

| Method | Fit to dry onboard pre-concentration | Decision |
|---|---|---|
| Controlled comminution + multi-cut sieving | PV evidence supports directing much of the total Ag into fine fractions without first burning off encapsulant; the fraction remains mixed | Primary candidate for supervised feasibility study on the documented laminate, only after feed and dust/glass controls are resolved |
| Multi-cut comminution and sieving | A 2024 study reports Ag in <0.25 mm fines and Cu primarily in a 0.5–2 mm cut, but with substantial glass/polymer co-presence | Compare multiple fractions by mass and assay; do not use size cut alone as a grade or purity claim |
| Rotating ECS | Can sort eligible liberated conductive particles; does not extract printed Ag from intact silicon fragments | Preserve as conditional secondary test; not the assumed core |
| Fixed high-frequency EDX | Fine-particle research evidence, but specialized system and reported energy demand are materially different from a simple rotating drum | Do not use its performance or cost as a drum specification |
| Electrostatic roll separation | Can enrich classified PV powder for silicon, but needs high voltage and dedicated apparatus | External-lab option if silicon-rich product is an explicit target |
| Gas-solid fluidized bed | Can separate already liberated coarse cells from glass by shape/density; the cited study used upstream 500 °C pyrolysis for liberation | Partner-lab comparator only; pyrolysis is outside the onboard boundary and this does not recover Ag from cells |
| Corona drum electrostatic separation | Recent MSc work combines controlled milling and size-class-specific corona separation; the fine fraction showed >80% recovery across product classes at ~53% Si grade | Useful partner-lab comparator only; specialized 30 kV unit and thesis-level evidence |
| High-voltage pulse crushing | Can liberate/enrich PV fractions, with a grade/recovery trade-off | External-lab option only; not a school build |
| Froth flotation | Strongest recent silver-specific result reviewed, but requires water, reagents and lab equipment | Central/partner-lab benchmark only; outside onboard process |
| Localized electrolyte-jet extraction | 2026 study reports >95% surface-silver separation using circulating 12 wt% nitric acid | Refiner-side chemical route only; reinforces that Agastya's hand-off is a characterized solid, not recovered elemental silver |

## Stage 4 cost model to populate after access or quotes

There is no defensible Stage 4 total cost yet. Obtain or measure each line below, with date, supplier/lab, tax, freight and whether an item is purchased, borrowed or charged per use.

| Cost line | Basis to record | Current status |
|---|---|---|
| Liberation/size-reduction equipment or lab fee | Quote or facility fee; include containment and dust extraction if required | Unknown |
| Sieves and sample containers | Aperture, material, certificates/check, and per-run consumables | Unknown |
| ECS/EDX/electrostatic equipment | Model, accepted feed envelope, quoted price or access fee | Unknown; no procurement decision |
| Mass measurement and assay | Balance resolution/calibration, sample preparation, XRF/ICP/lab fee per sample | Unknown |
| Electrical energy | Metered kWh per run; later multiply by applicable tariff | Not measured |
| Recurring supplies and upkeep | Containers/labels, screen cleaning, dust-collector filters, PPE, wear parts and maintenance | Not measured; “no process chemicals” does not mean “no consumables” |
| Transport and waste | Actual sample transport and residual/contaminated waste handling | Unknown |
| Labour and supervision | Person-hours and facility/supervisor charge | Unknown |

Once data exist:

```text
Stage 4 operating cost per batch = facility + assay + consumables + transport + waste + measured electricity + labour
Specific operating cost = operating cost per batch / dry feed mass
Specific energy = measured electricity (kWh) / dry feed mass (kg)
Annualized equipment cost per kg = (capital cost × capital-recovery factor) / annual dry-feed throughput
```

Do not estimate recovered-material revenue until measured feed assay, product assay, product mass, receiver specification and an actual price/processing-fee basis are known.

## EYE traceability

Use EYE for panel and Stage 3 provenance, then keep a stable Stage 4 **batch manifest** that maps source panel IDs and Stage 3 output events to every preparation aliquot, size fraction, separator run, assay sample and receiver batch. Append the Stage 4 event to the source passport where the schema permits; store the manifest ID with each event. Record raw measurements and instrument/calibration IDs. EYE is the record system; it is not a separator controller, safety interlock or chemical assay.

## Immediate next action

No purchase or physical trial is currently justified. The next actionable project step is a verified equipment-and-partner-access inventory, followed by confirmation of actual Stage 3 feed availability and a refiner/assay acceptance specification. The inventory template is blank because no facility access has yet been verified.

The desk review cannot verify actual school or partner-lab inventory. See [the 6 October readiness audit](STAGE4_READINESS_AUDIT_2026-10-06.md) for the present evidence status and a checklist for that real-world access check.





## Reassessment — 2026-11-19

Use [STAGE4_ARCHITECTURE_REASSESSMENT_2026-11-19.md](STAGE4_ARCHITECTURE_REASSESSMENT_2026-11-19.md) as the current route comparison. Conventional rotating ECS is not the default; dry size classification is the low-complexity baseline, flotation is conditional on qualified access and compatible prepared feed, and liberation is proposed adjacent to Stage 3 pending matched measurements.
