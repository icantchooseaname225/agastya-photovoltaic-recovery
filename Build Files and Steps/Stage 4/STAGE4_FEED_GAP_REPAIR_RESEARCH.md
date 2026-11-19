# Stage 4 Feed-Gap Repair Research


> **Architecture correction (16 Oct 2026):** Current Stage 4 is silver removal/recovery. This file's size-classification, ECS, assay, or hand-off descriptions are prior route research, not the current stage definition. Treat size reduction/classification as possible feed preparation; assay and mass accounting validate the stage. See [Stage 4 architecture and route decision](STAGE4_ARCHITECTURE_AND_ROUTE_DECISION_2026-10-16.md).

**Review date:** 7 October 2026  
**Question:** How can Agastya bridge the gap between Stage 3's cell/EVA/backsheet laminate and the feed required for Stage 4 silver removal/recovery?  
**Evidence status:** Literature and project-record review only. No sample, equipment access, assay partner, receiver specification or quote has been confirmed.

## Decision in one paragraph

The project owner defines Stage 4 as silver removal/recovery. The literature's contained comminution and multi-cut sieving route remains a **possible feed-preparation or pre-concentration step**, not the silver-removal operation. Sim et al. show that study-specific feeds can direct a majority of total Ag into a fine fraction without first burning away encapsulant, but this is not an Agastya result and the fines are not pure silver. The route question is now: what additional preparation, if any, makes the actual Stage 3 output acceptable to a qualified silver-removal process? Compare physical preparation, flotation and chemical/electrochemical removal against the intended product, facility safety and waste requirements.

If the project requirement is instead an intact-cell or EVA-free output, add a separate delamination route and treat it as a partner-lab research workstream. Published backsheet hot-knife and heat-assisted back-EVA approaches are promising partial steps, but the evidence does not yet establish a compact, onboard, full-layer process that turns Agastya's current laminate directly into ECS-ready Ag particles. The best system-level fallback remains a qualified recycler hand-off.

## Define the product before trying to “fix” the feed

These are different targets and require different process boundaries:

| Target | Minimum useful Stage 4 output | Does it require EVA-free cells first? | Direction |
|---|---|---:|---|
| Silver-bearing fraction for central refining | Dry, traceable, size-classified mixed concentrate with measured Ag grade/recovery and receiver acceptance | **Not necessarily.** A crush-and-sieve route can use polymer retention in coarse fractions and Ag distribution to fines. | First Agastya research hypothesis |
| Intact solar-cell fragments for later high-value recovery | Liberated cell pieces with measured EVA/backsheet carryover and cell damage | Usually requires delamination or a partner route | Separate partner-lab route |
| Free Ag particles / elemental silver | Purified metal meeting refiner/product specification | Yes, plus metal liberation and downstream refining | Outside Agastya's current Stage 4 claim |

The key unresolved issue is the mismatch between the **Stage 3 laminate output** and the feed required for the selected Stage 4 silver-removal route. Specify the desired silver-bearing output first, then determine whether EVA/backsheet removal, cell liberation, size reduction or another preparation step is required.

## What the literature supports

### Route A — process the laminate directly: controlled comminution + multi-cut sieving

Sim et al. (2022) deliberately avoided thermal treatment to free the encapsulation polymer. Their crush-and-sieve work produced size fractions with different compositions; more than 90% of polymer remained in the larger fractions, while the smallest fraction contained up to 70% and 80% of total Ag in the two studied waste categories. This means **Ag partition to a fine fraction**, not 70–80 wt% Ag grade. It supports a mixed-fraction hand-off concept, not silver purification. [Article](https://doi.org/10.1016/j.wasman.2022.11.023)

The reported size cuts were F1 >5 mm, F2 1–5 mm, F3 0.25–1 mm and F4 <0.25 mm. The larger fractions retained most polymer; the finest contained less polymer but was not pure metal. This gives Agastya a literature starting point for a comparison, not a screen specification: the Stage 3 hot-knife laminate and any candidate comminution device can shift the size distribution and composition.

Juyo Salazar et al. (2024) likewise report Ag concentrated in the <0.25 mm cut and multiple material distributions across size cuts. Their 94.12% value is an Ag fraction-distribution result; the coarser material contains substantial glass and polymer. Again, size classification is pre-concentration, not a finished silver product. [Article](https://doi.org/10.1016/j.susmat.2024.e01047)

Their process reduced dismantled module material to <6.35 mm before classification. The reported 0.5–2.0 mm stream was 76.85% glass and contained 64.04% polymer despite reporting 99.37% of the Cu; the <0.25 mm stream carried the reported 94.12% Ag distribution and also contained crystalline silicon. This is a direct warning that high metal partition to one size cut can still leave a mixed, polymer-contaminated product.

**Why it fits:** it can accept encapsulated PV-derived material; avoids adding an unvalidated EVA-peeling roller; keeps Stage 4 dry; supports a relatively simple product definition (assayed size fractions); and gives the central refiner the concentrated solid it can further process.

**What remains unproven:** the exact feed in those studies versus Agastya's hot-knife laminate; transfer of fraction cut points to the actual panel; Ag grade, not just Ag distribution; fines loss and mass closure; throughput, power, wear, dust capture and cleaning; receiver acceptance; and whether the process is compact enough for the vehicle.

**Agastya implication:** research a closed, guarded, staged size-reduction and sieving concept on paper and seek a supervised partner-lab trial. Do not choose a crusher or buy screens until the sample, dust controls and assay plan are established. Use literature size cuts only as candidate bins, not final dimensions.

**Important counter-evidence / target distinction:** Yan et al. (online 2025; December 2025 issue) studied mild crushing to enrich *Si-cell-bearing* particles, rather than Ag into fines. Their +1 mm candidate stream had 25.36% mass yield and 50.32% cell recovery after 10 seconds; a later gravity step reported 14.39% product mass yield and 45.43% cell recovery. The route then used pyrolysis for clean cells. This suggests low-intensity breakage can make a cell-rich stream, but also shows that size-selective concentration may lose roughly half the cells and does not, by itself, solve the polymer problem. It is a useful comparator if the target changes to cell recovery, not evidence that Agastya's dry stream will meet a refiner's specification. [Article](https://doi.org/10.1016/j.psep.2025.108091)

### Route B — partial layer delamination: mechanically remove backsheet / back EVA

Wahman et al. (2024) report a hot-knife method to separate and recover the backsheet from c-Si modules without breaking cell integrity. The work's target is backsheet removal, not freeing silver from silicon or removing every EVA interface. [Article record](https://doi.org/10.1016/j.solmat.2024.113067)

Wahman and Surowiak (online 2025; journal volume 2026) report a heat-assisted mechanical process for recovering back EVA. Their best reported laboratory condition was 200 °C, a 10 cm heating distance and 9–12 V pull-off, yielding 99.97% EVA purity in under one minute. That is **purity of the recovered EVA**, not module-wide EVA recovery. The sequence first removes the backsheet with a hot knife, removes back EVA, later separates the remaining front glass/EVA/cell structure, and uses a 400 °C treatment to release clean glass/silicon. The headline back-EVA result is promising, but it does not prove Agastya can fully remove both EVA interfaces in a compact mobile station. [University record](https://badap.agh.edu.pl/publikacja/162053) [DOI](https://doi.org/10.1016/j.solmat.2025.113924)

**Why it is relevant:** a backsheet peel could create a better-defined core feed, while back-EVA removal may make cells easier to handle downstream.

**Why it is not the baseline:** it adds a separate heated blade/peeling operation, handling of a fragile sheet and a remaining question about front-side EVA. The 400 °C cleanup step is beyond the current onboard boundary and would require a separate emissions and safety assessment. The recovered object is not automatically a liberated conductive granule for ECS.

**Agastya implication:** keep this as a partner-lab comparator if intact cells or polymer recovery becomes a stated target. First obtain the full methods and clarify which interfaces are removed, energy, heat source, emissions/ventilation, feed condition, yield, damage and whether the 400 °C step is required for the claimed output.

### Route C — laser-assisted back-EVA debonding and mechanical peeling

Li et al. (2022) report a 1064 nm pulsed-fiber-laser treatment that weakens the back-EVA/cell interface after the frame, junction box and backsheet are removed, allowing the EVA to be peeled from the cell without damage under the study conditions. This is a single-interface cell-preserving method, not an onboard silver liberation step. [Article](https://doi.org/10.1016/j.wasman.2021.11.024)

**Fit:** chemical-free laboratory alternative that targets a specific interface.

**Limitations:** laser capital/control and engineered laser-safety enclosure; requires previous frame/junction-box and backsheet removal; single-interface result does not establish a full-layer solution; does not itself liberate printed Ag from silicon. Treat as external-lab research, not a low-cost vehicle component.

### Route D — mechanical/thermal or optical delamination at a specialist partner

The IEA PVPS 2025 status report describes the EVERPV project comparing mechanical, optical/thermal, and mechanical/thermal delamination, with pilot lines in France and Italy. Its France route is described as mechanically removing the backsheet, then mechanically removing cells+EVA and processing those powders to recover EVA, Ag and silicon. These are project/pilot descriptions and targets, not a ready-to-copy Agastya design or a demonstrated local service offer. They show that “backsheet off, then cells+EVA mechanically separated” is a credible specialist process architecture. [IEA PVPS Task 12 report, project summary and process description](https://iea-pvps.org/wp-content/uploads/2025/07/IEA-PVPS-T12-31-2025-REPORT-Status-Module-Recycling.pdf)

**Agastya implication:** this is a strong partner-sourcing lead. Ask a recycler, university or project contact whether a c-Si cell/EVA laminate can be processed and returned as assayed fractions. It may solve the interface without placing the full delamination plant on the mobile unit.

### Routes to keep off the onboard baseline

- **Pyrolysis / high-temperature EVA removal:** can improve liberation, but polymer decomposition, off-gas management and fluorinated backsheet risk conflict with the current simple mobile boundary. A study by Feng et al. used 500 °C for 30 minutes for liberation; do not translate that into a Stage 4 build setting. [Feng et al.](https://doi.org/10.1016/j.solmat.2023.112553)
- **Solvents / swelling / acid:** potentially effective in research, but process chemicals, solvent recovery, wastewater and EHS controls violate the current no-process-chemicals premise.
- **Water-jet delamination:** useful specialist option for layer-by-layer recovery, but it is a wet process with high-pressure equipment and wastewater; do not insert it into Agastya's dry mobile route without changing the project boundary.
- **ECS on the intact laminate:** reject as the baseline. A laminate or composite particle moving in a field does not establish Ag separation.

## Recommended Agastya architecture

```text
Stage 2: identified, de-framed c-Si module
  -> Stage 3: hot knife separates front glass
  -> Stage 3 output: cell/EVA/backsheet laminate (actual, documented feed)
  -> Stage 4 baseline hypothesis: enclosed controlled size reduction
  -> dry multi-cut classification; retain all size fractions and residues
  -> assay representative feed + all products; mass closure
  -> defined mixed Ag-bearing fraction handed to named central refiner

Optional external partner route, only if intact-cell/high-integrity materials are needed:
  Stage 3 laminate -> mechanical backsheet peel / heat-assisted or laser debond comparator
  -> characterize what interfaces remain -> partner processing and assay
```

For the first route, redefine the old “controlled liberation” wording as **controlled comminution and size classification of the laminate**. Do not imply that it strips EVA or makes free metal particles. The primary output is a characterized mixed concentrate. Keep the EYE passport/batch-manifest plan so each panel's mass and derived fractions stay traceable.

## Bench-study comparison and pass criteria

If a supervised facility later confirms eligible feed, compare the following on equivalent aliquots; these are study arms to discuss with the facility, not instructions to operate equipment:

| Study arm | Question | Required result |
|---|---|---|
| A. Untreated Stage 3 laminate characterization | What material and Ag inventory enter Stage 4? | Feed mass, size/condition, polymer/glass description, assay, representative sampling and uncertainty |
| B. Size classification baseline | Does a size split alone move enough Ag into a smaller hand-off stream? | Mass of every cut, Ag grade/recovery per cut, enrichment, closure, energy/time, fines retained |
| C. Controlled comminution + same cuts | Does size reduction improve Ag distribution/receiver value versus B, and what does it do to cell-rich fractions? | Same metrics, with wear/dust/cleanup residue included in the boundary; report Ag and Si-cell distribution independently |
| D. Optional partner delamination + classification | Does a peeled/partly delaminated feed outperform B/C enough to justify another operation? | Which interfaces removed; intactness; output contamination; cost/time/energy; Ag metrics; receiver acceptance |
| E. Optional ECS on an eligible stream | Does ECS add measurable benefit to the best size-class route? | Machine feed envelope met; assay-confirmed grade/recovery improvement over the same feed without ECS |

**Pass the Stage 4 concept** only if a repeatable route produces an accepted output, closes mass within a predeclared measurement tolerance, demonstrates assay-based improvement over the untreated feed, and has a plausible facility/vehicle envelope. Set numerical tolerances with the supervisor and receiver before trials; the current record does not justify inventing them.

**Stop or redesign** if the feed is not traceable, the receiver will not accept the fraction, assay/sampling is unavailable, dust containment cannot be verified, or added delamination/ECS does not improve the output enough to justify its burden.

## Feasibility and cost findings

There is no defensible price or mobile throughput estimate yet. Cost should be requested separately for: enclosed comminution and dust extraction; multi-cut sieve stack and cleaning; sample containers/labels; scales and power metering; per-sample assay; maintenance and filters; partner delamination or toll processing; transport; residual waste; and operator/supervisor time. Compare the added cost of a delamination route against its assay-confirmed increase in receiver value, not against a theoretical pure-silver price.

The current research supports the **technical hypothesis** that size-selective concentration can work without EVA stripping. It does not establish the **operational feasibility** of doing it in Agastya's vehicle. Until the equipment footprint, dust strategy, actual feed, receiver terms and assay access are known, the partner hand-off path is the lower-risk architecture.

## Next research and project actions

1. Freeze the intended Stage 4 output as either (a) mixed Ag-bearing concentrate or (b) intact/partly delaminated cells; do not mix these targets in a single machine claim.
2. For target (a), ask a supervised lab/recycler about controlled comminution, screening, dust containment and assay of a traceable Stage 3 laminate sample. Request a quote and whether their equipment accepts a cell/EVA/backsheet laminate.
3. For target (b), ask a partner whether it has mechanical backsheet removal, back-EVA peeling, laser or equivalent equipment; request the exact remaining layers and measured outputs. The EVERPV architecture is a lead for partner questions, not a supplier quote.
4. Get a named receiver's specification and analytical method before choosing size cuts or calling any fraction “concentrate.”
5. Only after partner access is verified, write a bench protocol and data sheet with mass closure, assay, energy, cost and stop criteria. No Stage 4 machine purchase is justified before these items are known.

## References

- Sim, Y. et al. (2023). “A facile crush-and-sieve treatment for recycling end-of-life photovoltaics.” *Waste Management*, 156, 97–106. [https://doi.org/10.1016/j.wasman.2022.11.023](https://doi.org/10.1016/j.wasman.2022.11.023)
- Yan, G. et al. (online 2025; December 2025 issue). “An effective process for Si-cells enrichment of end-of-life photovoltaic panels based on mild crushing.” *Process Safety and Environmental Protection*, 204, 108091. [https://doi.org/10.1016/j.psep.2025.108091](https://doi.org/10.1016/j.psep.2025.108091)
- Juyo Salazar, R.B. et al. (2024). “Streamlined process with a sustainable approach for photovoltaic module recycling.” *Sustainable Materials and Technologies*, 41, e01047. [https://doi.org/10.1016/j.susmat.2024.e01047](https://doi.org/10.1016/j.susmat.2024.e01047)
- Wahman, M. et al. (2024). “PV back sheet recovery from c-Si modules using hot knife technique.” *Solar Energy Materials and Solar Cells*, 276, 113067. [https://doi.org/10.1016/j.solmat.2024.113067](https://doi.org/10.1016/j.solmat.2024.113067)
- Wahman, M. & Surowiak, A. (online 2025; 2026 volume). “A heat-assisted mechanical method for back EVA recovery from end of life c-Si modules.” *Solar Energy Materials and Solar Cells*, 294, 113924. [https://doi.org/10.1016/j.solmat.2025.113924](https://doi.org/10.1016/j.solmat.2025.113924)
- Li, X. et al. (2022). “Back EVA recycling from c-Si photovoltaic module without damaging solar cell via laser irradiation followed by mechanical peeling.” *Waste Management*, 137, 312–318. [https://doi.org/10.1016/j.wasman.2021.11.024](https://doi.org/10.1016/j.wasman.2021.11.024)
- IEA PVPS Task 12 (2025). *Status of PV Module Recycling in IEA PVPS Task 12 Countries*, EVERPV project summary and pilot process descriptions. [Report PDF](https://iea-pvps.org/wp-content/uploads/2025/07/IEA-PVPS-T12-31-2025-REPORT-Status-Module-Recycling.pdf)
- Wu, Z. et al. (2023). “A novel method for layer separation in waste crystalline silicon PV modules via combined low-temperature and thermal treatment.” *Waste Management*, 172, 299–307. [https://doi.org/10.1016/j.wasman.2023.10.036](https://doi.org/10.1016/j.wasman.2023.10.036)
- Feng, Y. et al. (2023). “A promising method for the liberation and separation of solar cells from damaged crystalline silicon photovoltaic modules.” *Solar Energy Materials and Solar Cells*, 262, 112553. [https://doi.org/10.1016/j.solmat.2023.112553](https://doi.org/10.1016/j.solmat.2023.112553)
