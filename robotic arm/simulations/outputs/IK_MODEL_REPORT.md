# Stage 2 inverse-kinematics and payload screen

**Run:** S2-3D-PLANAR-IK-2026-11-21-01<br>
**Evidence:** simulated from concept dimensions; not experimentally validated.

## Result

- Reachable perimeter points: **71/71 (100%)**.
- Maximum shoulder-to-target distance: **1971.44 mm**.
- Maximum FK closure error: **2.5421e-13 mm**.

Two-link IK uses cos(q2)=(d^2-L1^2-L2^2)/(2 L1 L2); both elbow branches are solved and the branch with minimum absolute pitch sum is retained. The wrist pitch cancels shoulder-plus-elbow pitch for a nominal horizontal tool.

## Candidate angle envelope

- yaw_deg: **14.7559° to 165.2441°** (150.4882° span over these 71 selected solutions). This is a discrete geometry screen, not a required joint travel specification.
- shoulder_pitch_deg: **-13.4996° to 8.8899°** (22.3895° span over these 71 selected solutions). This is a discrete geometry screen, not a required joint travel specification.
- elbow_pitch_deg: **-134.7785° to -19.4873°** (115.2912° span over these 71 selected solutions). This is a discrete geometry screen, not a required joint travel specification.
- wrist_compensation_deg: **32.4608° to 148.2781°** (115.8173° span over these 71 selected solutions). This is a discrete geometry screen, not a required joint travel specification.

## Static gravity-moment sensitivity

The generated `STATIC_GRAVITY_MOMENT_SENSITIVITY.csv` evaluates 625 combinations of analyst-selected link, tool and payload masses. The link centers of mass are assumed at their midpoints; the assembly is horizontal and fully extended; tool and payload centers are placed at the wrist. The grid demonstrates how omitted masses affect gravity moment. Its mass values are not measurements or selected design values, and the results are not actuator ratings.

![Workspace screen](IK_WORKSPACE_SCREEN.svg)

## Limits

The points and base location are illustrative. Unlimited joint travel, free yaw and a rigid ideal chain are assumed. There are no collision, link mass, tool, actuator, speed, structural, force, duty-cycle or safety models. Replace the panel and tool assumptions and obtain manufacturer data before considering a guarded physical build.
