# AGASTYA robotic arm concept package

**Updated:** 21 November 2026
**Status:** concept geometry, executed kinematic and static-load sensitivity screens, LTspice transient status model and quote-input framework; no robot selected or tested.

This folder packages the current Stage 2 robotic-disassembly work in one place. The panel dimensions, base location, arm link lengths and loads are illustrative inputs; replace them with measured process data before design decisions.

## CAD files

- cad/AutoCAD contains the plan/side/interface concept drawings in DXF with SVG previews.
- cad/Fusion/Stage2_Arm_Concept.py is a Fusion API script that creates named component envelopes and requests F3D/STEP exports.
- cad/Fusion/arm_envelope_model.scad is an editable parametric visualization source.
- cad/Fusion/exports/agastya_arm_envelope.obj and .mtl provide a nine-component neutral-pose mesh.
- cad/Fusion/exports/agastya_arm_envelope.stl contains 556 triangles for mesh import.

The STL and OBJ geometry was generated from the script in this package. It shows a floor plate, pedestal, yaw/shoulder/elbow/wrist housings, two link envelopes and an unselected tool-interface placeholder. It is not a structural design or a fabrication drawing. The Day 42 Fusion UI attempt did not reach a stable, inspectable work surface; the native Fusion script was not run and no F3D/STEP export is claimed. On Day 43, AutoCAD Core Console did not complete its DXF import/audit attempt, and no DWG was generated. The DXFs were not opened for in-application visual inspection.

## Kinematics and load screen

Run the model with:

    node "robotic arm/simulations/robotic_arm_kinematics.mjs"

It reads the illustrative 71-point perimeter CSV and writes the inverse-kinematics table, summary, SVG, payload-only sweep and static link/tool/payload sensitivity grid to simulations/outputs. The executed result found 71/71 points within the ideal two-link annulus for 1,100 mm plus 900 mm links, a 730 mm shoulder height and free base yaw. Maximum shoulder-to-target distance was 1,971.44 mm; maximum forward/inverse closure error was about 2.54e-13 mm. These are mathematical checks against the same geometric scenario, not independent physical validation.

The model reports the selected IK branch's discrete angle envelope over the 71 sample points. This is not a joint travel specification and does not add collision, limits or alternative approach checks. A second output evaluates 625 analyst-selected combinations of link, tool and payload masses in a horizontal, fully extended pose. Link centers of mass are at their midpoints, and tool/payload centers are at the wrist. Grid values are sensitivity points, not measured masses or design demands; moments do not include acceleration, friction, compliance, duty, safety factors or motor performance. Neither screen selects actuators.

## Electronics model

electronics/ contains the existing low-load Arduino manual-jog scaffold, pin map and design basis. spice/ includes an LTspice NC status-loop netlist and a Node.js resistor-equation model. LTspice 26.1.1 was run in batch mode: MCU_STATUS measured 4.9999499 V at 2 ms in the modeled open state and 0.00024999 V at 7 ms in the modeled closed state. Measurements are in electronics/spice/outputs/LTSPICE_TRANSIENT_RESULTS.json. The Arduino sketch was not compiled, and no board or servo was connected.

The NC contact is status-only. A separately rated hardware safety device must interrupt the servo rail. A single loop does not detect all wiring faults and the software is not a safety function.

## Tests and evidence

From the repository root:

    node --test "robotic arm/tests/*.test.mjs" "agastya economics/tests/*.test.mjs"

The 18 automated Node.js checks passed on Node.js 24.22.3. They test inverse/forward closure, annulus boundaries, payload and link-mass arithmetic, quote completeness behavior, catalogue arithmetic, contact voltage states and the generated mesh files. LTspice also completed the documented transient run. None of these checks validates a physical arm, control board, machine safety or PV-panel process.

**Evidence labels:** the CAD envelope is proposed geometry; the analytical results are simulated/calculated from stated assumptions; no Stage 2 hardware result is experimentally tested or validated.
