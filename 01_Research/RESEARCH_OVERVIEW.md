# AGASTYA research overview

## Research question

Crystalline-silicon solar cells carry thin printed silver contacts bonded to silicon and interconnects. AGASTYA asks whether a defined end-of-life panel feed can be prepared through thermal treatment and then processed to remove/recover silver, with traceable streams and a measured silver balance. No AGASTYA module, silver assay, or recovered-silver result is documented.

## Current four-stage sequence

The current owner direction is authoritative: **Stage 1 vision-based triage → Stage 2 robotic mechanical disassembly → Stage 3 hot-knife/foam-roller thermal separation → Stage 4 material liberation, separation and silver recovery.** Sampling, assay, mass accounting, chain of custody and uncertainty validate every stage; they are not Stage 4 process operations. See the [current architecture](../AGASTYA_ARCHITECTURE.md) and [provisional Stage 3/Stage 4 interface](../STAGE3_STAGE4_INTERFACE.md).

| Stage | Intended function | Expected interface | Current evidence and required demonstration |
|---|---|---|---|
| 1. Inspection/routing | Identify, inspect, electrically isolate and route incoming modules. | Traceable module and documented condition/route. | Proposed only; no AGASTYA panel intake is documented. |
| 2. Robotic mechanical disassembly | Use a robotic-arm-centered workcell, positive panel fixture and justified task-specific tooling/indexing for frame, junction-box and cable operations. | Separated component streams and traceable Stage 3 feed. | Architecture and 2D reach screen only; no robot, CAD, force data or physical trial. |
| 3. Thermal separation | Hot knife followed by the foam-roller concept; assess a modular liberation step at the outlet. | Expected glass and cell/EVA/backsheet laminate streams. | Prior hot-knife-only model; roller has no specification or integrated test. No physical trial. |
| 4. Material liberation, separation and silver recovery | Characterize feed; liberate/partition silver-bearing material and route an accepted concentrate to recovery/refining. | Measured concentrate/product and accounted residual streams; product form depends on the selected process. | Function set; process route, feed, facility, assay/QC and receiver requirements remain open. No AGASTYA separation/recovery trial is documented. |

## 19 November architecture update

Published industrial process flow supports evaluating mechanical liberation directly after thermal glass separation, but not a cost or recovery advantage. The Stage 4 architecture review removes conventional ECS from the default and compares a dry size-classification baseline with silver-specific flotation on compatible prepared feed. See the [Stage 2 review](../02_Engineering/Stage_2_Robotic_Disassembly/STAGE2_ROBOTIC_DISASSEMBLY_FEASIBILITY_2026-11-19.md), [Stage 3 review](../Build%20Files%20and%20Steps/Stage%203/STAGE3_ROLLER_AND_LIBERATION_PLACEMENT_REASSESSMENT_2026-11-19.md), and [Stage 4 review](../Build%20Files%20and%20Steps/Stage%204/STAGE4_ARCHITECTURE_REASSESSMENT_2026-11-19.md).

## Why the process is difficult

A PV panel is a bonded assembly of front glass, encapsulant, cells, printed contacts, ribbons, backsheet or rear glass, frame, cables and junction box. Silver is a small fraction of the total mass and may remain attached to silicon or polymer after glass separation. Crushing and screening can create mixed particles; size or conductivity alone does not identify pure silver. A silver-coloured particle is not proof of elemental silver.

The Stage 3 hot-knife baseline separates the front glass from a cell/EVA/backsheet laminate. It does not prove that EVA has been removed or that silver is liberated. Stage 4's input condition therefore depends on the silver-removal route selected. If that route needs additional cell liberation, EVA/backsheet removal or size reduction, the operation must be separately named, assessed and measured.

## Stage 3 thermal evidence

- The IEA PVPS hot-knife LCA uses pilot-plant data and reports about 50 seconds per module. Its 0.035 kWh/kg figure covers the reported take-back/hot-knife treatment boundary, not an isolated Agastya heater measurement. [IEA PVPS Task 12-25:2023](https://iea-pvps.org/wp-content/uploads/2023/07/Report_IEA-PVPS_T12-25-2023_LCA-PV-Recycling-Hot-Knife.pdf)
- NPC describes commercial hot-knife glass separation at about 60 seconds per panel and a 300 °C knife; its product line describes a separate EVA scraper. These are supplier claims and not Agastya specifications. Page checked 20 October 2026. [NPC process page](https://www.npcgroup.net/eng/solarproduct/dismantling)
- A 2026 coupon study heated specimens at 100 °C or 140 °C for 60 minutes and then mechanically peeled them. This is useful for a slow thermal-softening comparison, not proof of sub-minute throughput. [Saitta et al.](https://doi.org/10.3390/green1010002)
- EVA pyrolysis studies concern decomposition at substantially higher temperatures. Pyrolysis is a separate process from localized softening-assisted mechanical separation and is not a proposed Stage 3 setting. [2023 study](https://doi.org/10.1016/j.polymdegradstab.2023.110545)

The Stage 3 review and prototype plan are in [Build Files and Steps/Stage 3](../Build%20Files%20and%20Steps/Stage%203/) and the [thermal prototype package](../Stage%203%20Prototype%20Development/README.md). Literature values do not establish Agastya's temperature window, energy use, throughput, output quality or safety.

## Stage 4 silver-removal evidence

Existing Stage 4 research compares methods that may remove or concentrate silver, but no method has been selected for AGASTYA:

- **Mechanical size classification** can direct silver-bearing material into particular size fractions for specific feeds. It is feed preparation or pre-concentration; it does not itself produce pure silver. Report mass yield, Ag grade and Ag recovery separately.
- **Electrostatic separation** has been studied on PV-derived material, but some results measure silicon or co-concentrate Ag, Al and Si. It is not current Stage 3 and does not automatically extract Ag from a composite cell fragment.
- **Froth flotation** has recent Ag-specific laboratory evidence on delaminated and ground cell feed using water and reagents. It is a specialist comparison, not a prediction for AGASTYA or a student-build procedure.
- **Chemical/electrochemical extraction** studies report silver dissolution or separation for prepared feed. These methods need route-specific hazard review, validated assay, wastewater/residue handling and qualified laboratory controls.

See the [Stage 4 research folder](../Build%20Files%20and%20Steps/Stage%204/) for feed requirements, feasibility, method comparisons and readiness gaps. The findings are evidence for comparison, not an approved operating recipe.

## Silver-bearing material and recovered silver

An enriched fraction or concentrate can contain Ag along with silicon, copper, aluminium, glass and polymer. A silver-bearing solution is also not purified silver. Stage 4's specific output claim must match the selected method: silver-bearing concentrate, solution, or recovered solid. A metallic-silver purity claim requires further processing and a suitable assay. No silver-bearing product, solution or metal has been produced by AGASTYA.

## Measurement needed for a valid result

For every feed and output, record sample identity, source, mass, preparation, representative subsampling, assay basis, instrument/method, detection limits, uncertainty and custody. Include every product, residue, dust/filter catch and sample withdrawal in the balance. Report separately:

- mass yield and mass-balance closure;
- silver grade/concentration;
- silver recovery to the stated product;
- enrichment factor;
- residual/unaccounted silver and uncertainty;
- product purity only when measured with a suitable method.

One visible split, literature percentage or model run does not demonstrate recovery. Use a qualified lab to confirm that its sample preparation and analytical method are appropriate for the actual PV matrix.

## Source-qualified inventory arithmetic

The project records contain different literature silver values, including a 300 ppm secondary-source scenario and a 600 g/t publisher-abstract value from Dias et al. Secondary excerpts also state 630 g/t, which remains unresolved against the accessible source. These numbers come from different feeds and bases; they are neither measurements of one population nor an AGASTYA assay. Keep each value tied to its source and do not use it as measured project feed composition. See the [source evidence register](03_Source_Evidence/SOURCE_EVIDENCE_REGISTER.csv) and [data guide](../03_Data_and_Analysis/DATA_AND_ANALYSIS_GUIDE.md).

## What is still missing

The workspace has no verified feed source, module identity, thermal station, qualified facility access, Stage 3 measured output, Stage 4 selected route, receiver specification, matrix-validated silver assay, approved safety plan, or waste-handling pathway. These are gates before procurement, active heating or silver-removal trials. The [master task list](../00_Project_Management/MASTER_TASK_LIST.md) records the next actions.




