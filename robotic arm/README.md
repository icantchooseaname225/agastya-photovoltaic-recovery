# AGASTYA robotic arm concept package

**Updated:** 20 November 2026
**Status:** concept geometry, executed kinematic screen and classroom status-input model; no robot selected or tested.

This folder packages the current Stage 2 robotic-disassembly work in one place. The panel dimensions, base location, arm link lengths and loads are illustrative inputs; replace them with measured process data before design decisions.

## CAD files

- cad/AutoCAD contains the plan/side/interface concept drawings in DXF with SVG previews.
- cad/Fusion/Stage2_Arm_Concept.py is a Fusion API script that creates named component envelopes and requests F3D/STEP exports.
- cad/Fusion/arm_envelope_model.scad is an editable parametric visualization source.
- cad/Fusion/exports/agastya_arm_envelope.obj and .mtl provide a nine-component neutral-pose mesh.
- cad/Fusion/exports/agastya_arm_envelope.stl contains 556 triangles for mesh import.

The STL and OBJ geometry was generated from the script in this package. It shows a floor plate, pedestal, yaw/shoulder/elbow/wrist housings, two link envelopes and an unselected tool-interface placeholder. It is not a structural design or a fabrication drawing. Fusion did not reach a stable, inspectable work surface during this session; the native Fusion script was not run and no F3D/STEP export is claimed. The AutoCAD DXFs were not opened for in-application visual inspection during this update.

## Kinematics and load screen

Run the model with:

    node "robotic arm/simulations/robotic_arm_kinematics.mjs"

It reads the illustrative 71-point perimeter CSV and writes the inverse-kinematics table, summary, SVG and payload-only moment sweep to simulations/outputs. The executed result found 71/71 points within the ideal two-link annulus for 1,100 mm plus 900 mm links, a 730 mm shoulder height and free base yaw. Maximum shoulder-to-target distance was 1,971.44 mm; maximum forward/inverse closure error was about 2.54e-13 mm. These are mathematical checks against the same geometric scenario, not independent physical validation.

The load sweep uses tau = mass × 9.80665 × radius. It excludes link/tool mass, acceleration, friction, duty, stiffness, safety factors and motor performance. It cannot select actuators.

## Electronics model

electronics/ contains the existing low-load Arduino manual-jog scaffold, pin map and design basis. spice/ includes an LTspice NC status-loop netlist and a Node.js resistor-equation model. The executed model gives about 0.00025 V for a closed 0.5-ohm contact with a 10-kilohm pull-up and 5.0 V for an open contact. The netlist was not run in LTspice, the Arduino sketch was not compiled, and no board or servo was connected.

The NC contact is status-only. A separately rated hardware safety device must interrupt the servo rail. A single loop does not detect all wiring faults and the software is not a safety function.

## Tests and evidence

From the repository root:

    node --test "robotic arm/tests/*.test.mjs" "agastya economics/tests/*.test.mjs"

The 13 automated Node.js checks passed on Node.js 24.22.3. They test inverse/forward closure, annulus boundaries, payload arithmetic, catalogue arithmetic, missing-input behavior, contact voltage states and the generated mesh files. They do not validate a physical arm, control board, LTspice model, machine safety or PV-panel process.

**Evidence labels:** the CAD envelope is proposed geometry; the analytical results are simulated/calculated from stated assumptions; no Stage 2 hardware result is experimentally tested or validated.
