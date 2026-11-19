# Stage 4 Method Comparison and Calculations


> **Architecture correction (16 Oct 2026):** Current Stage 4 is silver removal/recovery. This file's size-classification, ECS, assay, or hand-off descriptions are prior route research, not the current stage definition. Treat size reduction/classification as possible feed preparation; assay and mass accounting validate the stage. See [Stage 4 architecture and route decision](STAGE4_ARCHITECTURE_AND_ROUTE_DECISION_2026-10-16.md).

**Updated:** 7 October 2026  
**Status:** literature-based engineering comparison; no Stage 4 equipment trial or PV feed processing has occurred.

## Decision summary

Stage 4's function is silver removal/recovery. Do not build or buy an eddy-current separator as though it alone removes silver from the Stage 3 output. First establish what Stage 3 can deliver, characterize the cell/EVA/backsheet laminate, and specify the silver-bearing product form. Compare preparation and removal routes against that actual feed.

Use this order for Stage 4 development:

1. **Near-term, no-spend work:** document feed requirements, check access to supervised lab equipment and analytical services, and use published data for design calculations. No PV crushing or high-voltage build is part of this desk phase.
2. **Primary Stage 4 research candidate:** contained controlled comminution and multi-cut size classification directly on the documented laminate, without assuming EVA has first been removed. PV studies report Ag partitioning into fine fractions, not pure Ag; a different mild-crushing study targeted cell-bearing coarse fractions and still used pyrolysis downstream. The target stream must be selected by assay and receiver need. Any comminution must be specified and supervised with glass and dust controls.
3. **Keep eddy-current / electrodynamic sorting as a conditional branch:** evaluate it only on dry, liberated conductive particles of a defined size. Conventional rotating ECS, specialized fixed-frequency EDX and roll electrostatic separation are different devices and must not be treated as interchangeable.
4. **If the goal becomes a silver concentrate and a qualified laboratory partner is available:** add froth flotation to the research comparison. A 2026 PV-cell study is promising, but its water, reagents, prepared feed, flotation cell and assay requirements put it outside Agastya's current mobile/no-on-site-chemistry scope.
5. **Do not build high-voltage pulse crushing or electrostatic hardware at school.** These remain literature options requiring engineered equipment, guarding, qualified supervision and a defined feed.

The current candidate claim should be: **Stage 4 will investigate a qualified route to remove/recover silver from Stage 3-derived cell-bearing material.** The exact method, additional feed preparation and product form remain open. Do not claim pure silver or a measured recovery based only on dry size partitioning or electrostatic separation.

See [Stage 4 Development Roadmap](STAGE4_DEVELOPMENT_ROADMAP.md) for gates, sequence, method selection, cost inputs and the next action.

## How to read the numbers

- **Grade** is the target material's share of a product stream.
- **Recovery** is the share of the target material in the feed that reports to the selected product.
- **Enrichment/upgrade** is product grade divided by feed grade.
- A high recovery does not imply a high grade, and vice versa.
- The calculations below reproduce or normalize reported literature results. They are not Agastya performance forecasts. No purchase price or full-line operating cost can be calculated from these papers because they do not provide a comparable Agastya equipment quote, feed rate, duty cycle, local electricity tariff, assay charge or labor boundary.

## Methods compared

| Method | Target and useful feed | Literature signal | Main limitation for Agastya | Current role |
|---|---|---|---|---|
| Crush-and-sieve | Size-selective split of disassembled/encapsulated PV-derived material; candidate silver-bearing fines and polymer-rich coarse material | Sim et al. found >90% of polymer retained in larger fractions and 70%/80% of total silver in the finest fraction for two feed categories | Silver is enriched, not recovered as pure metal; the study's feed and crushing conditions matter; dust/glass safety and actual Stage 3 transfer remain unverified | Best near-term PV-specific method to evaluate after feed/safety gate |
| Integrated comminution and sieving | Multi-fraction classification of dismantled module waste | Juyo Salazar et al. (2024) report 94.12% of Ag in fractions <0.25 mm; 99.37% of Cu in a 0.5–2.00 mm fraction that was still 64.04% polymer | This is distribution across the study's size fractions, not Ag grade or purity; mixed materials and upstream dismantling remain | Supports testing multiple size cuts and measuring each separately; not a fixed screen specification |
| Mild crushing for cell-bearing fraction | Concentrate silicon-cell fragments into a coarser size fraction for subsequent processing | Yan et al. reported +1 mm fraction at 25.36% mass yield and 50.32% cell recovery after 10 s; the subsequent route uses gravity separation and pyrolysis | Target is cell recovery, not Ag fines; about half of cells are not in the initial selected fraction; clean cells require further treatment | Comparator if receiver wants cells; not the chosen Ag-bearing-fines baseline |
| High-voltage pulse crushing | Selective fracture/liberation of layered module materials; enriches Ag into fine fractions | Zhao et al. reported Ag enrichment factors of 3.08 at 54.07% recovery, or 1.67 at 89.41% recovery at stronger field/more pulses | Specialized high-voltage comminution; recovery/grade trade-off; does not produce refined Ag and is not a school DIY machine | Literature comparator only; possible supervised partner-lab route |
| Conventional rotating ECS | Coarser liberated non-ferrous conductive particles separated from nonconductors | Established principle for metal/non-metal sorting | Does not demonstrate silver extraction from Ag-printed silicon fragments; fine and composite particles reduce confidence | Keep only for a defined coarse liberated-conductor feed |
| Fixed high-frequency EDX / EECS | Fine conductive/nonconductive particles, with specialized excitation and geometry | PV-like 1–3 mm surrogate mixtures: reported >85% grade and recovery, ~10 kg/h, 68 kWh/short ton | Not the thesis's conventional rotating drum; prepared surrogate blend, not complete PV waste; high specific energy in the reported setup | Research benchmark, not a build specification |
| Corona electrostatic separation after size-controlled milling | Classified PV cell fractions; separates by electrical response | Mbam (2026 MSc thesis): rod-mill surface abrasion followed by hammer milling; for 0.1–0.71 mm, >80% reported recovery across glass, Si and metallic fractions with ~53% Si grade at its selected condition | Thesis evidence, not peer-reviewed journal; specialized mill and 30 kV corona drum; separately tuned coarse fraction needed; do not transfer conditions | Best dry multi-method comparison to keep as a partner-lab option, not the first low-complexity build |
| Roll electrostatic separation | Fine classified PV powders; separates by electrical response | Li et al.: 0.30–0.45 mm; 15 kV, 30 rpm; 91.0% Si proportion and 48.9% Si recovery | Fine powder and high voltage; reported settings are apparatus-specific; high grade with modest recovery | Later supervised comparison if silicon-rich powder is the target |
| Froth flotation (2026) | Delaminated, ground c-Si cell feed; selective concentration of exposed metallic silver | Rougher tests in tap water: 97.55% Ag recovery, 32.2× upgrade; rougher-cleaner result in ultrapure water: ~47 wt% Ag at 86.5% recovery | Reagent/water circuit, lab flotation cell, delaminated and ground feed, ICP-MS assay; not dry or mobile/no-chemistry | Important new silver-focused benchmark; only with a qualified partner lab |
| Localized electrolyte-jet recovery (2026) | Downstream chemical extraction from end-of-life silicon cells with surface silver | 5 V and circulating 12 wt% nitric acid: 90.2% surface Ag dissolved in 7 minutes; >95% after 30 minutes | Uses nitric-acid electrolyte and a purpose-built cell; not a dry pre-concentration step | Refiner-side technology context only; outside Agastya onboard scope |
| Vibration separation | Coarse silicon wafer fragments from glass | One study reports 84.47% metal-Si grade at 83.73% recovery and 98.95% glass recovery under its optimized condition | Objective is wafer/glass split, not Ag separation; feed and equipment differ | Optional upstream cell/glass comparator, not Stage 4 metal refining |

## Reproducible calculations

### A. Specialized PV-like EDX energy normalization

Smith et al. report **68 kWh per short ton** of sorted material, with throughput roughly **10 kg/h**.

Using 1 short ton = 907.185 kg:

```text
Specific energy = 68 kWh / 907.185 kg
                = 0.07496 kWh/kg
                = 74.96 Wh/kg
                = 74.96 kWh/metric tonne
```

At 10 kg/h, if that throughput and energy boundary apply simultaneously:

```text
Implied average power = 0.07496 kWh/kg × 10 kg/h
                      = 0.7496 kW (about 0.75 kW)
```

This is an arithmetic implication, not an independently reported motor rating. The reported grade/recovery (>85%) and throughput belong to the study's specialized EDX and prepared 1–3 mm surrogate mixtures; do not transfer them to an Agastya drum.

### B. Industrial EDX one-tonne mass balance (not PV)

Nagel et al. report a Zorba feed with 71.4% Al, 68.3% mass reporting to the throw product, 97.6% Al grade in that product, and 93% Al recovery. Normalize the reported mass split to a 1,000 kg feed:

```text
Feed Al                     = 1,000 × 0.714 = 714 kg Al
Throw product mass          = 1,000 × 0.683 = 683 kg
Al in throw product         = 683 × 0.976 = 666.6 kg Al
Calculated Al recovery      = 666.6 / 714 × 100 = 93.36%
Non-Al in throw product     = 683 − 666.6 = 16.4 kg
Drop product mass           = 1,000 − 683 = 317 kg
Reported specific energy    = 7.2 kWh/t = 7.2 Wh/kg
Implied average power        = 7.2 kWh/t × 250 kg/h = 1.8 kW
```

The calculated 93.36% is consistent with the paper's rounded 93% report. It demonstrates why product grade and recovery require both stream mass and assay. Zorba is industrial mixed scrap, not PV feed; its results do not establish an Agastya throughput or energy target.

### C. Crush-and-sieve silver distribution

For each 100 units of silver initially present in the studied feed:

```text
EVAc-category feed: up to 70 units report to the finest fraction (F4).
MP-category feed:   up to 80 units report to the finest fraction (F4).
```

The paper also reports >90% of total polymer retained in larger fractions, and polymer retention above 83% in F1 (>1 mm) and above 70% in F1+F2 depending on the reported comparison. These percentages describe component distribution across size fractions. They do **not** say that F4 is 70–80 wt% silver, nor do they establish the mass yield, silver product grade or saleable silver recovery. Those require the feed assay and fraction masses for the specific material.

### D. 2024 multi-cut comminution and sieving

Juyo Salazar et al. report 94.12% of total Ag distributed into the <0.25 mm size fraction. On a normalized 100 units of feed Ag:

```text
Silver in <0.25 mm fraction = 94.12 units (reported distribution)
Silver outside that fraction = 100 − 94.12 = 5.88 units
```

The study also reports 99.37% of Cu in the 0.5–2.00 mm cut, which contained 76.85% glass and 64.04% polymer. These results show that fraction boundaries can route different values to different cuts, but also that a fraction can carry substantial unwanted material. The source does not provide enough mass-yield and Ag-assay information here to calculate the <0.25 mm product grade or its mass per kg of feed.

### E. High-voltage pulse crushing: recovery/enrichment trade-off

Normalize to 100 units of silver in the feed. The study reports two operating regimes:

| Literature regime | Silver to selected fraction per 100 units in feed | Enrichment factor | Interpretation |
|---|---:|---:|---|
| Lower field strength / fewer pulses | 54.07 units | 3.08× feed grade | Higher enrichment, lower recovery |
| Higher field strength / more pulses | 89.41 units | 1.67× feed grade | Higher recovery, lower enrichment |

If feed grade is `g` wt%, the corresponding product grades implied by the reported enrichment ratios are `3.08 × g` and `1.67 × g`, respectively, subject to the paper's enrichment definition and its tested feeds. Because Agastya's feed grade is unknown, an absolute product grade or concentrate mass cannot be calculated. Glass in a 0.5–4 mm fraction was reported at >98% purity in that study, but this is a separate product claim and does not establish silver purity.

### F. Electrostatic silicon separation: calculate on contained silicon, not total panel mass

Li et al. report an electrostatic product with 91.0% Si proportion and 48.9% Si recovery. Let `x` be the Si mass fraction in the **actual classified powder fed to the separator**. On a 1 kg powder-feed basis:

```text
Si in feed                         = x kg
Si in selected product             = 0.489x kg
Selected product mass               = 0.489x / 0.910 = 0.5374x kg
Non-Si mass in selected product     = 0.5374x − 0.489x = 0.0484x kg
```

The paper says 82.8 wt% of the silicon in the mechanically crushed c-Si waste was distributed into the mixed-powder stream before electrostatic separation. That 82.8% is an upstream distribution of total silicon, **not** the silicon grade of the separator feed and not the separator's recovery. We cannot calculate kilograms of Si product per kilogram of whole module without the panel composition and each upstream mass split.

### G. 2026 froth-flotation benchmark

The 2026 study reports rougher flotation in tap water at **97.55% Ag recovery** and **32.2× upgrade**, with roughly **2.8 wt% of original feed reporting to the leach-bound concentrate**. A rougher-cleaner sequence in ultrapure water reports approximately **47 wt% Ag at 86.5% recovery**. Thus, for each 100 units of feed silver, the tap-water rougher result reports about 97.55 units to its concentrate; the rougher-cleaner example reports 86.5 units while raising product grade to about 47 wt%.

The reported dosage basis was 150 g/t dry feed for the chosen reagent condition. This normalizes to:

```text
150 g reagent / 1,000 kg feed = 0.15 g/kg feed
For a 100 g bench sample:     0.015 g = 15 mg at that dosage basis
```

The paper used two reagents. The 15 mg value is only the mass equivalent of the stated dosage basis; verify the exact per-reagent addition schedule from the experimental protocol before attempting any replication. The paper's feed consisted of delaminated cells that were ground to improve silver exposure; it used flotation cells and ICP-MS-based silver assay. The high recovery is **not** from untreated laminate, dry separation, or ECS. Even where rougher concentrate is only a small feed mass fraction, water/reagent handling, tailings and verification remain required.

### H. Downstream localized electrolyte-jet study (not Stage 4)

Zhang et al. (2026) report a purpose-built electrolyte-jet system using 5 V and circulating 12 wt% nitric acid: 90.2% of surface metallized Ag dissolved after 7 minutes and >95% separation after 30 minutes. The output is a chemical extraction result, not a dry concentrate yield. Do not compare its Ag recovery directly with dry mechanical grade/recovery as though they were the same process boundary. It provides a possible central-refiner research direction after Agastya hands off a characterized solid; it is explicitly outside the mobile no-on-site-chemistry unit.

### I. Vibration separation check (wafer/glass objective)

The paper's abstract gives +0.83 mm as the optimized size, while its conclusion states +3 mm; treat the optimum feed-size notation as inconsistent in the source. The other listed conditions are 0.15 t/h, 190 V vibration supply, 48 Hz, 8° horizontal and 3° longitudinal inclination. Reported outputs were 84.47% metal-Si grade at 83.73% recovery for the silicon-wafer product, and 65.69% SiO₂ grade at 98.95% recovery for glass. This is a potentially relevant **wafer/glass liberation** comparison; it is not a silver concentration result. The 190 V is the study's vibration condition, not a recommended Agastya electrical setting.

## What can and cannot be calculated for Agastya now

**Stage 4 spend for this desk review: ₹0.** No equipment, samples, reagents or services were purchased. The practical route remains to verify free/borrowed supervised equipment access first. Any future quote should be recorded separately for separator access, feed preparation, assay, consumables, transport and waste handling; there is not enough information to invent a reliable total today.

| Quantity | Status | Why |
|---|---|---|
| Literature-specific energy for the two EDX examples | Calculable from reported kWh/t, one conditionally derived power estimate | Feed throughput and energy boundary are given for those specific studies |
| Literature grade/recovery and normalized contained-metal splits | Calculable where feed/product assays and mass splits are published | Calculations above preserve the study's system boundary |
| Stage 4 product mass or Ag yield from Agastya's Stage 3 laminate | Not calculable yet | No validated delamination/liberation step, feed mass, size distribution or assay |
| ECS or EDX capital cost for Agastya | Not calculable from the reviewed evidence | No matched vendor quote or validated separator specification; a student-built drum is not a comparable industrial unit |
| Electricity cost | Not calculable for Agastya | No selected machine, measured kWh/run or applicable tariff; use `measured kWh × local tariff` only after a real trial |
| Silver value, payback or profitability | Not calculable responsibly | Requires representative Ag assay, recovered mass, buyer specification/price, transport, labor, energy and residual handling costs |

## Next steps, in order

1. Keep the existing equipment inventory blank until each item is physically verified as available, borrowed or priced. Do not present a placeholder as a quote.
2. Close the Stage 3-to-Stage 4 feed gap: define whether Stage 3 will deliver a laminate, delaminated cell pieces, liberated particles or a characterized powder. Record which is demonstrated versus proposed.
3. Agree the Stage 4 target product first: silver-bearing fines, silicon-rich powder, coarse non-ferrous conductor, or separated cell/glass. These objectives select different methods.
4. Ask a qualified lab/supervisor what guarded equipment and assay access exists. If none exists, continue with a design study and no-spend evidence review; do not improvise high-voltage or crushing apparatus.
5. If the lab can support a safe comparison, start with a mass-balanced sieve classification baseline on traceable feed, then add one method that matches the stated objective. Preserve feed, product and residue aliquots for assay.
6. For each future run, capture mass, size class, process conditions, energy, all output fractions and assay provenance. Enter the run in the trial log and link the record to the EYE batch manifest and source Stage 3 panel events.

## Sources

- Sim, Y. et al. (2023), “A facile crush-and-sieve treatment for recycling end-of-life photovoltaics,” *Waste Management* 156, 97–106. [DOI](https://doi.org/10.1016/j.wasman.2022.11.023).
- Yan, G. et al. (2025), “An effective process for Si-cells enrichment of end-of-life photovoltaic panels based on mild crushing,” *Process Safety and Environmental Protection* 204, 108091. [DOI](https://doi.org/10.1016/j.psep.2025.108091).
- Zhao, P. et al. (2020), “A novel and efficient method for resources recycling in waste photovoltaic panels: High voltage pulse crushing,” *Journal of Cleaner Production* 257, 120442. [DOI](https://doi.org/10.1016/j.jclepro.2020.120442).
- Smith, Y.R., Nagel, J.R. & Rajamani, R.K. (2017), “Electrodynamic Eddy Current Separation of End-of-Life PV Materials.” [DOI](https://doi.org/10.1007/978-3-319-52192-3_37); [DOE project report](https://www.energy.gov/documents/61smithuutahpostdocawardpdf).
- Nagel, J.R. et al. (2020), “Electrodynamic Sorting of Industrial Scrap Metal,” *KONA* 37, 258–264. [DOI](https://doi.org/10.14356/kona.2020015).
- Li, J. et al. (2023), “Recycling Si in waste crystalline silicon photovoltaic panels after mechanical crushing by electrostatic separation,” *Journal of Cleaner Production* 415, 137908. [DOI](https://doi.org/10.1016/j.jclepro.2023.137908).
- Juyo Salazar, R.B. et al. (2024), “Streamlined process with a sustainable approach for photovoltaic module recycling,” *Sustainable Materials and Technologies* 41, e01047. [DOI](https://doi.org/10.1016/j.susmat.2024.e01047).
- Saffarian, H., Galvin, K.P. & Firouzi, M. (2026), “Rethinking silver recovery pathways in end-of-life photovoltaic recycling using froth flotation,” *Minerals Engineering* 242, 110189. [DOI](https://doi.org/10.1016/j.mineng.2026.110189).
- Zhang, Y. et al. (2026), “Near-complete Ag recovery from silicon solar cells via localized electrolyte-jet recycling,” *Separation and Purification Technology* 385, 136440. [DOI](https://doi.org/10.1016/j.seppur.2025.136440).
- Mbam, N.M. (2026), *Variant Study of Dry Beneficiation Methods for PV Module Cell Fractions*, MSc thesis, Montanuniversität Leoben. [DOI](https://doi.org/10.34901/mul.pub.2026.194). Exploratory thesis evidence, not peer-reviewed journal evidence.
- “Research on new process for separation of silicon wafers and glass from decommissioned photovoltaic module,” *Physicochemical Problems of Mineral Processing* 58(6) (2022), 151679. [DOI](https://doi.org/10.37190/ppmp/151679).


