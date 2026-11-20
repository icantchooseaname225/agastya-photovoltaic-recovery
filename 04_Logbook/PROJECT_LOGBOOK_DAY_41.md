# AGASTYA research logbook — Day 41

**Date:** 20 November 2026<br>
**Status:** AI-assisted digital continuation in first person; draft for owner review. No CAD application review, physical build, powered arm test, panel experiment or purchase was completed.

## Objective

Continue the Stage 2 work by preparing a robotic-arm concept package for Fusion and AutoCAD, laying out a separate electronics concept, checking educational-scale costs, and recording the remaining engineering inputs.

## Work undertaken

I carried the earlier 2D reach screen into a first arm layout. I kept the same illustrative 2,278 × 1,134 mm panel and 300 mm stand-off so the drawing stays connected to the 71-point screen. I used a 1,100 mm upper-arm and 900 mm forearm envelope for a four-axis concept. The arm is only a tool carrier; the fixture still supports the panel. These dimensions are placeholders because I do not yet have a measured panel or tool loads.

I created an AutoCAD R12 DXF concept sheet with the plan view, side elevation, task points and simple interface sketches. I also prepared a functional electronics block diagram in DXF and SVG. The DXF files were generated from the project files, but I did not open them in AutoCAD to inspect the drawing display.

I wrote a Fusion Python script that is intended to create separate named geometry components and export an F3D archive and STEP file when run inside Fusion. Fusion and AutoCAD are installed, but neither application exposed a targetable window through the computer-use app bridge. I could not run the script or inspect a native Fusion design, so I am not claiming that an F3D or STEP file has been generated. The script produces static envelopes only; it does not make a moving arm assembly or select motors.

For the electronics, I separated a future process cell from a small classroom demonstration. The process-cell diagram leaves the robot controller and safety devices unselected and keeps EYE out of the motion-safety path. I added a provisional Arduino pin map and manual-jog sketch for an unloaded bench mechanism. The sketch has not been compiled or connected to a board; its software limits are placeholders and its E-stop input is only a status input. A real E-stop would need to interrupt the motor power through hardware selected for the final actuators.

I checked current educational-arm and component listings in India and recorded them in the cost screen. A listed ACEBOTT learning arm was ₹5,019, and a Robokits 6-DOF kit with controller/software was listed at ₹13,600. The Robokits product page lists 350 mm maximum reach and 100 g maximum payload, so it is only a classroom-scale reference. A separate example using four listed servos, an official Arduino Mega and an optional PWM board totals ₹14,066–₹14,315 for those listed items only. Power, a hardware E-stop, guards, frame fabrication, shipping and other integration are not included. The ACEBOTT listing also has inconsistent controller details, so I would confirm the kit contents before buying. None of these educational products is a process-scale arm quote.

The 2 m arm envelope also shows why I cannot assign hobby servos to the real workcell: a 1 kg payload at 2 m creates about 19.6 N·m of shoulder gravity moment before link weight, tool mass, acceleration or design margin. I recorded this as a simple lower-bound calculation, not an actuator selection. The whole-cell cost and any payback remain unknown until the panel, tools, forces, throughput, safety system and vendor quotes are defined.

I completed the project-file review for this update and refreshed the public-sync manifest to include the Day 41 CAD, electronics, economic-screen and logbook files. I screened the publish candidate text/code for email, account-path, token, bearer-token and private-key patterns; no matches were found. I then pushed the reviewed changes to the public repository using a normal push and checked that remote `main` matched my local `main`. This is a file synchronization step, not evidence that the arm design or hardware has been validated. Day 40 already records the NML response and my visit inquiry; I have no confirmed visit, collaboration or new institute result to add here.

## What I found

1. The new AutoCAD drawings and Fusion script are concept resources, not fabrication or wiring-release drawings.
2. The current 2 m reach envelope does not prove usable robot poses, clearances, payload or safe operation.
3. The low-cost kit prices are only for educational-scale comparisons. There is still no defensible cost estimate for a PV-processing workcell.
4. No arm, actuator, power supply, safety relay, robot controller or fabrication method has been selected. I made no purchase and did not contact suppliers.

## Next steps

1. Open the DXFs in AutoCAD and visually check units, extents, labels and layers.
2. Run the Fusion script from Scripts and Add-Ins, inspect the resulting components, and create the F3D/STEP exports only after reviewing the model.
3. Replace the assumed module and arm dimensions after measuring the accepted module and the actual tools; measure contact forces under qualified supervision before sizing the arm.
4. Compare a robot with tool changing against a shorter-reach rail/indexer and dedicated de-framing/J-box fixtures using complete written quotes.
5. Have a qualified reviewer check guarding, gravity-axis support and E-stop behavior before any powered bench motion.
6. Continue the NML visit follow-up only when the institute provides its contact and visitor procedure; no visit or collaboration is confirmed.
7. Recheck catalogue listings before any purchase decision; today's prices are only a time-stamped comparison and are not a process-arm quotation.

**Full/short pair:** [Day 41 short entry](Short%20Versions/DAY_41_SHORT_ENTRY.md).
