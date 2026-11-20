# Arduino Uno or Nano servo gate

This sketch is a separate, optional tabletop gate for AGASTYA-EYE. The Python vision and inspection code does not call Arduino code. Only the local approval service can send a `RELEASE` command, and hardware activation is disabled unless `AGASTYA_HARDWARE_ENABLED=1` is set.

## Serial protocol

- Baud rate: 9600, 8-N-1.
- Python opens the configured COM port, waits for the board reset, then sends `PING <32 lowercase hex characters>`.
- The board replies `READY <same nonce>`.
- A release is `RELEASE <32 lowercase hex command ID> <duration_ms>`.
- The board replies `ACK RELEASE <command ID>` when it commands the servo to open, then `DONE <command ID>` after it commands the servo closed.
- Duplicate command IDs receive `ACK DUPLICATE` and never move the servo again. Invalid, busy, and overlength commands receive `ERR` and command the closed position.
- Accepted opening times are 1,000 to 30,000 ms. The Python default is 3,000 ms; configure it with `AGASTYA_SERVO_OPEN_MS`.

The Arduino has no position sensor. Its acknowledgements confirm only that the sketch issued servo commands; they do not prove that the linkage physically moved or closed.

## Wiring

For an unloaded, guarded tabletop fixture:

| SG90 lead | Connection |
|---|---|
| Signal (orange/yellow) | Arduino D9 |
| Ground (brown/black) | External regulated 5 V supply ground |
| Power (red) | External regulated 5 V supply positive |

Connect the external supply ground to an Arduino GND pin so the servo and board share a signal reference. Keep the Arduino connected to the computer by USB for serial communication. Do not power a loaded SG90 from the Uno/Nano 5 V pin; use a regulated 5 V supply sized for the servo's stall current. Check the servo travel and linkage by hand with power disconnected, guard pinch points, and keep the gate unloaded. Never connect this demo to an industrial sorter or safety interlock.

## Upload

Select **Arduino Uno** or the exact Nano processor variant in Arduino IDE, choose the detected serial port, and upload `servo_gate.ino`. The sketch uses the Arduino Servo library. After upload, close Serial Monitor before starting AGASTYA-EYE; two applications cannot own the COM port at once.
