# AGASTYA project index

**Last updated:** 21 November 2026 (Day 43 Stage 2 simulation continuation)
**Current architecture:** Stage 1 vision-based triage → Stage 2 robotic mechanical disassembly → Stage 3 hot-knife/foam-roller thermal separation → Stage 4 liberation, separation and silver recovery. See [current architecture](AGASTYA_ARCHITECTURE.md).

The current 19 November project-owner direction supersedes the 16 October manual Stage 2 baseline. Earlier stage maps and the 14 October electrostatic package remain preserved in `99_Archive/` as historical work. See the [current process architecture](AGASTYA_ARCHITECTURE.md).

## Start here

- [Start here guide](START_HERE.md)
- [Current architecture and interfaces](AGASTYA_ARCHITECTURE.md)
- [Project status](PROJECT_STATUS.md)
- [Project understanding audit](00_Project_Management/PROJECT_UNDERSTANDING_AUDIT.md)
- [Master task list](00_Project_Management/MASTER_TASK_LIST.md)
- [Decisions log](00_Project_Management/DECISIONS_LOG.md)
- [Change log](CHANGELOG.md)
- [File catalog](00_Project_Management/FILE_CATALOG.csv)
- [File inventory summary](00_Project_Management/file_inventory_summary.md) — path-level CSV is local-only and Git-ignored.

## Technical work

- [Research overview](01_Research/RESEARCH_OVERVIEW.md)
- [Engineering overview](02_Engineering/ENGINEERING_OVERVIEW.md)
- [Stage 2 robotic disassembly feasibility](02_Engineering/Stage_2_Robotic_Disassembly/STAGE2_ROBOTIC_DISASSEMBLY_FEASIBILITY_2026-11-19.md)
- [Stage 2 concept CAD plan and generator](02_Engineering/Stage_2_Robotic_Disassembly/simulation_outputs/concept_workcell_plan_notes.md)
- [Packaged robotic-arm CAD, electronics and simulations](robotic%20arm/README.md), with OBJ/STL/SCAD mesh sources, 71-point idealized IK, candidate angle envelope and static-moment sensitivity. The [Fusion API source](robotic%20arm/cad/Fusion/README.md) is prepared but not run; no F3D/STEP export exists. [Original Stage 2 basis](robotic%20arm/STAGE2_ARM_CONCEPT_BASIS_2026-11-20.md) includes the Day 43 addendum.
- [Stage 2 bench electronics models](robotic%20arm/electronics/README.md), including an LTspice transient result, and the [economic screen/model](agastya%20economics/README.md), including the three-layout quote template.
- [Stage 1 servo-gate control-interface demo](Agastya-EYE/demos/servo_gate/README.md)
- [Stage 3 roller/liberation placement review](Build%20Files%20and%20Steps/Stage%203/STAGE3_ROLLER_AND_LIBERATION_PLACEMENT_REASSESSMENT_2026-11-19.md)
- [Stage 4 architecture reassessment](Build%20Files%20and%20Steps/Stage%204/STAGE4_ARCHITECTURE_REASSESSMENT_2026-11-19.md)
- [Stage 3 thermal prototype package](Stage%203%20Prototype%20Development/README.md)
- [Stage 3 idealized EVA transient model](Agastya%20Thermal/STAGE3_EVA_TRANSIENT_MODEL_README.md)
- [Stage 3 thermal build plan](Build%20Files%20and%20Steps/Stage%203/STAGE3_BUILD_PLAN.md)
- [Stage 3 thermal development note](Build%20Files%20and%20Steps/Stage%203/STAGE3_THERMAL_DEVELOPMENT.md)
- [Stage 4 silver-removal research](Build%20Files%20and%20Steps/Stage%204/STAGE4_RESEARCH_COMPLETION_BRIEF_2026-10-08.md)
- [Stage 4 flotation reagent feasibility](01_Research/Stage_4_Flotation_Reagent_Investigation/AGASTYA_FROTH_FLOTATION_REAGENT_FEASIBILITY_REPORT.md)
- [Stage 4 mass-balance sensitivity model](03_Data_and_Analysis/Stage4/README.md)
- [India market and regulatory snapshot](01_Research/INDIA_SOLAR_PV_MARKET_REGULATORY_SNAPSHOT_2026-11-19.md)
- [Institutional validation programme](01_Research/Institutional_Collaboration/INSTITUTIONAL_VALIDATION_PROGRAMME_2026-11-19.md)
- [Stage 4 method comparisons](Build%20Files%20and%20Steps/Stage%204/STAGE4_METHOD_COMPARISON_AND_CALCULATIONS.md)
- [Source evidence register](01_Research/03_Source_Evidence/SOURCE_EVIDENCE_REGISTER.csv)
- [Data and analysis guide](03_Data_and_Analysis/DATA_AND_ANALYSIS_GUIDE.md)
- [Simulation/data README](Agastya%20Physics%20Simulation/README.md)
- [Agastya-EYE README](Agastya-EYE/README.md)
- [Stage 1 software validation run](Agastya-EYE/docs/STAGE1_VALIDATION_RUN_2026-11-19.md) — partial unit-test results and the uncompiled servo-demo boundary.
- [Current Stage 1 software validation](Agastya-EYE/docs/STAGE1_VALIDATION_RUN_2026-11-20.md) — all 65 tests and the synthetic workflow passed; hardware was not tested.
- [Stage 1 repair audit](Agastya-EYE/docs/SYSTEM_REPAIR_AUDIT_2026-11-19.md) and [Arduino servo-gate documentation](Agastya-EYE/docs/ARDUINO_SERVO_GATE.md).

## Project records and communication

- [Logbook index](04_Logbook/Logbook_Index.md) — original entries remain historical; no undocumented activity was backfilled.
- [Latest logbook entry](04_Logbook/PROJECT_LOGBOOK_DAY_43.md) with its [short counterpart](04_Logbook/Short%20Versions/DAY_43_SHORT_ENTRY.md) — AI-assisted first-person draft of the joint-angle/mass sensitivity screens, LTspice batch run and quote framework; 18 software checks passed, with no native CAD or physical validation. [Day 40](04_Logbook/PROJECT_LOGBOOK_DAY_40.md) records the owner-reported NML response and visit follow-up, not independently checked against the email thread. Days 31–33 remain short-only.
- [Session handoff](SESSION_HANDOFF.md) — current changes, checks and next action for continuation.
- [GitHub repository preparation](00_Project_Management/GITHUB_REPOSITORY_PREPARATION_2026-11-19.md) — repository state, current manifest and first-push outcome.
- [GitHub staged-file review](00_Project_Management/GITHUB_STAGED_FILE_REVIEW_2026-11-21.md) — refreshed Day 43 path/size inventory and exclusion rationale for the public sync.
- October presentation binaries are retained locally and excluded from the initial GitHub source set pending content and identity review.
- [Current presentation speaker notes](05_Presentation/Presentation_Script/AGASTYA_PRESENTATION_SPEAKER_NOTES_2026-10-20.md)
- [Presentation slide evidence register](05_Presentation/Final_Presentation/AGASTYA_SLIDE_EVIDENCE_REGISTER_2026-10-20.csv)
- [NCSC preparation guide](06_NCSC_Display/NCSC_PREPARATION_GUIDE.md)
- Printable bundles are retained locally and excluded from the initial GitHub source set pending content review.
- IRIS submission materials are retained locally and excluded from the initial GitHub source set pending identity/content review.
- Historical backup snapshots under `99_Archive/` remain local and are excluded to avoid duplicating superseded files.

## Evidence boundary

The 200,080 historical simulation rows are virtual scenarios/time histories, not physical samples or replicates. New thermal outputs are from an idealized EVA slab and the Stage 4 sweep is algebraic; neither establishes process quality, safety or AGASTYA performance. No AGASTYA thermal station, Stage 3 trial, Stage 4 silver-removal trial, assay, or recovered silver is documented. Published yields, settings and costs remain attributed to their source processes.
