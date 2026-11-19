# Stage 2 automated robotic disassembly: feasibility review

**Reviewed:** 19 November 2026  
**Status:** design review and executed 2D geometric screen; no robot or disassembly trial is documented.

## Current design direction

The current project instruction replaces the previous manual-preparation baseline with automated mechanical disassembly centred on a robotic arm. The arm is a proposed tool-manipulation system, not a panel-lifting device. An adjustable, positively supported fixture must carry the module and react cutting, pulling, and clamping forces.

The mechanical work is not one uniform task. At minimum, the design must handle:

1. **Frame release:** locate corners and joints, restrain the module, release the four extrusion rails without loading the glass unpredictably, and collect aluminium separately.
2. **Junction-box and cable removal:** identify the box location and cable route, restrain the module, remove the box and cables, and keep copper and polymer streams identifiable.
3. **Module presentation:** register different panel dimensions and junction-box positions while keeping the workpiece supported. A fixture, panel indexer, linear rail, or dedicated feed mechanism may be needed in addition to the arm.

The exact order of operations must follow the qualified facility procedure and accepted panel condition. Stage 1 image classification is not electrical isolation, a live-voltage check, or a safety interlock.

## External process evidence

Published and industrial process descriptions support automation, but they do not show that one general-purpose arm is the best machine for every task:

- The IEA PVPS 2025 country-status report describes an operating Japanese PV-recycling line with automated junction-box removal and de-framing, followed by hot-knife glass separation and then laminate shredding/sorting. This supports an integrated and sequenced automated workcell. It does not specify a single robot arm performing all operations. [IEA PVPS T12-31:2025](https://doi.org/10.69766/XLFG7020).
- Latunussa et al. describe a process inventory in which a Cartesian robot supplies panels, the aluminium frame edges are cut and the remaining frame is torn away, and a mechanical arm detaches cables. The reported arrangement uses task-specific equipment and separates material handling from tool operations. It is a process design/LCA source, not an AGASTYA performance test. [Latunussa et al. (2016)](https://doi.org/10.1016/j.solmat.2016.03.020).

The evidence therefore supports automated feeding and task-specific frame/cable tooling. It does not establish arm payload, reach, force, cycle time, repeatability, capital cost, or ROI for AGASTYA.

## Executed model: top-view perimeter reach screen

**Question:** From one stationary base on the midpoint of a long panel side, how much nominal radial reach is required to include sampled frame-perimeter task points?

**Model:** Euclidean distance from a fixed arm-base projection to perimeter samples. The executed script samples the four edges at no more than 100 mm spacing and compares each distance to four scalar reach values.

**Illustrative inputs:** 2,278 × 1,134 mm panel; base 300 mm beyond the near long edge; panel centred at the origin; 71 perimeter task points. These dimensions are a model scenario, not a measured AGASTYA panel. Execution used Python 3.14.10 and the standard library.

| Nominal radial reach | Sampled points within radius |
|---:|---:|
| 1.2 m | 25/71 (35.21%) |
| 1.5 m | 47/71 (66.20%) |
| 1.8 m | 69/71 (97.18%) |
| 2.0 m | 71/71 (100.00%) |

Maximum sampled radius was 1,831.3 mm. These percentages count geometric points only; they are not robot success rates. Even the 2.0 m result is a necessary-distance screen, not proof that a real robot can adopt all required tool poses.

Reproduce the run with:

```powershell
python -B .\02_Engineering\Stage_2_Robotic_Disassembly\robot_workcell_reach_model.py
```

The script, CSV task-point table, JSON run record, SVG diagram, and generated model report are in this folder and its `simulation_outputs` subfolder.

## Engineering assessment

A single fixed-base arm with about 1.5 m nominal reach is a poor assumption for complete perimeter access in the illustrative arrangement. Two ways to reduce arm reach are a panel indexer/rotator and a linear robot rail. Both add machinery and another interface to validate. A nominal 2.0 m arm covers the sampled perimeter in this 2D scenario, but a long-reach arm may bring higher payload/moment, deflection, stiffness, guarding, and cost requirements. No arm model is selected.

One arm can potentially perform both frame and junction-box work if it can reach the required sides and use suitable task-specific tools. Frame release and cable/box removal are different contact tasks; a quick tool changer, separate tools, and fixture repositioning add cycle time and failure points. For repeated production, dedicated frame-release and junction-box mechanisms may be simpler. For AGASTYA research, one configurable arm remains worth studying only if its flexibility justifies the extra reach and tooling.

Keep the complete panel supported in a fixture. Do not size the robot as if it should lift a whole module. Record actual tool mass, centre of gravity, applied force, moment, speed, and inertia before comparing a robot manufacturer's payload and wrist-moment limits. Force-controlled or compliant tooling may help with variable adhesive and frame fit, but no force requirement can be assigned until representative material is measured.

## Recommended concept to carry forward

- Make the **fixture and process registration** the primary workcell datum; add an indexer or rail only if a measured panel envelope requires it.
- Use the arm as a **tool carrier for flexible operations**, not as a substitute for positive module support or simple high-force dedicated mechanisms.
- Compare one-arm plus tool changer against a simple dedicated de-framer/J-box fixture on reach, tool changes, measured release force, handling, reliability, and fully defined cycle time.
- Begin any prototype design with a cold, unpowered fixture and representative module dimensions. No active disassembly, tool purchase, or actuator sizing is justified by the current evidence.
- Keep EYE isolated from robot motion. Its inspection and passport functions are not safety-rated machine control.

## Missing inputs before a 3D/CAD or actuator model

- Measured module length, width, thickness, mass, frame cross-section, corner joint, and junction-box layout for the accepted feed.
- Allowed feed variation, damage/warp limits, and electrical-isolation procedure.
- Required tool approach directions, clearances, restraint locations, and material-stream collection geometry.
- Tool mass/centre of gravity and measured force/moment profiles for frame and box removal.
- Candidate arm/rail/fixture manufacturer data, joint limits, and safety-system requirements.
- Throughput requirement, target duty cycle, acceptable changeover time, and verified India-market quotations.

Until those inputs exist, the reach screen cannot support an equipment selection or cost estimate. A later 3D model should test inverse kinematics, joint limits, tool orientation, link/panel collisions, fixture clearance, wrist moments, and path-cycle estimates, then be compared with supervised measurements.

## References

- Agraffeil, C. et al. (2025), *Status of PV Module Recycling in IEA PVPS Task 12 Countries*, IEA PVPS T12-31:2025. [DOI](https://doi.org/10.69766/XLFG7020).
- Latunussa, C.E.L. et al. (2016), “Life Cycle Assessment of an innovative recycling process for crystalline silicon photovoltaic panels,” *Solar Energy Materials and Solar Cells*, 156, 101–111. [DOI](https://doi.org/10.1016/j.solmat.2016.03.020).

