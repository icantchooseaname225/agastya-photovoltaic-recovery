# AGASTYA research logbook — Day 39

**Date:** 19–20 November 2026<br>
**Status:** AI-assisted digital continuation; pending owner review. No physical hardware experiment or servo movement was conducted.

## Objective

Record the work across this chat: resolve the reported inability to reach the local AGASTYA-EYE site, preserve and repair the existing inspection system, confirm the Python serial dependency, and prepare an optional site-controlled Arduino servo-gate demonstration with code, wiring guidance and auditable release conditions.

## Work undertaken

The user initially reported that `http://127.0.0.1:8765` could not be reached. The EYE launcher and readiness path were reviewed and improved; the local service was subsequently started, `/api/v1/health` reported ready, and the site opened at that address. The evidence supports a working local service at the end of the session; it does not establish a separate network fault diagnosis.

The project work was done in `C:\Agastya\Agastya-EYE` on local branch `codex/agastya-eye-serial-integration-20261119`, initially at `3ccd78a`. The correct launcher environment was the existing `%USERPROFILE%\Envs\agastya-python-3.12` environment (Python 3.12.14). pySerial 3.5 was installed into that existing environment and recorded as a project dependency; no new Python environment was created.

The audit preserved model checkpoints, model architectures, class labels and the primary database schema. A read-only baseline copy of the SQLite database contained six inspections and six panels; its SHA-256 was `13C1E0214C9EE535E2899207C92A98684D675727FB702A6DC711FD7962E746B0`. During the audit a seventh append-only inspection, `PV-000007`, dated `2026-11-19T18:17:11Z` and marked `PENDING_REVIEW`, was observed. Its origin was unknown, so it was left untouched. Later database quick-check and foreign-key checks passed with seven inspection and panel records.

Live RGB inference and evaluation had used different preprocessing paths: evaluation used TorchVision resize-to-256, center-crop-to-224, tensor conversion and ImageNet normalization, while live inference used a custom PIL resize/crop. A shared helper in `inference/preprocessing.py` now aligns those paths. On 104 existing test images, inference reproduced the stored sidecar metrics: accuracy `0.8461538461` (84.6%) and macro-F1 `0.8353395073` (83.5%). This is reproducibility against the existing test result, not a new field validation.

Repeated status and dataset requests had recursively scanned large raw and processed image trees. A 30-second cache was added. Sample local response times changed from about 778 ms for status and 609 ms for datasets to roughly 24 ms and 9 ms when warm; these are observations from one machine, not a controlled benchmark. Liveness remains separate from readiness: `/api/v1/health` reports database and RGB readiness, including warming/degraded states. Startup checks the selected environment and dependencies, waits for readiness, and reports launcher-managed process state; `Stop-EYE.ps1` requests graceful shutdown. Browser requests now have a 60-second timeout and actionable errors.

An optional Arduino Gate panel and independent controller were added. Site enable/disable is scoped to the current server session; enabling does not itself open a COM port, and ordinary inspection saving does not command the servo. A separate append-only hardware event ledger records gate events. Release requires system readiness, a fresh intact full-panel front-view RGB inspection, eligible c-Si panel and review metadata, documented electrical pass, human-confirmed clean/reuse disposition, serial readiness, operator ID and exact panel ID, followed by one-time approval. Pending, uncertain, rejected, stale, incomplete, unsupported or already-used cases are refused; uncertain commands are not retried for that inspection.

The site’s enable/disable behavior was checked using placeholder `COM99`, then reset to disabled with the port cleared. No serial port was opened. Port enumeration found COM3, COM4, COM6 and COM7, all identified as Standard Serial over Bluetooth; no Uno/Nano was detected.

The sketch is `firmware/servo_gate/servo_gate.ino`. It starts at 0 degrees, commands 90 degrees for a valid release and returns to 0 after the configured interval (3 seconds by default). It uses 9600 baud and READY/PING, ACK RELEASE and DONE protocol messages, rejects duplicate releases, and has no physical position sensor. Wiring guidance specifies SG90 signal to D9, red to external regulated 5 V positive, and brown/black to external supply ground joined to Arduino GND. Arduino remains on USB; a loaded servo must not be powered from the board’s 5 V pin. The documented setup is an unloaded, guarded tabletop demonstration.

## Checks and findings

- The existing suite passed 46/46 tests before changes; after changes, 65/65 unit tests passed in the project Python environment.
- The local health endpoint reported ready, RGB/thermal/crop models loaded on CUDA/RTX 4050, and the site was visible at `127.0.0.1:8765`.
- The synthetic `simulate_esp32.py` check passed. Python compileall, `node --check web/app.js` and PowerShell parsing passed.
- Arduino CLI 1.5.1 with AVR core 1.8.8 and Servo library 1.3.0 compiled the sketch for Uno and Nano.
- No firmware upload, physical board connection, servo movement, electrical measurement or end-to-end panel release was performed. Software checks are not physical hardware verification.
- The local branch was clean at the final check. No remote push was made. Recorded commits include `12b106b`, `6f59ea4`, `11fd993`, `44fab0f`, `aaa59e3` and `36b99eb`.

## Findings and decisions

1. The reported local-site error ended with the EYE server ready in the session; maintain the distinction between server readiness and a deeper network diagnosis.
2. RGB preprocessing is now consistent with evaluation, while model weights and labels remain unchanged. Recorded test metrics do not establish field accuracy.
3. pySerial is installed in the correct existing EYE environment. The Arduino gate can be enabled through the site for a server session, but real hardware must be connected and the real COM port selected before a physical demonstration.
4. Keep the gate fail-closed and human-approved. Serial acknowledgements confirm firmware messages, not actual servo position.
5. Preserve the unexplained pending inspection record; its origin remains unresolved.

## Next steps

Connect an actual Uno/Nano and SG90, identify its real COM port, upload the sketch, and use an external regulated 5 V supply with common ground. First test an unloaded, guarded linkage. Confirm the handshake and ordinary inspection behavior with hardware disconnected; then run one eligible and one blocked review case, observe physical movement directly, and record the board, servo, supply, travel and any exceptions.

## Supporting project records

- [System repair audit](../Agastya-EYE/docs/SYSTEM_REPAIR_AUDIT_2026-11-19.md)
- [Arduino installation, operation and wiring](../Agastya-EYE/docs/ARDUINO_SERVO_GATE.md)
- [Arduino sketch](../Agastya-EYE/firmware/servo_gate/servo_gate.ino)
- [Day 39 short entry](Short%20Versions/DAY_39_SHORT_ENTRY.md)
- [Word version](PROJECT_LOGBOOK_DAY_39.docx)
