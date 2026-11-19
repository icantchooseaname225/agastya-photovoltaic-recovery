# Stage 4 Feasibility Review


> **Architecture correction (16 Oct 2026):** Current Stage 4 is silver removal/recovery. This file's size-classification, ECS, assay, or hand-off descriptions are prior route research, not the current stage definition. Treat size reduction/classification as possible feed preparation; assay and mass accounting validate the stage. See [Stage 4 architecture and route decision](STAGE4_ARCHITECTURE_AND_ROUTE_DECISION_2026-10-16.md).

**Prepared:** 3 October 2026  
**Purpose:** assess whether the thesis's Stage 4 concept can work as described, what needs to change, and what a credible next study can demonstrate.  
**Evidence status:** published literature and design analysis only; Agastya has no Stage 4 machine, material trials, or measured results.

## Decision summary

**Stage 4 is the silver-removal/recovery step, but its route is not yet a complete process specification.** The thesis's eddy-current concept may move suitable liberated conductive particles away from non-conductors; that physical split does not automatically remove printed silver from silicon or polymer. Other reviewed silver-specific methods use prepared feed and specialist equipment. Select the Stage 4 route only after defining the actual Stage 3 feed and target product.

The project's critical gap is upstream: the current Stage 3 baseline produces glass plus a cell/EVA/backsheet laminate. It has not shown EVA-free cells or liberated metal pieces. A conventional rotary-drum ECS will not separate silver paste from a silicon cell fragment simply because the paste conducts. The proposed optional electrostatic step is not generic “polishing”; it is another distinct unit operation with its own fine feed requirements and high-voltage equipment.

**Recommended current correction:** define Stage 4 by its silver-removal function. Treat comminution, size classification and electrostatic sorting as possible feed-preparation or separation operations, and compare them with silver-specific flotation and extraction routes. No route is selected until feed condition, required product form, qualified facility, safety/waste controls, assay QA/QC and receiver requirements are specified. Do not claim purity or recovery before a measured silver balance.

## Feasibility by claim

| Thesis claim or project need | Verdict | Evidence-based reason |
|---|---|---|
| Eddy-current force can deflect non-ferrous conductive particles away from non-conductors | **Feasible in principle** | This is the established operating principle of ECS/EDX; separation depends on conductivity, particle mass/density, shape, size, field, speed and feed presentation. |
| A conventional rotating magnetic drum will sort fine cell material at sub-centimetre scale | **Poor fit** | PV-specific electrodynamic research reports that traditional rotating systems struggle to economically sort below about 1 cm. A rotary drum is more appropriate to a liberated, coarser non-ferrous fraction. |
| A specialized electrodynamic system can separate small PV-like Si/Al particles | **Demonstrated at research scale** | Smith et al. report >85% grade and recovery for 1–3 mm Si/Al and CdTe/Al particle mixtures at roughly 10 kg/h, using a fixed high-frequency electromagnet design. These are prepared mixtures and a specialized machine, not Agastya outputs. |
| Stage 4's ECS drum can extract printed silver from a silicon wafer or cell fragment | **Not supported** | The silver grid remains attached to the silicon cell unless upstream processing liberates it. The literature reviewed reports ECS sorting of material classes/particles, not silver removal from intact cell material. |
| ECS alone can generate the thesis's “silicon-and-silver-bearing concentrate” | **Not established** | No Agastya feed, grade/recovery assay, or receiver specification exists. ECS may make a metal/non-metal split; it does not make a silver product by itself. |
| Optional electrostatic separation can polish any ECS product | **Incomplete as described** | Published PV studies use crushed, size-classified fine fractions and dedicated high-voltage roll separators. Results are condition-specific, and a high-voltage, fine-powder stage adds guarding, dust and process controls. |
| The complete concept can be demonstrated with no purchases and the current kit | **No, as a functional Stage 4** | The thesis does not include an existing ECS or composition-assay instrument. A physical display/software demonstration is possible, but it cannot validate recovery. A real separator test requires borrowed/partner-lab equipment and assay access. |
| A Stage 4 station can fit the 20-foot mobile concept | **Physically plausible, commercially unproven** | A separator is a compact process block, but feed conditioning, dust containment, collection, safety systems, instrumentation and the Stage 3 interface all take space and cost. No Agastya layout, supplier quote, or integrated trial establishes the footprint or economics. |

## The two separator architectures must not be conflated

### Conventional rotary-drum ECS

A rotating permanent-magnet array induces currents in free conductive particles and throws them away from the belt trajectory. It is a reasonable downstream choice for **coarse liberated non-ferrous pieces** in a nonconductive stream, after upstream frame/J-box removal and size preparation. Fine printed contacts, thin flakes and metal still bonded to polymer or silicon are poor assumptions for a simple drum.

### Electrodynamic sorting (EDX/EECS)

The University of Utah work used a fixed electromagnet excited with alternating current instead of a mechanically rotating magnet array. Smith et al. report sorting 1–3 mm Si/Al and CdTe/Al particles at >85% grade and recovery, around 10 kg/h, and 68 kWh per short ton of sorted material. Converted, that energy is about **75 kWh per metric tonne** (0.075 kWh/kg) for the reported sorting operation only; it excludes Agastya's upstream delamination, comminution and any downstream refining. This is evidence that a specialized small-particle PV-like separation can work, not evidence that Agastya's drawn drum can.

A later industrial-scrap EDX prototype reported 97.6% aluminium grade and 93% recovery from a Zorba scrap mixture at about 250 kg/h and roughly 7.2 kWh/t for that assembly. The authors also report lower performance for particles around 5 mm or smaller in that setup and note that size, shape, collisions and feed presentation affect results. Zorba is not PV waste; this result demonstrates the possibility of EDX at higher throughput, not Agastya's PV performance.

## What the PV material studies show

### Crush-and-sieve can enrich fractions without a hot-knife EVA peel

Sim et al. (2022) demonstrated a crush-and-sieve route that retained over 90% of the polymer in larger fractions and concentrated more than 70% or 80% of the total silver (depending on the tested waste category) in its smallest fraction. This is a **silver-enriched mixed fines fraction**, not recovered pure silver; the paper discusses further treatment. It suggests that size classification may be a more direct pre-concentration step for a silver-bearing stream than a rotary ECS. It also requires comminution, produces fines, and changes Stage 3's process boundary.

### Electrostatic separation can enrich prepared fine silicon fractions, with a grade/recovery trade-off

Li et al. (2023) reported 91.0% silicon proportion and 48.9% silicon recovery for their 0.30–0.45 mm feed, 15 kV and 30 rpm roll-separator condition. The result shows that high grade does not mean high recovery, and that the material must first be mechanically crushed and size classified. These apparatus settings are not ready-made Agastya settings.

de Souza and Veit (2023) also tested electrostatic separation of crushed and size-classified c-Si panel scrap and reported elevated Si, Ag and Al fractions. This is evidence for concentration across a mixed feed, not pure silver or cell-grade silicon, and uses a distinct high-voltage separator.

### High-yield silver recovery uses additional operations

A 2026 study combined a special sieving-aid method with upstream pyrolysis and subsequent 4 M nitric-acid leaching. It reports >96.3 wt% separation of chip-like cell particles from debris under its optimized sieving conditions and >98.9% silver recovery in the later leaching step. This does not support an ECS-only claim; it shows that high silver recovery in the reported route came from a sequence of liberation, separation and chemical leaching. The chemistry remains outside Agastya's on-site, chemical-free design boundary.

## End-to-end material-path gap

| Current/claimed step | Output | Does it meet Stage 4's input need? |
|---|---|---|
| Stage 2 manual frame and junction-box removal | Frame, cables/J-box, laminated module | Provides accessible frame aluminium and cable copper as separate coarse items; those are already more directly recovered at Stage 2 than by routing them through Stage 4. |
| Stage 3 evidence-based hot-knife baseline | Front glass + cell/EVA/backsheet laminate | **No.** It is not EVA-free, not a dry liberated particulate mixture, and not an ECS-ready metal/non-metal feed. |
| Thesis's proposed heated roller | Claimed EVA-stripped cell sheet | **Not yet.** No result or source reviewed validates the claimed output or retained-heat benefit. |
| Additional material liberation and size classification | Sized PV-derived particles/fractions | Could create an ECS/EDX feed, but requires a separate, specified, guarded and measured operation that is absent from the current build plan. |
| ECS/EDX | Conductive-particle-rich and residual fractions | Could be a pre-concentration step, subject to the selected machine/feed size and measured assay. It does not establish pure Ag/Si products. |
| Central specialist refiner | Refined metals or downstream products | Consistent with Agastya's no-on-site-chemistry premise; the hand-off specification is still unknown. |

## Best route for Agastya

### Keep the mobile unit's claim modest

Agastya can remain a **chemical-free mobile pre-processing concept** if it sends physically concentrated but mixed solid fractions to a qualified central refiner. It cannot currently claim the system recovers silver onboard. The material passport can document source, process and mass flows, but cannot prove elemental grade without assay evidence.

### Split Stage 4 into a validated core and a research extension

1. **Core research question:** Can a selected guarded separator enrich a known liberated conductive fraction from a dry inert mixture with repeatable mass closure and assay-based grade/recovery?
2. **PV extension:** Does a characterized PV-derived feed prepared by a separately approved liberation/size-classification process show an enrichment benefit under the same separator conditions?
3. **Silver recovery:** Keep this downstream of Stage 4. If the goal shifts to silver pre-concentration, compare literature-supported crush-and-sieve or electrodynamic approaches; actual silver extraction remains the refiner's task unless the project boundary is deliberately expanded.

For a no-purchase school project, stop at a technical design, a non-working display or a borrowed-lab demonstration using known reference feed. Label it accurately. Do not use improvised high-voltage electrostatic equipment or build a high-current/high-frequency EDX drive as a school prototype.

## Update — 6 October 2026: route selection after expanded method comparison

The thesis's system constraint is retained: mobile, dry, mechanical/thermal pre-processing with a solid hand-off to a central refiner. However, the literature comparison changes the current Stage 4 development priority. PV-specific crush-and-sieve evidence directly supports concentration of silver-bearing material into a fine fraction, while the literature does not show that the thesis's drum extracts printed silver from cell fragments. Accordingly, controlled liberation followed by dry size classification is now the **primary candidate flowsheet for evaluation**; ECS remains a conditional secondary step for a characterized liberated conductor fraction if it adds assay-confirmed benefit.

This is not a validated design change or an instruction to build a crusher. No feeder, feed mass, particle-size distribution, safe facility access, separator specification, refiner acceptance criteria or capital quote has been established. The first implementation action is therefore to verify feed and partner-lab access. See the [Stage 4 Development Roadmap](STAGE4_DEVELOPMENT_ROADMAP.md) for the gates and cost framework.

## Stage 4 study design if lab access is found

### Gate 1 — Freeze the claim and feed

- Choose conventional rotary ECS only for a coarser free-metal fraction; choose EDX only if an existing supervised unit accepts the required size and feed type.
- Begin with known reference particles and inert media to rehearse mass tracking and trajectory measurement. This is a method control, not PV validation.
- For any later PV feed, identify c-Si provenance, Stage 3 event, dryness, size bins, degree of liberation and polymer/glass carryover.
- Do not feed intact modules, unknown thin-film panels, uncharacterized dust or loose glass into a research separator.

### Gate 2 — Characterize the machine and baseline

Record rotor or field configuration, rotor/frequency setting, belt and feed speed, feeder rate, separator gap/stand-off, splitter setting, particle size, mass, number of passes and energy. Use the installed unit's approved operating envelope; do not copy published voltages, frequencies or speeds as set-points.

### Gate 3 — Measure every fraction

Weigh feed, target product, residual, middlings and retained losses. Reconcile mass closure. Use calibrated XRF or a qualified assay with a representative sampling plan for composition. Report feed grade, product grade, recovery, enrichment and uncertainty separately. Repeat on independent aliquots.

### Gate 4 — Decide whether PV processing is worthwhile

Compare the incremental enrichment and specific energy against the untreated feed, sample preparation needs, downstream receiver's specification, and the added equipment/containment cost. If the receiver does not accept the product or the assay shows no useful enrichment, stop or revise the flow sheet rather than add an electrostatic polisher by default.

## Go/no-go assessment

- **Go** for continued literature/design work and a possible borrowed-equipment reference-mixture experiment.
- **Conditional go** for PV-derived feed only after Stage 3 output, liberation method, particle-size range, assay access and equipment review are established.
- **No-go for the thesis's present strong claim** that the rotating drum separates silver-bearing silicon fragments into a valuable concentrate or that an optional electrostatic unit automatically purifies it.
- **No-go for a purchased/build-it-yourself separator now:** there is no Agastya feed specification, verified hardware budget, or safe design, and the existing project has a no-spend constraint.

## Sources

- Smith, Y.R., Nagel, J.R. & Rajamani, R.K. (2017). *Electrodynamic Eddy Current Separation of End-of-Life PV Materials*. Energy Technology 2017, pp. 379–386. [Springer chapter](https://doi.org/10.1007/978-3-319-52192-3_37).
- Nagel, J.R., Cohrs, D., Salgado, J. & Rajamani, R.K. (2020). *Electrodynamic Sorting of Industrial Scrap Metal*. KONA Powder and Particle Journal, 37, 258–264. [Open full text](https://doi.org/10.14356/kona.2020015).
- Sim, Y., Tay, Y.B., Pham, H.K. & Mathews, N. (2023). *A facile crush-and-sieve treatment for recycling end-of-life photovoltaics*. Waste Management, 156, 97–106. [https://doi.org/10.1016/j.wasman.2022.11.023](https://doi.org/10.1016/j.wasman.2022.11.023).
- Fiandra, V. & Sannino, L. (2023). *Analysis report on photovoltaic waste as source of valuable materials*. ENEA RT-2023-05. [Repository record](https://hdl.handle.net/20.500.12079/66887).
- Li, J. et al. (2023). *Recycling Si in waste crystalline silicon photovoltaic panels after mechanical crushing by electrostatic separation*. Journal of Cleaner Production, 415, 137908. [https://doi.org/10.1016/j.jclepro.2023.137908](https://doi.org/10.1016/j.jclepro.2023.137908).
- Dias, P. et al. (2023). *Study of electrostatic separation to concentrate silver, aluminum, and silicon from solar panel scraps*. Circular Economy, 2(1), 100027. [https://doi.org/10.1016/j.cec.2023.100027](https://doi.org/10.1016/j.cec.2023.100027).
- He et al. (2026). *Improving particle separation and recovery of valuable materials from end-of-life solar panels*. Resources, Conservation and Recycling, 225, 108594. [https://doi.org/10.1016/j.resconrec.2025.108594](https://doi.org/10.1016/j.resconrec.2025.108594).

## Update — 7 October 2026: stress test of the thesis model and alternatives

A separate [Stage 4 Model Critique and Alternatives](STAGE4_MODEL_CRITIQUE_AND_ALTERNATIVES.md) records the full problem matrix, comparison and decision sequence. The central issue is a feed mismatch: the evidence-based Stage 3 output is a glass/cell/EVA/backsheet laminate, while an ECS requires a suitably liberated conductive-particle feed. A metal-bearing composite particle can respond as a whole; its trajectory does not establish silver separation. ECS should therefore be demoted to an optional coarse non-ferrous pre-sort, only if actual feed characterization and assays show a useful role.

The strongest current baseline research option is controlled liberation plus multi-cut dry size classification, with assay of every stream. Juyo Salazar et al.'s 2024 result that 94.12% of silver reported to a <0.25 mm fraction is a distribution/recovery statement, not a claim that the product fraction is 94.12 wt% silver. This route remains conditional on real feed, safe facility access, dust controls, assay and receiver requirements. If those gates cannot be met, the system-level alternative is a Stage 3 hand-off to a qualified recycler.

Other alternatives are screened in the new critique: gas-solid fluidized-bed separation after liberation (the cited study used pyrolysis), corona electrostatic separation (dry but high-voltage and feed-sensitive), fixed-frequency EDX (not interchangeable with rotary ECS), high-voltage pulse liberation and wet froth flotation (lab-only, outside the vehicle boundary). No method is selected for procurement. The current cost status remains unknown; do not describe a dry process as having no consumables, since dust filters, sample supplies, cleaning, PPE and maintenance are recurring costs.

## Update — 7 October 2026: define a feed-gap repair that matches the intended product

The new [Feed-Gap Repair Research](STAGE4_FEED_GAP_REPAIR_RESEARCH.md) separates two targets that had been blurred together: (1) a dry mixed Ag-bearing fraction for a central refiner, and (2) intact or EVA-free cells. For target 1, full EVA stripping is not a required first assumption. PV crush-and-sieve studies report substantial total Ag partitioning into fine fractions while retaining most polymer in coarse fractions, but this does not mean the fine fraction is high-grade Ag. The revised baseline hypothesis is therefore contained comminution and multi-cut size classification of the actual Stage 3 laminate, followed by assay of every fraction. This is a research hypothesis, not demonstrated Agastya performance.

If intact cells are the goal, investigate mechanical backsheet removal and heat-assisted or laser debonding only through a qualified partner. The reported heat-assisted back-EVA study is promising, but does not establish a simple complete mobile delamination route; its described process also uses a 400 °C treatment for clean glass/silicon recovery. The old ECS model remains conditional and is excluded from the new baseline. No purchase, operation, cost total or throughput claim is supported before feed, supervised lab access, dust controls, assay and receiver acceptance are confirmed.
