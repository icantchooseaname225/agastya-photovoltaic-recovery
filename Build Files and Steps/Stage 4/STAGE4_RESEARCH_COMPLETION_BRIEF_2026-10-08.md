# Agastya Stage 4 — Research Completion Brief


> **Architecture correction (16 Oct 2026):** Current Stage 4 is silver removal/recovery. This file's size-classification, ECS, assay, or hand-off descriptions are prior route research, not the current stage definition. Treat size reduction/classification as possible feed preparation; assay and mass accounting validate the stage. See [Stage 4 architecture and route decision](STAGE4_ARCHITECTURE_AND_ROUTE_DECISION_2026-10-16.md).

**Desk-review date:** 8 October 2026  
**Purpose:** consolidated Stage 4 decision after reviewing the thesis, PV separation literature, Stage 3 feed boundary, alternatives, feasibility, costs and EYE software needs.  
**Status:** literature/design phase complete for now. This is not a physical-readiness approval, process validation, equipment specification or purchase authorization.

**Research update, 9 October 2026:** added one newly published sonochemical study below. It reinforces the separation between dry pre-concentration and downstream extraction; it does not change the Stage 4 recommendation.

## Decision in brief

The current AGASTYA Stage 4 function is **silver removal/recovery**. The previously reviewed eddy-current concept and dry size-classification route do not, by themselves, establish silver removal from a cell/EVA/backsheet laminate. They remain possible feed-preparation or physical-separation comparators. The Stage 4 route, feed specification and silver-bearing product form are still open.

The first next research action is to define the Stage 4 output and characterize the actual Stage 3 stream. The hot-knife baseline yields a cell/EVA/backsheet laminate, so any additional liberation or polymer removal needed for silver removal must be specified explicitly. Compare dry preparation, flotation and chemical/electrochemical extraction against this feed, facility capability, hazards, waste, assay QA/QC and receiver requirements. Do not treat literature yields or cut sizes as AGASTYA performance.

The reviewed froth-flotation and chemical/electrochemical studies are silver-removal route comparators, not an approved school or mobile process. They use prepared feed, specialist equipment and process-specific safety and waste controls. They may inform partner-lab evaluation if a suitable facility accepts the material.

**Current gate result: no physical Stage 4 PV trial and no equipment build yet.** Actual feed, supervised access, dust/glass controls, suitable assays and receiver acceptance remain unverified in the project records. This means their status is unknown, not that such resources do not exist.

## What the thesis says and the corrected boundary

The thesis section 3.4.5 proposes that “freed, EVA-stripped” silicon cell material with printed Ag/Al contacts and fine glass passes a rotating magnetic drum. It says conductive Ag-bearing silicon fragments are repelled farther than nonconductive particles, with optional electrostatic polishing. Its stage safety section identifies rotating equipment and guards but does not establish particle liberation, assay performance or the real feed envelope.

The current Stage 3 baseline separates front glass and leaves a **cell/EVA/backsheet laminate**. A proposed heated roller is not validated. That laminate is not established as ready for any silver-removal route without feed characterization. The current boundary is therefore:

```text
Stage 3 front-glass separation
  -> documented cell/EVA/backsheet laminate
  -> external, supervised feed characterization and preparation study
  -> route-specific additional preparation if required
  -> Stage 4 silver-removal/recovery operation at a qualified facility
  -> silver-bearing product/solution and residual material, each measured and characterized
```

Stage 4's defensible output claim depends on the selected method: it may be a silver-bearing concentrate, solution or recovered solid. Do not claim elemental silver purity, saleability or a recovery percentage without route-specific AGASTYA measurements.

## Options ranked by the output Agastya wants

| Target | Best-supported option | What the evidence says | Fit to Agastya now |
|---|---|---|---|
| Smaller dry Ag-bearing hand-off fraction | Controlled comminution + multi-cut sieving, tested at a qualified facility | PV studies show substantial Ag can report to fines; other material remains in those cuts. Sim et al.'s 70–80% and Juyo Salazar et al.'s 94.12% describe Ag distribution into fractions, **not Ag product grade**. | Best-aligned hypothesis, but unverified on Agastya's laminate; requires containment, sampling, assay, receiver criteria and a partner facility. |
| Coarse non-ferrous conductive pre-sort | Conventional rotary ECS, only after suitable liberation and size classification | Established for the right conductive-particle/non-conductor split; not demonstrated as silver-from-silicon separation. Fixed-frequency EDX results are a different machine architecture. | Conditional later comparison, not core Stage 4 and not a feed-in of the current laminate. |
| Intact or cleaner cells / EVA removal | Mechanical backsheet/EVA peel, heat-assisted or laser interface debonding at a partner | Published work addresses specific interfaces; it does not establish a complete mobile delamination chain for Agastya. Some reported full sequences add a 400 °C step. | Separate partner workstream only if intact cells or polymer separation is an explicit requirement. |
| Silver-rich concentrate | Delamination + grinding + froth flotation in a specialist lab | 2026 study reports rougher tap-water recovery 97.55% with 32.2× upgrade; a separate rougher-cleaner result reports about 47 wt% Ag at 86.5% recovery. It uses real delaminated cells, reagents, water, grinding and ICP-MS/TIMA characterization. | Best silver-specific benchmark, but not dry/onboard and not a school-built route. Potential lab collaboration/receiver benchmark only. |
| Si-rich or cell-rich stream | Controlled crushing/classification followed by electrostatic, gravity or fluidized-bed separation | Studies show selected fractions can be enriched, with grade/recovery trade-offs and machine-specific feed conditions; some require pyrolysis or high voltage. | Specialist lab comparison only if a named receiver wants Si/cells. Does not solve silver purity. |
| Elemental Ag recovery | Central refinery or specialist downstream processing | High extraction figures in studies generally include chemical/electrochemical steps or further processing. | Outside current Stage 4. Do not say Agastya recovers elemental silver. |

## Literature updates and interpretation

- The 2026 IEA PVPS update, based on commercial and pilot-scale recycler inventories, says mechanical recycling remains the dominant commercial c-Si approach; thermal/chemical combinations can reach higher recovery and purity, while gaps remain in electricity consumption, output-quality characterization and harmonized boundaries. That supports Agastya's modest mechanical hand-off ambition but underscores why comparable energy/cost/quality data are still missing. [IEA PVPS Task 12, April 2026](https://iea-pvps.org/key-topics/t12-advances-module-recycling-3rd-edition-2026/)
- The 2026 flotation study is a useful new benchmark for the *silver-specific* target. It processed delaminated and ground cells, with a prepared 3.5 kg feed sample and fine grinding; its metrics come from small laboratory cells. Keep the two reported rougher and rougher-cleaner results attached to their own test conditions; do not combine them into a single expected performance. [Saffarian, Galvin & Firouzi (2026)](https://doi.org/10.1016/j.mineng.2026.110189)
- The 2025 IEA PVPS status report's pilot examples show multi-technology delamination lines, including water-jet and mechanical/optical routes. These are useful partner architecture leads, not evidence of locally available service or a copyable small mobile process. [IEA PVPS Task 12 status report (2025)](https://iea-pvps.org/wp-content/uploads/2025/07/IEA-PVPS-T12-31-2025-REPORT-Status-Module-Recycling.pdf)
- A 16 September 2026 sonochemical study compared mechanical milling, 500 °C pyrolysis and acetone pretreatment with several leachants. Its <0.05 mm fraction (13.4–14.4% of total mass) held the highest concentrations of most measured elements, while the highest Ag recovery used pyrolysis followed by nitric-acid leaching. This is additional evidence that fines can carry valuable metals, but its strongest Ag result depends on thermal/chemical treatment and cannot be claimed for dry sieving alone. [Yandem et al. (2026)](https://doi.org/10.1007/s10098-026-03606-5)
- The Stage 4 size-classification literature remains relevant but is feed- and process-specific. The fine fraction may include silicon, glass, polymer and metal. Report grade, recovery, mass yield and enrichment separately; no percentage of total silver reporting to a size cut should be described as product purity.
- NIR hyperspectral imaging may later support surface-material classification or residual-EVA checks. The reviewed 2026 study does not establish Ag-grade prediction. Ordinary RGB imagery is not a silver assay. See the [software/model research note](STAGE4_SOFTWARE_AND_MODEL_RESEARCH.md).

## Proposed study only after real-world gates pass

This is a design outline for a qualified, supervisor-approved facility, not an instruction to operate a crusher or separator.

1. **Identify target and receiver:** written receiving spec for material form, prohibited contaminants, batch size, packaging and assay.
2. **Verify feed:** c-Si identity and source, Stage 3 parent event, measured dry mass/moisture, size distribution, layer carryover and representativeness.
3. **Verify facility:** named supervisor, allowed equipment/process envelope, suitable enclosure/dust and sharp-glass controls, sample storage and waste procedure.
4. **Secure assay:** method and quote for feed and each product fraction, sample preparation, detection limits/uncertainty, and an agreed sampling/mass-closure tolerance.
5. **Baseline and comparison:** characterize an untreated aliquot; compare size classification alone and controlled comminution plus the same cuts on matched aliquots. Add delamination only as a separate arm if intact cells are the target. Add ECS only if the feed matches its documented envelope.
6. **Retain every output:** all cuts, middlings, filter/dust catches, samples and residues receive IDs, mass and disposition. Account for sample withdrawals and retained losses.
7. **Report:** mass closure, Ag grade, Ag recovery, enrichment, mass yield, uncertainty, energy, time, cost, cell/Si distribution if relevant, and receiver acceptance. Compare against untreated feed and the extra operation's burden.

### Predeclared decision rule

Continue with the lowest-complexity route that (a) is accepted by the named receiver, (b) shows repeatable assay-backed improvement over untreated feed, (c) closes mass within a tolerance agreed before work, and (d) can be performed within the approved facility and mobile boundaries. Keep an ECS only if it adds measurable benefit over the same feed after size classification. If no receiver accepts the mixed fraction, treat Stage 4 as research pre-concentration and send material through a qualified recycler's route rather than claim a marketable product.

## Components and cost status

| Cost block for a future approved study | Minimum function | Cost basis now |
|---|---|---|
| Partner/facility access | Enclosed, supervised feed preparation and classification; optional eligible separator | Unknown. Request written access/fee and permitted feed envelope. |
| Feed containment and dust management | Capture/retain fines and prevent cross-contamination; facility-approved controls | Unknown; must be specified by facility before selecting equipment. |
| Sieve set and sample containers | Reproducible size cuts and separated, labelled outputs | Apertures and cost depend on the protocol and available lab stock; no purchase yet. |
| Weighing and energy/speed instruments | Checked balance, energy meter and speed measurement if separator is tested | Access, resolution and calibration status unknown. |
| Assay and sample preparation | Ag plus relevant Si/Al/Cu/Pb composition in feed and products | Per-sample fee and method unknown; obtain quote before run count. |
| ECS/EDX or delamination access | Conditional comparator if target/feed warrants it | No verified Agastya equipment model, availability or price in project inventory. |
| Labor, transport, residual handling and upkeep | Supervision, sample chain, filters/cleaning/PPE, transport and waste | Unknown; include in actual cost per accepted kg. |

There is no honest total cost, cost-per-kg or payback figure yet. A component list is possible; a purchase list is premature. Populate the existing [equipment inventory](STAGE4_EQUIPMENT_INVENTORY_TEMPLATE.csv) and cost framework with dated local quotes once a facility is identified. Do not use literature throughput/energy or internet hobby-tool listings as Agastya estimates.

## Software and model decision

Build the material-lineage and assay/mass-balance workflow in EYE first: panel → Stage 3 stream → batch → aliquot → run → fraction → assay → receiver. The first analysis should be deterministic equations for mass closure, Ag inventory, grade, recovery, enrichment, energy and cost, with provenance and uncertainty. Keep the two physical targets and their outcomes distinct.

Do not train a process ML model yet: there is no Agastya Stage 4 dataset. After repeatable assay-backed trials, evaluate simple process-outcome models with whole panels/batches held out from training; consider a separate HSI material classifier only if calibrated spectra and physical labels become available. Neither model should replace elemental assay or facility safety controls.

## Final status for the Stage 4 research phase

### Settled by desk research

- The thesis's present ECS silver claim must be narrowed; conventional ECS is not a demonstrated method for silver extraction from Ag-printed silicon.
- Stage 3-to-Stage 4 feed mismatch is real in the project design: laminate is not EVA-free liberated metal feed.
- Direct comminution/classification is the best dry, mobile-aligned research hypothesis for a mixed Ag-bearing hand-off; its result on Agastya feed is unproven.
- Delamination is a separate target route; flotation is a separate wet silver-focused research benchmark; neither should be silently folded into the dry mobile baseline.
- EYE should prioritize lineage, assay provenance and mass-balance calculations; model training waits for real data.
- A September 2026 sonochemical paper supports treating fine-fraction metal concentration and Ag extraction as separate claims; its high-recovery Ag route is not a dry Stage 4 method.

### Requires physical or commercial information, not more desk literature

- Is any eligible Stage 3 c-Si feed available, in what state and quantity?
- Which supervised facility has suitable containment, separation equipment and trained oversight?
- Which assay can quantify Ag in representative feed/fractions, at what detection limit and fee?
- Will a named recycler/refiner accept the resulting stream, and under what conditions?
- What are actual local access, consumable, assay, transport and equipment costs?
- Does the proven process fit the mobile unit's footprint, power and handling envelope?

These are real-world verification gates. More literature cannot close them. Once they are answered, reopen Stage 4 work at protocol and cost finalization; until then the literature/design phase is complete and the project should stay at no-spend readiness review.

## Related Stage 4 records

- [Literature review](STAGE4_LITERATURE_REVIEW.md)
- [Feasibility review](STAGE4_FEASIBILITY_REVIEW.md)
- [Model critique and alternatives](STAGE4_MODEL_CRITIQUE_AND_ALTERNATIVES.md)
- [Feed-gap repair research](STAGE4_FEED_GAP_REPAIR_RESEARCH.md)
- [Method comparison and calculations](STAGE4_METHOD_COMPARISON_AND_CALCULATIONS.md)
- [Development roadmap](STAGE4_DEVELOPMENT_ROADMAP.md)
- [Readiness audit, 6 October](STAGE4_READINESS_AUDIT_2026-10-06.md)
- [Software and model research](STAGE4_SOFTWARE_AND_MODEL_RESEARCH.md)
