# Stage 4 Literature Review: Dry Separation of PV-Derived Material Fractions


> **Architecture correction (16 Oct 2026):** Current Stage 4 is silver removal/recovery. This file's size-classification, ECS, assay, or hand-off descriptions are prior route research, not the current stage definition. Treat size reduction/classification as possible feed preparation; assay and mass accounting validate the stage. See [Stage 4 architecture and route decision](STAGE4_ARCHITECTURE_AND_ROUTE_DECISION_2026-10-16.md).

**Review updated:** 8 October 2026  
**Thesis stage:** Legacy thesis Stage 4, described as an eddy-current separator with optional electrostatic polishing. This numbering differs from the current charter: its Stage 3 is the electrostatic candidate and Stage 4 is assay/accounting.  
**Evidence status:** desk review only. Agastya has not built or tested a Stage 4 separator.

> **Version/architecture note:** This review preserves the older thesis-stage numbering and its eddy-current concept. Do not use its stage numbers as the current AGASTYA architecture; see [Engineering overview](../../02_Engineering/ENGINEERING_OVERVIEW.md).

## Research question

Can a compact, dry Stage 4 produce an assay-verified Ag-bearing mixed fraction from the actual Stage 3 cell/EVA/backsheet laminate, and when (if ever) does separate liberation make a downstream separator worthwhile?

This review focuses on the thesis's eddy-current-separation claim. It does not assume that Stage 3's proposed heated roller works, that EVA-free cells are available, or that an eddy-current separator recovers silver or silicon at saleable purity.

**8 October 2026 consolidation:** a new [research completion brief](STAGE4_RESEARCH_COMPLETION_BRIEF_2026-10-08.md) incorporates the latest IEA PVPS 2026 commercial/pilot inventory summary and the July 2026 silver-specific flotation results, then records the final no-spend decision and the remaining field-verification gates.

## What the thesis currently proposes

The thesis routes EVA-stripped cell material containing silicon, printed silver/aluminium contacts and glass fragments over a rotating magnetic drum. It says conductive fragments, including silver-bearing silicon, are repelled into a separate trajectory. An electrostatic separator is described as optional polishing.

The first part of that concept is plausible only for feed that has been liberated into suitably sized, dry, mobile particles. The second claim is not supported by the sources reviewed: eddy-current separators are established for separating non-ferrous conductive metal particles from non-conductors, but the reviewed PV-specific sources do not demonstrate that an eddy-current drum separates printed silver from a silicon wafer or reliably ejects a composite silicon cell fragment as a silver concentrate. Silver is a thin printed contact attached to silicon, not a free metal particle.

## Findings from the literature

| Source | Method and reported result | What it means for Agastya | Evidence limit |
|---|---|---|---|
| Fiandra & Sannino, ENEA technical report (2023), [Analysis report on photovoltaic waste as source of valuable materials](https://hdl.handle.net/20.500.12079/66887) | Reviews PV waste processing routes and reports eddy-current and corona-electrostatic methods as options for aluminium/copper recovery from plastic particles. It cautions that eddy current is not efficient for separating different non-ferrous metals in PV waste and that metals attached to inert material need further crushing/liberation. | Treat ECS as a candidate coarse metal/non-metal pre-concentration step after suitable liberation. Do not claim a silver/silicon product or separation of Al from Cu without a separate test. | Review/technical report; describes limitations and prior work rather than validating Agastya's feed or geometry. |
| Smith et al. (2017), [Electrodynamic Eddy Current Separation of End-of-Life PV Materials](https://doi.org/10.1007/978-3-319-52192-3_37) | Reports a specialized fixed, high-frequency electrodynamic separator sorting 1–3 mm Si/Al and CdTe/Al surrogate particle mixtures with >85% grade and recovery, about 10 kg/h throughput and 68 kWh/short ton energy demand. The authors contrast it with traditional rotary ECS, which struggles economically below about 1 cm. | Confirms fine-particle PV-like separation is possible with a specialized EDX/EECS setup; it does not validate the thesis's conventional rotating drum. The study supports keeping separator architecture and particle size explicit in the design. | Research-scale result on prepared mixtures; not a processed complete module or Agastya trial. Energy and performance belong to that setup and boundary. |
| Nagel et al. (2020), [Electrodynamic Sorting of Industrial Scrap Metal](https://doi.org/10.14356/kona.2020015) | A fixed electromagnet under a conveyor sorted aluminium from industrial Zorba scrap; reports 97.6% Al grade, 93% recovery, about 250 kg/h practical rate, and roughly 7.2 kWh/t for its assembly. Smaller particles around 5 mm or less and thin shapes were harder to sort in that operating setup. | Shows a different EDX configuration can reach high throughput on industrial scrap, while confirming performance depends on size/shape/feed behavior. It is not PV feed evidence. | Industrial Zorba is not a PV-derived mixture; the machine and throughput cannot be assumed for Agastya. |
| Sim et al. (2022), [A facile crush-and-sieve treatment for recycling end-of-life photovoltaics](https://doi.org/10.1016/j.wasman.2022.11.023) | Reports >90% of polymer retained in larger fractions and >70% or >80% of total silver concentrated in the finest fraction for two studied waste categories, using crush-and-sieve without burning. | Size classification may be a more direct pre-concentration route for silver-bearing fines than the thesis's rotating ECS. It changes the Stage 4 feed and adds a controlled comminution step. | A silver-enriched fraction is not pure silver; study results depend on feed and crushing/sieving conditions. It does not validate an ECS. |
| Juyo Salazar et al. (2024), [Streamlined process with a sustainable approach for PV module recycling](https://doi.org/10.1016/j.susmat.2024.e01047) | A dismantle/comminute/sieve route reports 94.12% of Ag in the <0.25 mm fraction; 99.37% of Cu in the 0.5–2.00 mm fraction, which also contained substantial glass and polymer. | Supports testing multiple size fractions rather than assuming one separator output. This aligns with a dry solid hand-off, but the receiver still needs composition and contaminant assays. | Distribution/recovery into a size fraction is not its product grade or purity; result is feed- and process-specific. |
| Zhang et al. (2020), [Mathematical model and experimental investigation for eddy current separation of nonferrous metals](https://doi.org/10.1016/j.rinp.2020.103170) | Pilot ECS experiments separate copper and aluminium. The authors investigate particle size, conductivity-to-density ratio, magnetic induction and feed velocity; model and experimental results are compared. | ECS performance depends on particle and operating conditions. A drum cannot be specified from a diagram alone; measure feed size and set repeatable speed, belt/feed rate and magnetic-field conditions. | Tested Cu/Al solid-waste particles, not PV laminate, silver paste, cell fragments or an Agastya prototype. |
| Bin et al. (2022), [Effects of particle size on the separation efficiency in a rotary-drum eddy current separator](https://doi.org/10.1016/j.powtec.2022.117870) | Combines simulation and physical experiments; reports an optimal particle size for a given setup and interactions among size, material, rotational speed and magnetic-pole arrangement. | Particle-size classification should be a recorded feed-preparation variable, not an afterthought. Test defined size classes instead of feeding an uncontrolled mixture. | Results are setup-specific and do not define a universal PV particle-size window. |
| Li et al. (2023), [Recycling Si in waste crystalline silicon photovoltaic panels after mechanical crushing by electrostatic separation](https://doi.org/10.1016/j.jclepro.2023.137908) | Mechanically crushed PV material was classified and electrostatically separated. The study reports a 0.30–0.45 mm optimum size, 15 kV and 30 rpm for its tested apparatus, with 91.0% Si proportion but 48.9% Si recovery. | Electrostatic separation is a plausible later, instrumented comparison for fine liberated PV powders and may enrich a silicon-rich fraction. It is not evidence for an ECS step or for high recovery in Agastya. | Exact feed and separator conditions matter; the reported optimum must not be copied as an Agastya setting. High grade and recovery are different metrics. |
| de Souza & Veit (2023), [Study of electrostatic separation to concentrate silver, aluminum, and silicon from solar panel scraps](https://doi.org/10.1016/j.cec.2023.100027) | Crushed and size-classified c-Si PV scrap was tested in a roll-type electrostatic separator. Its abstract reports 38 kV and 75 rpm and qualitative co-concentration of Si, Ag and Al; a mass-weighted Ag balance is not available in the accessible abstract. | Electrostatic treatment can be considered after dry characterization and size classification. It produces concentration behaviour across a mixed fraction, not pure silver or cell-grade silicon. | Small-scale study; do not transfer its high-voltage settings into an unreviewed school build. Authors are de Souza and Veit, not Dias. |
| He et al. (2026), [Improving particle separation and recovery of valuable materials from end-of-life solar panels](https://doi.org/10.1016/j.resconrec.2025.108594) | Integrates upstream pyrolysis, a special sieving-aid method and later 4 M nitric-acid leaching. Reports >96.3 wt% separation of chip-like cell particles from debris and >98.9% silver recovery in the later leaching step. | High reported Ag recovery belongs to a multi-step route including chemical leaching; it is not an ECS-only or chemical-free result. The work underlines the need to state the actual process boundary for every recovery claim. | Different process architecture and feed; downstream acid leaching lies outside Agastya's on-site design boundary. |
| Zhang et al. (2026), [Near-complete Ag recovery via localized electrolyte-jet recycling](https://doi.org/10.1016/j.seppur.2025.136440) | Reports localized treatment at 5 V in circulating 12 wt% nitric acid: 90.2% surface-silver dissolution after 7 minutes and >95% separation after 30 minutes. | Reinforces the system boundary: dry pre-concentration can hand off a smaller characterized solid; silver extraction still belongs to a qualified external refiner under Agastya's current requirements. | A chemical/electrolyte process, not dry separation; it requires acid circulation and specialized equipment and does not validate Stage 4 hardware. |
| Zhao et al. (2020), [High-voltage pulse crushing](https://doi.org/10.1016/j.jclepro.2020.120442) | High-voltage pulse crushing of PV waste reported silver enrichment of 3.08× at 54.07% recovery under lower field/pulse conditions, and 1.67× at 89.41% recovery at stronger field/more pulses. The 0.5–4 mm glass fraction was reported above 98% purity. | A promising liberation and pre-concentration alternative, with a clear grade/recovery trade-off. It is not conventional ECS and does not produce pure silver. | Specialized high-voltage comminution; it requires engineered equipment and supervised testing, not a school-built device. |
| Saffarian, Galvin & Firouzi (2026), [PV silver recovery by froth flotation](https://doi.org/10.1016/j.mineng.2026.110189) | Lab-scale flotation of delaminated and ground PV cells used two reagents at 150 g/t. Rougher flotation in tap water reported 97.55% Ag recovery and a 32.2× upgrade; rougher-cleaner tests in ultrapure water reported about 47 wt% Ag at 86.5% recovery. | This is a new and strong silver-specific pre-concentration result. It is more directly aligned with silver than ECS and offers a possible university-lab collaboration route. | Requires liberated/ground cell feed, flotation cell, water and reagents, plus assay; not a dry or mobile no-chemistry Stage 4 method. Single recent study, not Agastya validation. |
| Mbam (2026), [Dry beneficiation thesis](https://doi.org/10.34901/mul.pub.2026.194) | MSc study combined rod-mill glass surface abrasion, hammer-mill size reduction and Hamos Corona drum electrostatic separation. For the 0.1–0.71 mm fraction, it reports >80% recovery across glass, silicon and metallic fractions with about 53% Si grade under one selected condition; the coarser size class needed separate optimization. | Useful recent evidence for staged comminution, size-class-specific separation and assay as a design pattern. It does not support a generic single-size/one-setting separator. | Master's thesis, not a peer-reviewed journal article; uses a specialized 30 kV separator and preparation train. Do not transfer settings to Agastya. |
| [Vibration separation of wafers and glass](https://doi.org/10.37190/ppmp/151679) (2022) | Reports an optimized coarse separation condition with silicon wafer product at 84.47% metal-Si grade and 83.73% recovery, alongside 98.95% glass recovery. | Could inform an upstream cell/glass split if Stage 3 eventually produces liberated coarse fragments. It does not recover silver from cell metallization. | Different target from Stage 4's metal separation; its vibration settings are apparatus-specific. |

## Synthesis and correction to the thesis design

1. **Eddy current separation sorts conductive particles by their electromagnetic response and trajectory.** It is not a general-purpose separator for every conductive-containing composite. A silicon cell fragment carrying a printed silver grid remains a silicon-rich composite; the literature reviewed does not show that ECS extracts its silver.
2. **The feed state is unresolved.** Stage 3's demonstrated literature baseline is hot-knife glass-to-laminate separation. It leaves an EVA/cell/backsheet laminate. The proposed roller's EVA stripping is still a hypothesis. Stage 4 therefore has no established, ready-to-feed stream in the present project.
3. **Size reduction and liberation are likely prerequisites for deeper fractionation.** The PV-specific ENEA review notes that non-ferrous conductors can remain attached to inert material. Shredding or crushing creates dust, sharp glass and potentially hazardous mixed fines; it is a separate controlled operation, not an implicit property of Stage 4.
4. **Conventional rotating ECS and fixed high-frequency EDX are different design choices.** A rotary drum is better matched to a coarser liberated non-ferrous fraction; PV-like 1–3 mm results were reported for a specialized fixed-frequency EDX system. The 2017 result does not validate the thesis's drum for fine cell material.
5. **ECS/EDX is a pre-concentration step, not silver extraction.** It may reduce metal in a residual stream or enrich conductive particles, but separation quality must be measured by mass balance and independent composition analysis.
6. **Electrostatic separation belongs later in the research plan.** PV studies show it can partition crushed and size-classified powders, but use high voltage and fine particles. It should be a separate supervised, guarded study after the feed and ECS baseline are characterized.

### Revised Stage 4 claim for the prototype

> Stage 4 will investigate whether a dry, size-classified, liberated c-Si PV-derived feed can be enriched into a coarse non-ferrous conductor fraction and a residual fraction using eddy-current separation. It will not claim recovery of pure silver, pure silicon, or panel-ready cells. Those require validated downstream separation and analytical evidence.

This correction keeps the thesis's core Stage 4 technology in the plan while narrowing the output claim to what the current literature supports.

For the system-level go/no-go judgment, conventional drum versus EDX comparison, and updated alternatives, see [Stage 4 feasibility review](STAGE4_FEASIBILITY_REVIEW.md).

For normalized mass/energy calculations and the updated comparison of crush-and-sieve, pulse crushing, ECS/EDX, electrostatic separation, flotation and vibration separation, see [Stage 4 method comparison and calculations](STAGE4_METHOD_COMPARISON_AND_CALCULATIONS.md).

**Development decision updated 6 October 2026:** controlled liberation and dry size classification is the primary Stage 4 candidate for producing a silver-bearing solid fraction for central refining. ECS is now conditional on a measured, liberated conductor feed and evidence that it adds value beyond the size split. No physical build or processing is authorized by this desk review. See [Stage 4 Development Roadmap](STAGE4_DEVELOPMENT_ROADMAP.md).

## Proposed research design

### Phase 4A — Define and characterize feed

- Start with a safe, known, non-PV reference mixture of dry aluminium/copper pieces and inert non-conductive material to validate the measurement procedure and separator trajectory.
- Only after equipment and supervision are in place, use a traceable PV-derived sample. Record its upstream Stage 3 event, construction/chemistry, source, mass, moisture, size distribution and visible laminate/polymer carryover.
- Do not feed intact modules, loose broken PV glass, unknown thin-film material, or uncharacterized dust to a prototype separator.
- Create sieve classes based on available calibrated sieves and the safe equipment; literature values are candidate ranges for study design, not preset settings.

### Phase 4B — Establish a baseline

- Record feed mass, particle-size class, material mix and initial photographs.
- Fix and record the separator geometry, rotor speed, belt/feed speed, feed rate, splitter position, magnetic configuration and number of passes.
- Collect every output stream separately; weigh each with an identified, checked scale and reconcile input/output mass.
- Repeat each condition on independent aliquots. Keep raw observations immutable.

### Phase 4C — Measure separation

Use measured, predeclared metrics:

- **Mass closure (%)** = 100 × (sum of output masses / input mass).
- **Target-metal recovery (%)** = 100 × (target metal mass in selected product / target metal mass in feed).
- **Product grade (%)** = 100 × (target metal mass in selected product / selected product mass).
- **Enrichment ratio** = product grade / feed grade.
- **Specific energy** = measured separator electricity (Wh or kWh) / feed mass (kg).

The target-metal mass and grade require a composition method such as XRF or a qualified laboratory assay. Weighing a stream alone is not chemical identification. Report uncertainty, sampling method and the analytical instrument; do not label visual inspection as purity.

### Phase 4D — Compare and decide

Compare ECS feed/product splits against the untreated feed and, only in a separate approved experiment, an electrostatic polishing route. Select settings by a stated trade-off between recovery and grade, not by the largest-looking product pile. Keep the downstream refinery hand-off as the destination for mixed silicon/silver-bearing concentrate until its receiving specification is known.

## Components and data needed for a real Stage 4 pilot

| Block | Required function | Minimum evidence/selection input |
|---|---|---|
| Feed preparation | Dry, screen and present a consistent, liberated feed | Feed chemistry, dust controls, accepted size range and mass per run |
| ECS test unit | Adjustable belt/feed, rotor speed and splitter; enclosed moving/magnetic parts | Rotor and belt speed range, magnetic-field configuration, feed capacity, particle-size envelope and guarding review |
| Collection | Separate, labelled and fully retained product/tail/middlings | Stream labels, sealed containers and no cross-contamination between runs |
| Metrology | Weigh feed/outputs and measure electric energy/speed | Scale capacity/resolution and check weights; power/energy meter range; tachometer or verified speed reading |
| Composition analysis | Identify and quantify Al, Cu, Si, Ag and relevant contaminants | Access to calibrated XRF or qualified lab assay; representative sampling plan |
| EYE record link | Tie feed and all products back to Stage 1–3 panel passport | Stable `panel_id`, Stage 3 completion event, Stage 4 event IDs, station/operator/instrument/calibration records |

No safe, priced ECS unit is specified yet. A separator must be selected or fabricated only after particle size, throughput and supervision are known; a small educational magnet/hand-built rotor is not evidence of an industrial ECS and should not be presented as one.

## Agastya-EYE hand-off

EYE already supports append-only `stage_4` events after a Stage 3 `process_completed` record. For each Stage 4 run, use a distinct `event_id` and include the measured masses, process settings and instrument provenance. Suggested measurement names include `feed_mass`, `conductive_product_mass`, `residual_mass`, `middlings_mass`, `rotor_speed`, `feed_rate`, `specific_energy`, `mass_closure`, `target_metal_recovery`, and `product_grade`. The EYE API now accepts `rpm` as a unit for measured rotor speed. **Do not relabel a unit to pass validation.** Composition percentages must include an assay instrument and sampling/calibration reference.

The event API is a traceability interface only. It does not control an ECS motor, validate guarding or prove chemical identity.

## References

- Fiandra, V. & Sannino, L. (2023). *Analysis report on photovoltaic waste as source of valuable materials: Overview on the current material recovery approaches*. ENEA RT-2023-05. [Repository record and report](https://hdl.handle.net/20.500.12079/66887).
- Smith, Y. (DOE EERE project document). *Comminution and Electrodynamic Eddy Current Separation Studies of End-of-Life Photovoltaic Materials*. [Project document](https://www.energy.gov/documents/61smithuutahpostdocawardpdf).
- Smith, Y.R., Nagel, J.R. & Rajamani, R.K. (2017). *Electrodynamic Eddy Current Separation of End-of-Life PV Materials*. [https://doi.org/10.1007/978-3-319-52192-3_37](https://doi.org/10.1007/978-3-319-52192-3_37).
- Nagel, J.R. et al. (2020). *Electrodynamic Sorting of Industrial Scrap Metal*. [https://doi.org/10.14356/kona.2020015](https://doi.org/10.14356/kona.2020015).
- Sim, Y. et al. (2023). *A facile crush-and-sieve treatment for recycling end-of-life photovoltaics*. [https://doi.org/10.1016/j.wasman.2022.11.023](https://doi.org/10.1016/j.wasman.2022.11.023).
- Juyo Salazar, R.B. et al. (2024). *Streamlined process with a sustainable approach for photovoltaic module recycling*. Sustainable Materials and Technologies, 41, e01047. [https://doi.org/10.1016/j.susmat.2024.e01047](https://doi.org/10.1016/j.susmat.2024.e01047).
- Zhang, S. et al. (2020). *Mathematical model and experimental investigation for eddy current separation of nonferrous metals*. Results in Physics, 17, 103170. [https://doi.org/10.1016/j.rinp.2020.103170](https://doi.org/10.1016/j.rinp.2020.103170).
- Bin, C. et al. (2022). *Effects of particle size on the separation efficiency in a rotary-drum eddy current separator*. Powder Technology, 410, 117870. [https://doi.org/10.1016/j.powtec.2022.117870](https://doi.org/10.1016/j.powtec.2022.117870).
- Li, J. et al. (2023). *Recycling Si in waste crystalline silicon photovoltaic panels after mechanical crushing by electrostatic separation*. Journal of Cleaner Production, 415, 137908. [https://doi.org/10.1016/j.jclepro.2023.137908](https://doi.org/10.1016/j.jclepro.2023.137908).
- Dias, P. et al. (2023). *Study of electrostatic separation to concentrate silver, aluminum, and silicon from solar panel scraps*. Circular Economy, 2(1), 100027. [https://doi.org/10.1016/j.cec.2023.100027](https://doi.org/10.1016/j.cec.2023.100027).
- He, Y. et al. (2026). *Improving particle separation and recovery of valuable materials from end-of-life solar panels*. Resources, Conservation and Recycling, 225, 108594. [https://doi.org/10.1016/j.resconrec.2025.108594](https://doi.org/10.1016/j.resconrec.2025.108594).
- Zhang, Y. et al. (2026). *Near-complete Ag recovery from silicon solar cells via localized electrolyte-jet recycling*. Separation and Purification Technology, 385, 136440. [https://doi.org/10.1016/j.seppur.2025.136440](https://doi.org/10.1016/j.seppur.2025.136440).


## Updated Stage 4 research question after 7 October 2026 feed-gap review

The lead question is no longer whether ECS can sort pre-liberated particles. It is whether contained comminution and multi-cut classification can make an accepted mixed Ag-bearing fraction directly from Stage 3 laminate. ECS is a conditional follow-on only if a suitable separate conductor stream is identified. This reframing is fully documented in [Stage 4 Feed-Gap Repair Research](STAGE4_FEED_GAP_REPAIR_RESEARCH.md).

## Update — 7 October 2026: literature on repairing the Stage 3-to-Stage 4 feed gap

The [Stage 4 Feed-Gap Repair Research](STAGE4_FEED_GAP_REPAIR_RESEARCH.md) compares direct laminate comminution/classification with partial delamination routes. The evidence changes the baseline question: if Agastya needs an assay-defined mixed Ag-bearing hand-off, is it better to classify controlled laminate fragments directly than to add an unvalidated EVA peel? Sim et al. (2022) support this as a research hypothesis: >90% of polymer remained in larger fractions, while up to 70%/80% of total Ag reported to the smallest fraction for their two studied waste categories. This is distribution to the size fraction, not its Ag grade.

For an intact-cell target, Wahman et al. (2024) demonstrate hot-knife backsheet recovery, while Wahman and Surowiak (2025 online / 2026 volume) report a heat-assisted mechanical back-EVA separation. These are promising partial-delamination references, but do not establish an onboard full-layer route; the latter study's summary includes a subsequent 400 °C step to recover clean glass/silicon. Li et al. (2022) provide a laboratory laser-assisted mechanical-peeling alternative after backsheet removal. IEA PVPS Task 12's 2025 report describes EVERPV pilot architectures that remove the backsheet and then mechanically separate cell+EVA fractions, making this a useful partner-processing lead rather than a copyable Agastya BOM.

The revised recommendation is to test, through a supervised facility, the actual Stage 3 laminate as the feed for controlled comminution and multi-cut classification first. Retain full delamination as an external partner route if the receiver or project target requires intact cells. Keep ECS out of the baseline unless the size/assay results reveal an eligible liberated coarse conductor stream.


### Counter-evidence: cell enrichment by mild crushing is not the same as Ag-fines recovery

Yan et al. (online 2025; December 2025 issue) study mild crushing to enrich silicon-cell fragments into a +1 mm size fraction. They report 25.36% mass yield and 50.32% cell recovery after 10 seconds; the later gravity step reports 14.39% product mass yield and 45.43% cell recovery, and clean cells require subsequent pyrolysis. This is evidence for a cell-bearing coarse stream and a different product objective, not an Ag recovery result or a complete dry mobile route. The comparison reinforces that Stage 4 must assay both silver and cell-bearing fractions and choose a target with the receiver. [Article](https://doi.org/10.1016/j.psep.2025.108091).
