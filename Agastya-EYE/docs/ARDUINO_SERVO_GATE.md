# Arduino servo gate integration

This integration is an optional, local tabletop extension to the existing AGASTYA-EYE application. It does not change the RGB classifier or its labels. The independent controller is in `hardware/`; the Uno/Nano sketch is `firmware/servo_gate/servo_gate.ino`.

## Release rules

Hardware is disabled by default. You can enable it for the current server session from the **Arduino Gate** panel in the site after entering the actual Uno/Nano COM port. The environment setting `AGASTYA_HARDWARE_ENABLED=1` remains an alternative. A release additionally requires all of the following:

- The app, inspection database, and primary RGB checkpoint are ready.
- The original image is present and belongs to a fresh, full-panel front-view RGB inspection (five-minute maximum age by default).
- The current class is `clean` at or above the existing 75% confidence and 12-point margin thresholds.
- The recorded panel is c-Si, has the `SECOND_LIFE_REVIEW` route, a documented electrical pass with voltage/current readings, and a final `REUSED` disposition with a reviewer note.
- The Arduino completed the serial readiness handshake.
- A person enters an operator ID, types the exact panel ID, and approves the one-time release.

Pending review, uncertain, rejected, incomplete, failed, stale, unsupported-modality, and already-used inspections are refused. Hardware status is separate from inspection success. A saved inspection never sends an Arduino command by itself. Every release attempt is tied to one inspection; a duplicate or uncertain command is never retried for that inspection.

## Install pySerial in the EYE environment

The launcher-selected environment is `%USERPROFILE%\Envs\agastya-python-3.12`. In PowerShell from `C:\Agastya\Agastya-EYE`:

```powershell
$EyePython = Join-Path $env:USERPROFILE 'Envs\agastya-python-3.12\Scripts\python.exe'
& $EyePython -m pip install pyserial
& $EyePython -c "import sys, serial; print('Python:', sys.executable); print('pySerial:', serial.__version__); print('Module:', serial.__file__)"
```

The project dependency is listed in `requirements.txt`. If you use a different existing interpreter, set `AGASTYA_EYE_PYTHON` to that interpreter before running the launcher; the launcher checks PyTorch, TorchVision, NumPy, Pillow, and pySerial in the same environment.

## Find and configure the COM port

Connect the Uno/Nano by USB. Close Arduino Serial Monitor and any other program using that port. List detected ports without assuming a port number:

```powershell
& $EyePython -m serial.tools.list_ports -v
```

Set the real port shown by that command. The following `COMx` is a placeholder; replace it with the detected value:

```powershell
$env:AGASTYA_EYE_PYTHON = $EyePython
$env:AGASTYA_HARDWARE_ENABLED = '1'
$env:AGASTYA_ARDUINO_PORT = 'COMx'
$env:AGASTYA_ARDUINO_BAUD = '9600'
$env:AGASTYA_SERVO_OPEN_MS = '3000'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Start-EYE.ps1
```

The serial defaults are 9600 baud, 250 ms per serial read, a three-second readiness handshake, and a 1.8-second board reset wait. The site activation applies only until the server restarts and does not automatically open a COM port; use **Connect Arduino** after activation. The servo-open interval accepts 1,000–30,000 ms; set `AGASTYA_SERVO_OPEN_MS` to change it. Approval age defaults to 300 seconds and can be set from 30 to 3,600 seconds with `AGASTYA_APPROVAL_MAX_AGE_SECONDS`. Invalid settings are reported as a hardware configuration error and do not stop vision inspections.

Check `http://127.0.0.1:<port>/api/v1/hardware/status` or the inspection panel in the app for Arduino state. If the board is connected after EYE starts, use **Retry Arduino connection**. The same PowerShell session must be used for environment variables and the launcher. To shut down a server started by the launcher:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Stop-EYE.ps1
```

If you start `app.py` directly, stop it with Ctrl+C in that PowerShell window.

## Firmware upload

Open `firmware/servo_gate/servo_gate.ino` in Arduino IDE. Select Arduino Uno or the exact Nano board/processor variant, select the COM port shown in **Tools → Port**, and click **Upload**. The sketch uses the built-in Servo library. Close Serial Monitor before running EYE because only one process can own the COM port at a time.

If Arduino CLI is installed and the AVR core/Servo library are not present, the additive setup and compile commands are:

```powershell
arduino-cli core install arduino:avr
arduino-cli lib install Servo
arduino-cli compile --fqbn arduino:avr:uno .\firmware\servo_gate
```

For a Nano, select the Nano board and processor option that matches the board. Upload is then `arduino-cli upload --fqbn arduino:avr:nano -p <detected-COM-port> .\firmware\servo_gate` with the real port substituted. Do not copy a placeholder COM number into the command.

## Wiring and power

Use an unloaded, guarded tabletop linkage for this demonstration.

| SG90 lead | Connection |
|---|---|
| Signal (orange/yellow) | Arduino D9 |
| Ground (brown/black) | External regulated 5 V supply ground |
| Power (red) | External regulated 5 V supply positive |

Connect the external supply ground to an Arduino GND pin so the signal has a common reference. Keep the Arduino on USB for serial communication. Do not power a loaded SG90 from the Uno/Nano 5 V pin; use a regulated 5 V supply sized for the servo stall current. Check servo travel and linkage by hand with power disconnected and guard pinch points. This is not a production sorter, process interlock, or safety controller.

The sketch starts at 0 degrees (closed), commands 90 degrees on a valid release, and commands closed after the selected interval. It sends `READY`, `ACK RELEASE`, and `DONE` messages. The Arduino has no position sensor; its acknowledgement confirms only the sketch's commands, not physical movement or barrier closure.

## Complete tabletop demonstration

1. Upload the firmware and wire the servo to D9 and its external regulated 5 V supply with common ground.
2. Find the actual COM port, close Serial Monitor, configure the environment above, and start EYE.
3. Confirm `/api/v1/health` reports the database and RGB model ready and `/api/v1/hardware/status` reports the Arduino ready.
4. Submit a front-view RGB panel image through the existing inspection workflow. Record c-Si, a qualified electrical pass with its method/instrument/operator, and the human-confirmed `clean` label. The RGB result must meet the existing confidence and margin thresholds.
5. Save the existing workflow's `REUSED` final disposition and `SECOND_LIFE_REVIEW` route with a reviewer note. Do not infer approval from the classifier alone.
6. Within five minutes, review the inspection, enter the approving operator ID, type the exact panel ID, and click **Authorize one-time gate release**.
7. Observe the SG90 move toward 90 degrees and return to the commanded 0-degree position after the configured interval. The app reports Arduino acknowledgements; physical movement still requires direct observation.
8. Submit an uncertain or pending-review record to confirm that the gate control remains unavailable. Disconnecting the Arduino must leave normal inspections working and must not activate the gate.

## Automated checks and troubleshooting

Run the full suite from the project root with the same interpreter selected by the launcher:

```powershell
& $EyePython -m unittest discover -s tests -v
```

Serial protocol and release tests use a mocked COM device and do not need an Arduino. A real board/servo is required only for the physical demonstration. If startup fails, read the `.out.log` and `.err.log` paths printed by `Start-EYE.ps1` under `%TEMP%`. For an Arduino error, confirm the COM port, close Serial Monitor, verify 9600 baud, inspect the external supply/common ground, and use **Retry Arduino connection**. A serial timeout after a release is recorded as uncertain: inspect the gate directly and do not retry that inspection.
