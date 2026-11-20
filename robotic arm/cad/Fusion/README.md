# Fusion and 3D concept files

Stage2_Arm_Concept.py is a Fusion API source script for a named, static envelope assembly and F3D/STEP export. Its dimensions are illustrative. It contains no joints, motion limits, motors, bearings, cable management, load cases or tool design.

arm_envelope_model.scad is a parameterized visualization source. generate_arm_obj.mjs creates the nine-part OBJ/MTL mesh and ASCII STL file in exports/. The STL uses model dimensions in millimetres but STL itself has no unit metadata.

Fusion is installed and its window was present in the app inventory, but UI automation could not establish a stable inspectable work surface in this session. The script was not run in Fusion; no F3D or STEP file is present or claimed. AutoCAD drawings are separate DXF files in the sibling AutoCAD folder.

Open these mesh/source files for visual review only. Do not manufacture from them.
