# Stage 2 robotic-arm concept basis

**Prepared:** 20 November 2026<br>
**Status:** conceptual CAD envelope and bench-electronics study; not a selected robot, fabrication package or safety design.

## Purpose

I carried the earlier 2D perimeter screen into a first 3D envelope for discussion. The concept is a four-axis articulated arm used as a tool carrier while a separate fixture supports the PV module. The arm is not sized to lift a module. The CAD is a geometry and layout study; no mechanical loads, motor sizes, materials, wall thicknesses, fasteners, tolerances, controller or motion limits have been validated.

## Working geometry

| Item | Concept input | Basis / limitation |
|---|---:|---|
| Illustrative panel envelope | 2,278 × 1,134 mm | Same scenario as the existing 2D reach screen; not a measured AGASTYA module. |
| Base stand-off | 300 mm from near long edge | Same illustrative layout. |
| Upper-arm envelope | 1,100 mm | Placeholder link length. |
| Forearm envelope | 900 mm | Placeholder link length. |
| Nominal extended reach | 2,000 mm, excluding tool projection | Leaves 168.7 mm over the earlier 1,831.3 mm sampled far-corner radius. That is only geometric margin; not pose, collision, deflection or payload clearance. |
| Axes | base yaw, shoulder pitch, elbow pitch, wrist/tool pitch | A selected two-link IK solution is screened over the illustrative point set; no physical joint limits or motion plan are defined. |
| Vertical base datum | 730 mm to shoulder centre | 20 mm base plate + 650 mm pedestal + 60 mm turntable from the current Fusion script; layout placeholder. |
| Link cross-section envelopes | 120 × 100 mm and 100 × 80 mm | Solid visual envelopes only; no material or structural section chosen. |

The 2D screen found that a 2.0 m nominal radial reach covers its 71 illustrative perimeter samples. The later planar IK model adds a selected geometric solution, but still does not include robot-link collision geometry, physical tool orientation, joint stops, singularity handling, deflection, wrist dynamics, guarding or safety. The 2.0 m total in this concept is therefore a drawing input, not proof that a real arm can reach or safely perform the operations.

## What the files contain

- The AutoCAD DXF presents the same workcell in plan, a side-view arm envelope, and non-fabrication interface sketches.
- The Fusion Python script creates separate named components and extrusions, then exports an F3D Fusion archive and STEP file when run in Fusion's Scripts and Add-Ins tool. The script was prepared but could not be executed in Fusion during this session because the desktop application did not expose a targetable window.
- The electronics package separates a small, low-load classroom arm demonstration from the future process cell. The Arduino example is a manual-jog scaffold only. It is not connected to AGASTYA-EYE and is not a machine-safety controller.

## Inputs still needed before design freeze

1. Measure the accepted panel's length, width, thickness, mass, frame profile, corner fasteners, junction-box position and cable route.
2. Write the allowed feed-condition range and the facility-approved isolation/verification procedure. A vision result is not electrical isolation.
3. Measure each operation's force and moment on a representative, approved specimen; record the tool's mass and centre of gravity.
4. Choose the operations and tool approach directions, gripper/contact geometry, fixture restraints, collection bins and required Z clearance.
5. Compare one arm plus tool changing with a shorter-reach arm on a rail/indexer and with dedicated de-framing/J-box mechanisms.
6. Obtain manufacturer kinematics, payload, wrist-moment, speed, repeatability, duty-cycle and controller/safety data for actual candidates.
7. Have a qualified adult/mechanical reviewer assess the guarded cell and stop architecture before any powered movement.

## Engineering boundary

The hobby-servo prices in the accompanying cost screen are market comparables for small educational arms only. They do not support the 2 m reach concept. A 1 kg payload alone creates at least 19.1 N·m of gravity moment at a 1.95 m shoulder radius, before link mass, acceleration, friction or safety margin. The process-scale arm therefore remains unselected and uncosted.

**No hardware was fabricated or powered.** Do not manufacture from the DXF or export geometry. Replace assumptions with measurements, then perform a documented 3D kinematic, collision, structural, load and safety review.

## Follow-up package update — 20 November 2026

I added a parametric envelope source, nine-component OBJ/MTL and 556-triangle STL mesh, and executed the two-link IK screen against the existing 71 illustrative perimeter points. The simplified model reported 71/71 reachable and a maximum shoulder-to-target distance of 1,971.44 mm. Its exact forward/inverse closure check is mathematical; no joint limits, collisions, loads from the arm itself or physical motion are represented.

A Node.js NC-loop divider model and LTspice netlist were added for status-input discussion. At the Day 42 update, only the Node equation model had been executed; the LTspice file and Arduino sketch had not been run. Thirteen software checks across the arm, mesh, electronics and economics packages passed. The Fusion script remained unexecuted and there was no F3D/STEP export.

## Digital addendum — 21 November 2026

I extended the selected-branch output with a discrete candidate angle envelope for the 71 illustrative points: yaw 14.7559° to 165.2441°, shoulder pitch −13.4996° to 8.8899°, elbow pitch −134.7785° to −19.4873°, and wrist compensation 32.4608° to 148.2781°. These are model outputs, not required actuator travel. The model still omits collisions, tool approaches, clearances and alternate configurations.

I added a 625-case static gravity-moment sensitivity grid that includes analyst-selected upper-link, forearm, tool and payload masses. It places link centers of mass at link midpoints and tool/payload centers at the wrist on a horizontal, fully extended arm. The sensitivity inputs are not measured loads; resulting moments are not motor ratings. The component masses and actual centers of gravity are still missing.

I ran the status netlist in LTspice 26.1.1 batch mode. The modeled open contact measured 4.9999499 V at 2 ms and the closed contact 0.00024999 V at 7 ms. This confirms only the idealized circuit behavior; no controller board, E-stop, safety relay or arm was wired or tested. I added a quote-completeness framework for three process-cell layouts. It leaves CAPEX, cost per panel and payback unset because no comparable process-cell quotes or operating data were supplied. Eighteen Node checks passed. Fusion-native export remains open. The AutoCAD Core Console attempt timed out before creating a DWG, so in-app AutoCAD review is still outstanding.
