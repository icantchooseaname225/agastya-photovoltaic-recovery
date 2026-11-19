# AGASTYA froth-flotation reagent feasibility report

**Prepared:** 19 November 2026. **Status:** desk research only; no AGASTYA reagent, slurry or physical test.

## Finding

Flotation is a Stage 4 candidate because a 2026 peer-reviewed study treated delaminated, ground end-of-life c-Si cells and reported Ag concentration in bench tests. It does not establish performance on whole-module material, AGASTYA's Stage 3 outlet or an Indian commercial circuit.

A critical reagent-role discrepancy remains. The PV study labels AEROPHINE 3418A the collector and AEROFLOAT 242 the frother. Syensqo currently markets **both** as collectors/promoters; its AEROFLOAT 242 page calls it a selective galena collector. Resolve with the authors and supplier before circuit design, sample request or pricing. This report excludes an indexed paper dated January 2027 because it is after the report cutoff.

No traceable India unit price, stock, MOQ or delivery time was verified for either reagent. A manufacturer quotation route exists, but Asia-Pacific availability is not proof of India stock or price. Cost remains parameterized.

## 1. PV evidence and transfer limits

Saffarian, Galvin and Firouzi (2026) used end-of-life solar-cell material supplied after delamination. The study reports crushed-cell feed with d100 about 2 mm, wet-ground to P80 about 103 µm, then tested in 0.5 L and 1 L mechanical cells.

Reported results:
- 0.5 L: 95.3 ± 2% Ag recovery; 17.9 ± 0.3 upgrade.
- 1 L: 91.31 ± 0.61% recovery; 33.8 ± 3.5 upgrade.
- tap-water rougher: 97.55 ± 0.03% recovery; 32.2 ± 2.3 upgrade.
- reported optimum: 150 g/t dry feed for tested setup; confirm whether per reagent or combined.
- roughly three minutes to approach the study rougher recovery plateau.
- rougher-cleaner result: 46.7 ± 1.5 wt% Ag at 86.5 ± 2.8% recovery under study conditions.

Calculated mass pulls from recovery/upgrade are 5.32% for the 0.5 L test, 2.70% for the 1 L test, and 3.03% for the tap-water rougher. They describe those study feeds and are not AGASTYA projections. Do not calculate cleaner mass yield without matching feed grade/definitions.

The feed was already delaminated and milled; this says nothing about foam-roller output, glass/EVA/backsheet contamination, copper ribbon/solder, dust or coarse feed. The tap-water comparison is not repeated process-water reuse. A silver-bearing froth is not purified silver.

## 2. Candidate reagent systems

| Candidate | Evidence / fit | AGASTYA assessment |
|---|---|---|
| AEROPHINE 3418A | Direct use as collector in the 2026 PV study, with surface-chemistry evidence. Manufacturer describes a sulphide/precious-metal ore collector. | Best-supported PV collector candidate for study-like prepared feed, not proven on AGASTYA feed. Obtain current SDS, active content, compatibility and India quote. |
| AEROFLOAT 242 | PV paper calls it a frother; manufacturer calls it a proprietary selective collector, especially for galena where silver is present. | Critical role conflict; hold until authors/supplier clarify intended function and dose basis. |
| MIBC | Common mineral-processing frother; not the frother identified in the retrieved 2026 batch PV study. | Comparator only; no PV-specific dose/performance transfer. |
| Xanthates/dithiophosphates | Common in sulphide ore circuits. Retrieved PV paper does not demonstrate these as replacements for native Ag metallization attached to silicon. | Research comparators, not selected. |
| Alcohol/glycol frothers | Manufacturer lists dedicated frother products separately from collectors. | Consider only after roles are verified and matched-feed tests planned. |

Syensqo's AEROPHINE FAQ gives 0–35 °C storage guidance in a closed container away from heat/acids, lists compatible vessel materials/exclusions, and instructs users to read the current SDS. This is supplier guidance, not process design or safety approval.

## 3. Dose, cost and sensitivity

The paper reports 150 g/t dry feed at optimum with two reagent streams and a 75–600 g/t test range. Confirm whether 150 g/t is per product or combined.

For T tonnes dry feed:
- If 150 g/t is **per reagent**, each demand is 0.15T kg; cost is 0.15T × (Pcollector + Psecond), where prices are delivered INR/kg.
- If 150 g/t is **combined**, cost depends on reagent split and blend/product prices.
- No delivered India price was verified.

Arithmetic stress test only: 150 g/t each gives 0.30 kg/t total. Each ₹1,000/kg combined weighted-average price adds ₹300/t feed. A ₹500/t reagent allowance implies a maximum weighted average ₹1,667/kg at that dose; ₹1,000/t implies ₹3,333/kg. These are thresholds, not market prices or AGASTYA OPEX. They exclude water, energy, labor, equipment, maintenance, tax, assay and waste.

A generic SDS catalog price is not a proxy for the proprietary candidates and is not a supported substitute; excluded.

## 4. Reuse and recycling

The retrieved study includes a tap-water comparison, not repeated use of recovered process water. No reuse cycles, residual reagent activity, contaminant buildup, regeneration or long-term performance were established for this PV feed. Do not claim indefinite reuse.

A qualified host should define water-quality cases and compare fresh/tap/recycled water on matched feed, with full water/solids accounting. The host decides containment and disposal.

## 5. Equipment and maintainability

Flotation adds a stirred cell, controlled air supply, reagent dosing, froth/tailings collection, dewatering/drying, cleaning, water management and QA/QC. A 0.5–1 L cell does not size a pilot.

Host design review should address vessel/seal/hose compatibility with the current SDS, buildup from fines/EVA/foam debris, air/agitation/pulp/pH/froth monitoring, calibration, cleaning/carryover, operator training, and collection of unused reagent, tailings, wash water and cleaning residue.

AEROFLOAT 242 current storage/compatibility/hazard details need product-specific SDS confirmation. Do not assume AEROPHINE guidance applies.

## 6. Environmental and safety

- Require facility chemical review and current SDS for each product.
- Do not infer low risk from mineral-processing precedent or a vendor comparison.
- Characterize actual PV feed and residues; fine Ag-bearing particles, polymers, glass and possible solder metals are feed-specific.
- Contain solids and liquids; no discharge to drain/general waste based on this desk report.
- Ask the host to determine waste category, storage, transport and authorized disposal route.
- Resolve AEROFLOAT's disputed role, identity, active content and SDS before procurement.

## 7. Indian procurement and regulatory context

No India-local stock, delivered price, MOQ or lead time was verified for either reagent. Syensqo pages offer quotation/inquiry and show Asia-Pacific availability; this does not prove domestic stock. Obtain delivered quote, grade, pack size, lead time and current SDS.

India's E-Waste Rules, 2022 include a PV module chapter. The primary text covers producer/manufacturer registration, storage through 2034–2035 and annual returns; the schedule says standard recycling targets do not apply to PV waste. This is not a blanket exemption for other constituents/residues. Verify current consolidated rules and facility compliance.

## 8. Route comparison and viability

| Route | Evidence level | Complexity/cost implications | Decision |
|---|---|---|---|
| Mechanical liberation + dry size classification | Low-complexity baseline; literature on other module feeds does not prove AGASTYA grade/recovery. | Classification, dust capture, all-fraction assay. | Keep baseline after characterization. |
| Mechanical liberation + ECS + flotation | No retrieved proof ECS retains Ag-bearing silicon fragments in the actual feed. | Adds equipment/energy/handling; benefit requires paired Ag retention and downstream improvement. | Keep ECS in comparison, conditional on mechanism and balance. |
| Prepared-feed flotation | Direct bench PV-cell study. | Reagents, water, agitation/air, cleaning, dewatering, QA/QC, residues. | Leading silver-specific candidate at a qualified host, not a selection. |
| Hydrometallurgy after concentration | Separate literature exists; brings chemical and waste requirements. | Requires qualified assay, refining and waste plan. | Host-led research only; no recipe here. |

The 1 L paper mass-pull calculation (~2.70% of its prepared feed) illustrates why a small concentrate may be useful. It does not prove saleability, profitability or purified silver.

## 9. Economic boundary

Gross Ag value = measured Ag kg/t × measured end-to-end recovery × buyer price for the actual product. A 999 silver benchmark is not a mixed-concentrate price.

AGASTYA lacks feed assay, Stage 2/3 mass retention, Stage 4 recovery, buyer, delivered reagent quote, water/energy/labor costs and equipment quotes. No net margin is defensible. CEEW's India-scale whole-module model reports losses in its reference routes; that cautions against equating high Ag recovery with commercial feasibility.

## 10. Future supervised data requirements

Before a qualified host runs any test, specify sample provenance, representative assay, size/liberation, verified reagent identities/roles/dose basis, SDS, water source, matched controls/replicates, all concentrate/tailings mass and Ag assay, mass/Ag closure, energy/time/labor/cleanup, reuse cycles actually tested, uncertainty, receiver specification and residue route. The host selects all conditions and safeguards.

## 11. Recommended actions

1. Ask authors to clarify 150 g/t basis and AEROFLOAT 242's role.
2. Ask Syensqo for role, composition, current India SDS, delivered quote, pack/MOQ/stock/lead time and a separate frother recommendation.
3. Do not procure before host acceptance, safety review and waste plan.
4. Characterize actual Stage 3 feed before choosing ECS, flotation or size target.
5. Replace symbolic costs only with verified quotes and measured data.

## Sources

- Saffarian et al. (2026), *Minerals Engineering* 242, 110189. [DOI](https://doi.org/10.1016/j.mineng.2026.110189). Peer-reviewed PV feed experiment; narrow prepared-feed scope.
- [Syensqo AEROPHINE FAQ](https://www.syensqo.com/en/brands/aerophine/faqs), [AEROFLOAT 242 product page](https://www.syensqo.com/en/product/aerofloat-242-promoter), [AEROPHINE applications](https://www.syensqo.com/en/brands/aerophine/applications). Manufacturer product-role/storage sources.
- [CEEW India recycling financial analysis](https://www.ceew.in/publications/is-solar-module-recycling-in-india-financially-feasible)
- [MoEFCC rules index](https://moef.gov.in/rules-regulations-3); [CPCB-hosted rules](https://cpcb.nic.in/uploads/Projects/E-Waste/e-waste_rules_2022.pdf)
- [IBJA 19 Nov 2026 market report](https://www.ibja.co/Upload/IBJA_Bullion%20Daily%20Report%20-%2019-11-2026.pdf), market reference, not concentrate offer.

