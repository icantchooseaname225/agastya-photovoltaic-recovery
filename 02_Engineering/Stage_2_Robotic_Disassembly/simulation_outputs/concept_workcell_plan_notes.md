# Stage 2 conceptual CAD plan

`concept_workcell_plan.dxf` is a generated two-dimensional AutoCAD R12 drawing in millimetre coordinates. It shows the same assumed 2,278 × 1,134 mm panel, 300 mm near-edge standoff, 71 sampled perimeter task points, a placeholder fixed arm-base footprint, support-rail placeholders, and 1.5 m/2.0 m nominal reach circles as the existing screen.

This is a plan-view layout artifact, not a robot assembly or fabrication drawing. It contains no link geometry, 3D heights, kinematics, tool orientation, joint limits, collision checks, load/force calculations, guarding, emergency-stop design, fastener sizing, or measured host dimensions. The reach circles only reproduce the scalar 2D reach assumption. Do not manufacture from it.

Regenerate with the available bundled Python runtime:

`python generate_workcell_plan_dxf.py`

The script reads `simulation_outputs/perimeter_task_points.csv` and overwrites only the generated DXF in that folder. A CAD editor is needed for visual review before the drawing is used in design work.
