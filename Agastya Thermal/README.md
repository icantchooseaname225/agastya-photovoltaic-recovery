# Agastya Thermal

**Current stage:** Stage 3 is thermal treatment/delamination, with guarded hot-knife glass-to-laminate separation as the working reference. Stage 4 is silver removal/recovery, with the method and required feed preparation still open. No thermal unit has been physically tested. See the root current architecture and engineering overview.

Agastya-EYE remains the shared inspection, passport, and stage-event application; it does not control thermal equipment.

## LCD demonstration sketch

- [Arduino LCD monitor](AgastyaThermalMonitor/AgastyaThermalMonitor.ino) and [wiring/operation notes](AgastyaThermalMonitor/README.md): shows live tool/interface probe readings and a manual countdown. Its 200 C reference and 55-second demo timer are illustrative values derived from the legacy thesis concept and literature benchmarks, not validated AGASTYA settings. No physical thermal trials are recorded.

## What the literature supports

- **Hot knife:** an established way to separate front glass from the EVA/cell/backsheet laminate. The IEA PVPS pilot-plant assessment reports approximately 50 seconds per module. NPC currently describes a 300 C knife and approximately 60 seconds per panel. These process times are references, not performance claims for Agastya. The IEA's 0.035 kWh/kg figure covers a broader treatment system, not Stage 3 heater energy. [IEA PVPS report](https://iea-pvps.org/wp-content/uploads/2023/07/Report_IEA-PVPS_T12-25-2023_LCA-PV-Recycling-Hot-Knife.pdf) | [NPC equipment](https://www.npcgroup.net/eng/solarproduct/dismantling)
- **Machine layout:** NEDO's account of NPC's development describes adopting a fixed knife and controlled panel feed after an earlier moving-blade arrangement struggled with uneven retired modules and output handling. Blade entry and glass breakage took further design iteration. [NEDO/NPC development account](https://webmagazine.nedo.go.jp/practical-realization/articles/202503NPC/)
- **Lower-temperature assisted peeling:** one 2026 study tested 100 C and 140 C oven heating for 60 minutes, then immediate manual peeling at about 20-30 N. This is a low-temperature comparison, not evidence for continuous high throughput. [Saitta et al. (2026)](https://doi.org/10.3390/green1010002)
- **Pyrolysis:** studies report EVA decomposition over much higher temperature ranges, including staged reactions around 284-527 C. This is distinct from softening EVA for mechanical separation. [Polymer Degradation and Stability (2023)](https://doi.org/10.1016/j.polymdegradstab.2023.110545)
- **Agastya's heated roller:** the claimed EVA stripping from cell material and the retained-heat benefit remain unvalidated. Commercial EVA scraping described by NPC applies to residue on the separated glass; it does not establish the proposed roller result on the cell/EVA sheet.

## Options

1. Establish hot-knife glass-to-laminate separation as the Stage 3 baseline, with metered energy, tool and material temperatures, cycle time, output masses, and quality scoring.
2. Compare lower-temperature assisted peeling as a separate condition if equipment and supervision support it.
3. Test the roller and heat reuse only after the baseline is repeatable. Define exactly what EVA-removal output is expected and measure whether retained heat reduces external energy without reducing output quality.
4. Keep pyrolysis as a later alternative requiring its own process, energy, emissions, and safety assessment.

The main open process decision is whether Stage 3 should output glass plus cell/EVA/backsheet laminate, or substantially EVA-free cells. The latter is a separate and currently unsupported process claim.

## Files

- [Multistage numerical simulation report](../Agastya%20Physics%20Simulation/Agastya_Physics_Simulation_2026-10-10.md): Stage 2/3/4 parameter sweep. Model output only; no thermal trial or Stage 4 performance is measured.
- [Initial simulation CSV](../Agastya%20Physics%20Simulation/Agastya_Physics_Simulation_2026-10-10.csv): 147,912 labeled scenario/model rows.
- [Follow-up virtual studies](../Agastya%20Physics%20Simulation/followup_virtual_experiments.csv): 52,168 additional rows covering cooldown, numerical time-step convergence, capacity, screen-cut and conditional Ag-grade arithmetic.
- [Experiment register](../Agastya%20Physics%20Simulation/experiment_register.csv), [data dictionary](../Agastya%20Physics%20Simulation/data_dictionary.csv) and [procedures/results](../Agastya%20Physics%20Simulation/PROCEDURES_AND_RESULTS.md).

- [Stage 3 thermal development note](../Build%20Files%20and%20Steps/Stage%203/STAGE3_THERMAL_DEVELOPMENT.md): equations, evidence table, test plan, measurements, and unresolved decisions.
- [Stage 3 prototype build plan](../Build%20Files%20and%20Steps/Stage%203/STAGE3_BUILD_PLAN.md): recommended first station, build phases, measurement plan, cost references, and validation boundaries.
- [Stage 3 thermal workbook](../Build%20Files%20and%20Steps/Stage%203/stage3_thermal_data.xlsx): sourced literature values, editable assumptions, formula-driven calculations, and a blank trial log.
- [Stage 4 literature review](../Build%20Files%20and%20Steps/Stage%204/STAGE4_LITERATURE_REVIEW.md): critical review of the thesis's eddy-current claim and a research path for a measurable Stage 4 pilot.
- [Stage 4 feasibility review](../Build%20Files%20and%20Steps/Stage%204/STAGE4_FEASIBILITY_REVIEW.md): system-level verdict on the proposed separator, Stage 3 interface, alternatives, and go/no-go gates.
- [Stage 4 feed requirements and next steps](../Build%20Files%20and%20Steps/Stage%204/STAGE4_FEED_REQUIREMENTS.md): feed acceptance gates and phased pilot setup.
- [Stage 4 blank trial-log template](../Build%20Files%20and%20Steps/Stage%204/STAGE4_TRIAL_LOG_TEMPLATE.csv): blank fields only; no test data entered.
- [Stage 4 equipment-access inventory](../Build%20Files%20and%20Steps/Stage%204/STAGE4_EQUIPMENT_INVENTORY_TEMPLATE.csv): check existing/borrowable resources before buying anything.
- [Logbook, Days 3–4](../04_Logbook/PROJECT_LOGBOOK_DAY_3_4.md), [Days 5–8](../04_Logbook/PROJECT_LOGBOOK_DAY_5_8.md), [Day 9](../04_Logbook/PROJECT_LOGBOOK_DAY_9.md), [Day 10](../04_Logbook/PROJECT_LOGBOOK_DAY_10.md), and [Day 11](../04_Logbook/PROJECT_LOGBOOK_DAY_11.md).

## Kept in Agastya-EYE

The Stage event API and shared interoperability documentation remain in Agastya-EYE because they support multiple stages and the panel passport. Stage 3 energy and duration units are supported for observations. EYE remains a record interface, not a heater controller or safety interlock.

