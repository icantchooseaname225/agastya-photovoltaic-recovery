# Robotic arm simulations

Inputs: inputs/perimeter_task_points.csv copied from the earlier 2D reach scenario.

Source: robotic_arm_kinematics.mjs. Run with Node.js 24 or later and built-in modules only:

    node "robotic arm/simulations/robotic_arm_kinematics.mjs"

Outputs: outputs/IK_TASK_POINT_RESULTS.csv, IK_SUMMARY.json, IK_WORKSPACE_SCREEN.svg, IK_MODEL_REPORT.md, PAYLOAD_ONLY_MOMENT_SWEEP.csv and STATIC_GRAVITY_MOMENT_SENSITIVITY.csv.

The kinematics model solves two-link planar inverse kinematics for each radialized perimeter point, calculates yaw from the base position and verifies each solution with forward kinematics. It reports selected-solution angle ranges over the 71 points, but assumes unlimited pitch travel and free base yaw. It is not collision-aware, dynamic, structural, actuator-sized or safety-validated. All 71 scenario points are geometrically reachable in this simplified model; that is not a process success rate.

The static gravity-moment CSV covers 625 analyst-selected link/tool/payload mass combinations for a horizontal fully extended arm. Link centers of mass are assumed at their midpoints; tool and payload centers are at the wrist. Grid values are sensitivity inputs only, not measurements or design recommendations. Replace them with measured masses and center-of-gravity locations before using moments in a design review.
