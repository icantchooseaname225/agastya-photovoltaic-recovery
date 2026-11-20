# AGASTYA engineering overview

**Reviewed:** 19 November 2026. The current design direction is defined in [AGASTYA_ARCHITECTURE.md](../AGASTYA_ARCHITECTURE.md).

| Stage | Engineering function | Proposed input/output | Evidence/status |
|---|---|---|---|
| 1. Vision triage | Inspect, record, classify cautiously, and route or hold. | Identified module → passport and advisory route. | Application implemented. Limited image benchmarks; not field validated, not an electrical safety check and not composition assay. |
| 2. Robotic mechanical disassembly | Robot arm manipulates task-specific tools while a fixture supports the module; compare arm/tool changer with dedicated actuators and panel indexing/rail. | Accepted isolated module → separated frame, cable/J-box and traceable laminate streams. | No robot/hardware/test. A 2 m four-axis envelope, Fusion script, AutoCAD plan/side DXF, and separate electrical/cost screens are concept-only. Fusion script not run; DXF not opened in AutoCAD. See [Stage 2 feasibility](Stage_2_Robotic_Disassembly/STAGE2_ROBOTIC_DISASSEMBLY_FEASIBILITY_2026-11-19.md) and [concept basis](Stage_2_Robotic_Disassembly/STAGE2_ARM_CONCEPT_BASIS_2026-11-20.md). |
| 3. Thermal separation | Hot knife followed by the foam-roller concept; measure glass/laminate separation and consider a modular liberation step adjacent to the outlet. | Prepared module → expected glass plus cell/EVA/backsheet laminate; later liberation feed if validated. | Prior hot-knife conduction simulation; no integrated roller model or physical trial. See [roller/liberation placement review](../Build%20Files%20and%20Steps/Stage%203/STAGE3_ROLLER_AND_LIBERATION_PLACEMENT_REASSESSMENT_2026-11-19.md). |
| 4. Liberation, separation, silver recovery | Characterize feed; compare dry size classification and silver-specific flotation; route concentrate for qualified refining. | Measured feed → assayed concentrate/product and accounted residues. | Route open; no AGASTYA feed assay or process run. Conventional ECS is conditional, not baseline. See [Stage 4 reassessment](../Build%20Files%20and%20Steps/Stage%204/STAGE4_ARCHITECTURE_REASSESSMENT_2026-11-19.md). |

## Stage 2 workcell direction

The robot must not be assumed to lift a large PV module. A rigid adjustable support fixture carries the panel and reacts contact forces. The arm can provide flexibility for tool operations, but frame release and junction-box/cable removal involve different approach directions and contact conditions. A linear rail, panel indexer, quick changer, or dedicated mechanism may be needed. The 2D model suggests that a nominal 1.5 m radius is insufficient for all perimeter points from one fixed position in its illustrative layout; it does not establish a real robot's reachable or safe workspace.

The current CAD adds an illustrative 2 m four-axis arm envelope from a 1,100 mm upper link and 900 mm forearm. It is not an Autodesk Fusion-tested assembly, not a motion study and not a manufacturing drawing. The electronics sketches deliberately separate a future OEM safety architecture from a small manual-jog classroom demonstration. Current catalogue prices inform only the educational comparison; they do not establish process-cell cost.

Before actuator sizing, measure module geometry, tool mass and center of gravity, force/moment profiles, restraint loads and cycle sequence. A later 3D model must use manufacturer kinematics and include joint limits, orientation, collision, deflection and safety constraints.

## Stage 3/4 interface

The Stage 3 sequence is currently a hot knife followed by a foam roller. Local older design notes and simulations describe hot-knife thermal transfer only; they do not describe a tested roller. The first expected stream remains a glass sheet and cell/EVA/backsheet laminate. Evidence from a published industrial line supports testing liberation downstream of hot-knife treatment, so the design should reserve a modular, contained, bypassable unit at the Stage 3 outlet. Formal stage assignment should follow measured feed quality and whole-line data.

For Stage 4, distinguish liberation, separation, concentration, recovery and purification. The previous proposed mechanical liberation → conventional rotating ECS → flotation train is not supported as a default because available ECS evidence does not test fine silver metallisation on silicon-cell feed. Dry size classification is a low-complexity baseline; flotation is the strongest direct silver-concentration candidate found, but requires compatible prepared feed and a qualified facility. Neither route has been tested by AGASTYA.

## Engineering evidence boundary

Do not report measured arm reach, force, repeatability, cycle time, roller behavior, thermal energy, silver recovery, product grade, purity, cost or profitability from literature or scenario models. No purchase, robot selection or process build is justified until the feed, facility, safety and measurement gates are met.
