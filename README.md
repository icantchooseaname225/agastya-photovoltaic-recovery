# AGASTYA

AGASTYA is a student-led engineering and research project for automated end-of-life solar-panel processing and silver recovery. The current four-stage direction is:

1. **AGASTYA-EYE:** vision-based triage and traceability.
2. **Robotic mechanical disassembly:** a robotic-arm workcell with fixture and task-specific tooling.
3. **Thermal separation:** hot knife followed by the foam-roller concept.
4. **Material liberation, separation, and silver recovery:** route and product form still under investigation.

The authoritative status and evidence limits are in [AGASTYA_ARCHITECTURE.md](AGASTYA_ARCHITECTURE.md). See the [Stage 2 robot feasibility review](02_Engineering/Stage_2_Robotic_Disassembly/STAGE2_ROBOTIC_DISASSEMBLY_FEASIBILITY_2026-11-19.md), [Stage 3 roller/liberation review](Build%20Files%20and%20Steps/Stage%203/STAGE3_ROLLER_AND_LIBERATION_PLACEMENT_REASSESSMENT_2026-11-19.md), and [Stage 4 route reassessment](Build%20Files%20and%20Steps/Stage%204/STAGE4_ARCHITECTURE_REASSESSMENT_2026-11-19.md).

The project includes an implemented vision/traceability application, a preliminary 2D robotic reach screen and conceptual DXF plan, a separate Arduino servo-interface demo sketch, an idealized EVA heat-diffusion simulation, and a literature-based Stage 4 mass-balance sensitivity model. **No AGASTYA robot, thermal/foam-roller station, silver-separation process, assay, or recovered silver is documented as physically tested.** Literature and simulations are not AGASTYA process performance.

Open [START_HERE.md](START_HERE.md) for the project map, [PROJECT_STATUS.md](PROJECT_STATUS.md) for current gaps, and [AGASTYA_PROJECT_INDEX.md](AGASTYA_PROJECT_INDEX.md) for research and records. The existing October presentations and historical documents reflect earlier decisions and must be reviewed before reuse.

The Stage 2 package now includes a generated nine-component arm-envelope mesh, an editable parametric source, an executed 71-point idealized inverse-kinematics screen, a bench NC-loop model, and a transparent education-scale cost calculator. See [robotic arm](robotic%20arm/README.md) and [agastya economics](agastya%20economics/README.md). The Fusion API script remains unexecuted and the package has no F3D/STEP export; all geometry and simulations remain concept-stage and physically unvalidated.
