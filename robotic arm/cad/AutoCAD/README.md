# AutoCAD Stage 2 concept drawings

## Files

- `AGASTYA_STAGE2_ARM_CONCEPT.dxf` — ASCII AutoCAD R12 DXF in millimetres. It contains a plan view aligned to the 71-point reach screen, a side elevation, and three interface-envelope sketches.
- `AGASTYA_STAGE2_ELECTRICAL_ARCHITECTURE.dxf` — functional blocks for a future OEM robot/safety system and for a separate low-load classroom demonstrator.
- The `*_PREVIEW.svg` files are editable vector previews of the concept diagrams.
- `generate_stage2_arm_package.py` reproduces the DXF and SVG artifacts from the tracked reach-point CSV and the stated envelope assumptions.

## Limits

AutoCAD was installed but did not expose a targetable window through the desktop app bridge. On 21 November 2026 I also tried the AutoCAD 2027 Core Console to import and audit the arm DXF; it did not complete within 25 seconds and its startup log reported a missing `ErrorReports` log path. No DWG was generated and the drawing was not visually reviewed in AutoCAD. See Autodesk's [Core Console command reference](https://help.autodesk.com/cloudhelp/2026/ENU/AutoCAD-Core-Console/files/AUTOCAD_CORE_CONSOLE.html). The DXF is a concept layout, not a fabrication drawing, wiring release or safety schematic. Joint envelopes are simple circles/rectangles; no kinematic joints, tolerances, motor mounts, force calculations, structural checks, cable routing, interlocks or guard design are present.

In AutoCAD, open each DXF and check its extents, text height, units and layer visibility before annotating it. Do not manufacture or wire from these files. The interface hole patterns are placeholders that must be replaced by the selected robot/fixture manufacturer's data.
