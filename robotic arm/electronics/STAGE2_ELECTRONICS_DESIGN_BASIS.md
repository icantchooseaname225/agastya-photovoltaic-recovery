# Stage 2 arm electronics and control boundary

**Prepared:** 20 November 2026<br>
**Status:** conceptual architecture and low-load demonstrator scaffold; not a safety-rated design or wiring-release drawing.

## Two separate systems

### Future process cell

The production arm must use a selected robot manufacturer's controller, drives, safety I/O and documented Safe Torque Off (STO) or equivalent stop architecture. A qualified safety review must determine the guard interlocks, dual-channel emergency-stop circuit, reset behavior, power isolation and expected gravity-axis behavior. No robot, drive, safety relay/PLC, contactor, power supply or safety level has been selected. AGASTYA-EYE remains an inspection and record system; its classification, network or UI does not authorize motion and does not replace a safety controller.

The production block diagram in [the AutoCAD electrical architecture](../cad/AutoCAD/AGASTYA_STAGE2_ELECTRICAL_ARCHITECTURE.dxf) intentionally uses functional blocks only. Do not wire mains voltage or purchase safety devices from that sketch.

### Low-load classroom demonstrator

The Arduino example is for a small, unloaded tabletop mechanism and manual jog learning only. It is a separate research activity and cannot be connected to a full-size arm, frame tool, junction-box tool, hot knife or AGASTYA-EYE motion command. The pin assignment is provisional and the software ranges must be reviewed against the actual mechanism.

- Four RC-servo signals may be driven from an Arduino Mega for a small demonstration. Servos require their own supply sized from the selected servo's voltage and stall-current data; never power the servo rail from the board's 5 V pin.
- A PCA9685 is optional PWM signal hardware. It does not provide servo motor power and does not make a safety circuit.
- The NC emergency-stop contact provides a status input to the microcontroller and must also interrupt the separate servo-power path through a correctly rated device. The sketch also expects an isolated auxiliary status contact from that power-interrupting device. The Arduino input alone cannot stop power.
- NC travel-limit loops are software monitoring only in this scaffold. Include physical stops, an unloaded catch/support and a supervisor-reviewed guard. A broken wire reads as open and faults the example software.
- On power removal, an arm can fall. Support gravity axes before energizing; do not perform a powered movement until the power-loss behavior is understood.

## Included files

- [Bench firmware scaffold](STAGE2_ARM_BENCH_DEMO.ino)
- [Provisional Mega pin map](STAGE2_BENCH_ARM_PIN_MAP.csv)
- [AutoCAD functional block/wiring architecture](../cad/AutoCAD/AGASTYA_STAGE2_ELECTRICAL_ARCHITECTURE.dxf)
- [Electrical SVG preview](../cad/AutoCAD/AGASTYA_STAGE2_ELECTRICAL_ARCHITECTURE_PREVIEW.svg)

## Serial interface in the scaffold

The sketch starts with servo outputs detached. It accepts `STATUS`, `HELP`, `RESET`, `ENABLE`, `DISABLE`, `CENTER`, and `J <axis 1..4> <angle>`. It slews the commanded angle in small software increments but has no feedback that the physical joint followed the command. `ENABLE` can cause motion to the stored target. Use only after the arm is mechanically supported, unloaded, guarded and centered under supervision. The input pin is a status input; the external power-interrupting E-stop is still required.

The sketch and pin map have not been run on a board. Servo type, supply rating, connector, relay/contactor, fusing, limits, actual angles and enclosure remain unselected.
