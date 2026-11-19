# AGASTYA current process architecture

**Current revision:** 19 November 2026  
**Authority:** current project-owner direction, superseding the manual Stage 2 baseline recorded on 16 October 2026. Historical records remain unchanged and are identified as historical where needed.

## Four-stage sequence

| Stage | Current role | Intended input and output | Current evidence status |
|---|---|---|---|
| **1. AGASTYA-EYE — vision-based triage** | Capture and review module images, record verified measurements, identify likely condition, and route the module or hold it for human review. | Incoming identified module → inspection passport and an advisory route. | The local application and image models are implemented. The RGB checkpoint has a small group-aware held-out benchmark; it is not field-validated and does not establish electrical condition, material composition, or silver content. No production routing trial is recorded. |
| **2. Automated mechanical disassembly — robotic-arm workcell** | Mechanically disassemble accepted modules, with a robotic arm as the flexible tool-manipulation element, supported by a fixture and any justified indexer/rail or dedicated mechanism. Candidate operations include frame, junction-box, and cable removal. | Isolated, accepted module → traceable frame, cable/box and laminate streams for Stage 3. | Architecture direction is set; no robot, end effector, fixture, motion plan, or physical disassembly has been validated. A new 2D perimeter reach screen is a geometric calculation only. |
| **3. Thermal separation — hot knife and foam roller** | Use controlled hot-knife separation followed by the project’s foam-roller concept to separate the front glass and cell-bearing laminate. | Prepared module → expected glass and cell/EVA/backsheet laminate streams. | The hot-knife literature and prior conduction models are research inputs. The local thermal model does not include a foam roller or peel/fracture mechanics. The roller’s material and process parameters are unspecified; no integrated station or trial exists. |
| **4. Material liberation, separation and silver recovery** | Prepare or receive cell-bearing material, separate/concentrate silver-bearing fractions, and route them to a defined recovery/refining process. | Characterized Stage 3 feed → a measured silver-bearing concentrate, solution or solid plus accounted residues; final product depends on downstream refining. | Process route, actual feed specification, qualified facility, receiver requirements, and assay plan remain open. The Stage 4 reassessment does not support a conventional eddy-current separator as a default step. No AGASTYA silver has been removed, recovered, assayed, or purified. |

Sampling, representative assay, chain of custody, mass accounting, uncertainty analysis and safety review support all stages. They do not replace the Stage 4 silver-separation/recovery function.

## Stage boundaries and interfaces

### Stage 1 → Stage 2

EYE provides an inspection record and an advisory route. Human review and the applicable electrical-isolation procedure remain necessary. A vision result is not a safety-rated interlock and does not prove that a panel is electrically safe to handle.

### Stage 2 → Stage 3

The Stage 2 workcell is expected to remove accessible frame, junction-box and cable components while keeping the large module positively supported. The robot is a candidate for positioning and controlling tools; it is not assumed to lift the full panel. Stage 2 must record the module, tools, fixture, operator/supervisor, procedure, masses, streams, deviations and handoff to thermal treatment.

### Stage 3 → Stage 4

The working Stage 3 sequence is hot knife → foam roller → separate collection of glass and cell-bearing laminate. The foam roller’s exact role, contact conditions, wear and contamination behavior remain to be specified. The first output is not assumed to be EVA-free, cell-only, silver-liberated, or ready for flotation.

Published industrial process flow describes hot-knife glass separation followed by laminate shredding and sorting. This supports testing an adjacent, modular liberation step after Stage 3. Whether that module is assigned formally to Stage 3 or Stage 4 remains conditional on measured feed quality, dust/contamination control, handling, energy and whole-line economics. See [Stage 3 roller/liberation reassessment](Build%20Files%20and%20Steps/Stage%203/STAGE3_ROLLER_AND_LIBERATION_PLACEMENT_REASSESSMENT_2026-11-19.md).

### Stage 4 separation and recovery

The project’s original proposed chain — mechanical liberation → conventional eddy-current separation → froth flotation — is not retained as the default. The present evidence supports first characterizing all size fractions, keeping dry liberation/size classification as a low-complexity baseline, and evaluating silver-specific flotation only on compatible, prepared feed at a qualified facility. Conventional ECS is conditional on a measured coarse liberated conductive fraction for which a paired mass-balanced test demonstrates a benefit. See [Stage 4 architecture reassessment](Build%20Files%20and%20Steps/Stage%204/STAGE4_ARCHITECTURE_REASSESSMENT_2026-11-19.md).

A concentrate is not pure silver. Grade, recovery, mass yield, enrichment and purity must be calculated or assayed separately. Any final purity claim requires an independent method appropriate to the product specification.

## What has actually been accomplished

- **Implemented:** AGASTYA-EYE inspection/passport application and advisory image classifiers. The local RGB benchmark uses 104 held-out images, reports 84.6% accuracy and 83.5% macro-F1, and has mixed per-class performance; these are not field results.
- **Computationally modelled:** historical scenario datasets, accounting calculations, Stage 3 layered thermal models, Stage 4 literature-normalized balances, and a new Stage 2 planar perimeter reach screen. Their inputs and limits are recorded with each package.
- **Simulated:** numerical scenario sweeps and solver studies recorded in `Agastya Physics Simulation`; these are not physical replicates or validated machine performance.
- **Experimentally tested:** no AGASTYA Stage 2 disassembly, Stage 3 thermal/roller trial, Stage 4 liberation/separation trial, or assay is documented.
- **Validated against measured AGASTYA results:** none of the four process stages.

The Stage 2 model source and outputs are in [02_Engineering/Stage_2_Robotic_Disassembly](02_Engineering/Stage_2_Robotic_Disassembly/README.md). The historic 200,080 virtual scenario/time-history rows remain virtual and are not physical observations.

## Decision status

1. Stage 1 remains advisory until whole-module, site-specific data and human-verified routing performance are established.
2. Stage 2 remains a robotic-arm-centered design concept; a fixture, tool/task split, reachable panel envelope, measured process forces and safety architecture must precede actuator selection.
3. Stage 3 follows the current hot-knife and foam-roller direction, but only the prior hot-knife thermal model has been executed. Roller integration and all output performance remain unvalidated.
4. Place post-thermal liberation adjacent to Stage 3 as a modular, bypassable design option for the next comparison. Keep formal ownership and the accepted feed boundary conditional until matched trials are measured.
5. Do not adopt conventional ECS in Stage 4 unless actual feed characterization and paired trials show useful silver recovery or a complementary coarse-metal product.
6. Keep flotation and any chemical refining at a qualified partner facility unless site controls, costs, waste handling and receiver requirements are established.

## Historical records

Older thesis sections, logbooks, presentations, and models may describe manual Stage 2 preparation or other earlier designs. They remain historical evidence of the project’s development and are not silently rewritten. Current design guidance follows this file and the dated 19 November reassessments.
