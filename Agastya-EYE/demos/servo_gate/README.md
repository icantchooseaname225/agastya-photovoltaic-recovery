# AGASTYA-EYE servo gate interface demo

This small Arduino sketch demonstrates an operator command changing a servo position. The existing AGASTYA-EYE ESP32 application and inference firmware are separate and are not modified. The sketch does not connect to a classifier, camera, conveyor, panel, or industrial gate.

## Interface

- USB serial at 115200 baud accepts `APPROVE`, `REJECT`, or `HOLD`, each followed by a newline.
- Startup and a two-second command timeout set the output to `HOLD`.
- Demo positions are 90° (`HOLD`), 35° (`APPROVE`), and 145° (`REJECT`). These are illustrative angles; verify the servo, linkage, travel limits, and mechanical clearance before any powered tabletop demonstration.
- Unknown and overlength commands are reported and do not request a new position.

## Demonstration boundary

Use synthetic operator-entered commands and an unloaded, guarded tabletop fixture. A future integration needs a documented message schema, explicit confidence/uncertain state, human approval, communication-loss handling, position feedback, hardware limit review, and a separate safety assessment. The current sketch is a control-interface mock-up only.

## Validation record

The source was prepared for the Arduino `Servo` library interface. Arduino IDE/CLI and an attached board/servo were not available in this session, so compilation, timing, serial interoperability, motion, and electrical limits have not been tested. No latency or physical performance is claimed.
