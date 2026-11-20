# AutoCAD Stage 2 concept drawings

## Files

- `AGASTYA_STAGE2_ARM_CONCEPT.dxf` — ASCII AutoCAD R12 DXF in millimetres. It contains a plan view aligned to the 71-point reach screen, a side elevation, and three interface-envelope sketches.
- `AGASTYA_STAGE2_ELECTRICAL_ARCHITECTURE.dxf` — functional blocks for a future OEM robot/safety system and for a separate low-load classroom demonstrator.
- The `*_PREVIEW.svg` files are editable vector previews of the concept diagrams.
- `generate_stage2_arm_package.py` reproduces the DXF and SVG artifacts from the tracked reach-point CSV and the stated envelope assumptions.

## Limits

AutoCAD was installed but did not expose a targetable window through the current desktop app bridge, so the DXF was generated from the R12 writer and could not be visually opened/verified in AutoCAD during this session. The DXF is a concept layout, not a fabrication drawing, wiring release or safety schematic. Joint envelopes are simple circles/rectangles; no kinematic joints, tolerances, motor mounts, force calculations, structural checks, cable routing, interlocks or guard design are present.

In AutoCAD, open each DXF and check its extents, text height, units and layer visibility before annotating it. Do not manufacture or wire from these files. The interface hole patterns are placeholders that must be replaced by the selected robot/fixture manufacturer's data.
