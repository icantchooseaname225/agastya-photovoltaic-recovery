# Fusion arm concept script

`Stage2_Arm_Concept.py` creates an illustrative four-axis arm envelope as separate Fusion components. It is an assembled neutral-pose shape study; it does not include Fusion joints/motion, link material, internal structure, motors, bearings, cable routing, guarding, load cases or a tool. The design constants are at the top of the script. They must be replaced after actual panel/tool measurements and an engineering review.

## Run in Autodesk Fusion

1. Copy the complete `Stage2_Arm_Concept` folder into `%APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts\Stage2_Arm_Concept` or use Fusion's Scripts and Add-Ins dialog to link the local script.
2. In Fusion, open **Utilities → Scripts and Add-Ins** and run `Stage2_Arm_Concept`.
3. The script creates a new design and exports `AGASTYA_Stage2_Arm_Concept.f3d` and `.step` into the `exports` subfolder beside the script.
4. Review the component placement and export geometry in Fusion before using either file. The exports are still concept geometry, never fabrication drawings.

The Autodesk Fusion desktop app is installed on this workstation, but the app bridge did not expose a targetable Fusion window in the current session. The script has therefore **not** been run here and no F3D/STEP export is claimed. Autodesk documents the Python `run(context)` entry point, script installation and Scripts and Add-Ins runner, and the export manager methods in its [script guide](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-9701BBA7-EC0E-4016-A9C8-964AA4838954) and [ExportManager reference](https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/fusion_ExportManager.htm).
