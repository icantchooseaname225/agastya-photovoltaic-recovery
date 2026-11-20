# Agastya-EYE repair and hardware audit — 19 November 2026

## Preservation baseline

- Existing checkout: `C:\Agastya\Agastya-EYE`, Git root `C:\Agastya`, starting revision `3ccd78a`.
- Work is on local branch `codex/agastya-eye-serial-integration-20261119`; the `main` branch was not changed.
- Before changes, the existing suite passed **46/46** with the existing Python 3.12.14 launcher environment (`%USERPROFILE%\Envs\agastya-python-3.12\Scripts\python.exe`).
- A read-only baseline copy of `database\eye.sqlite3` was made before the work. At that point it had six inspections and six panels, SHA-256 `13C1E0214C9EE535E2899207C92A98684D675727FB702A6DC711FD7962E746B0`.
- A seventh append-only inspection appeared later during the audit (`PV-000007`, `2026-11-19T18:17:11Z`, `PENDING_REVIEW`). The launcher-managed logs checked do not show an inspection POST, so its source is undetermined. Its record and image were left intact. The current database hash is `91854664FA19B9334F4315444539585FA7B0E79B7C92019BEE12455462B97472`; it has seven inspections and seven panels, `quick_check` is `ok`, and the foreign-key check is empty.
- The existing MobileNetV2 RGB, thermal, and close-up checkpoints and class definitions were retained. No training ran and no checkpoint was written. All three existing model loaders reached `loaded: true` in the post-change live server check.
- No destructive change was made to the main inspection database schema. Hardware approvals use a new, separate append-only `database\hardware.sqlite3` ledger.

## Confirmed findings and repairs

### RGB evaluation and live inference used different transforms

Training validation and test evaluation used TorchVision `Resize(256)`, `CenterCrop(224)`, tensor conversion, and ImageNet normalization. Live inference used a separate PIL resize/crop path with different rounding and resampling. The active checkpoint and test data were present, but the live predictions did not reproduce the recorded test metrics.

The live RGB classifier and training evaluation now call one shared deterministic transform. On the existing 104-image held-out test set, live inference reproduces the sidecar confusion matrix (class order `bird_drop`, `clean`, `dust`, `other`) and its **84.615% accuracy / 83.534% macro-F1**. This is reproducibility against the existing small benchmark, not evidence of field accuracy. The checkpoint and labels were not changed.

### Dataset status repeatedly walked image trees

`/api/status` embeds the dataset summary, and `/api/datasets` builds the same summary by walking processed and raw image folders. Recomputing it for every request caused avoidable repeated filesystem work. The summary is cached for 30 seconds; database and live model health remain checked separately.

After model warm-up, one PowerShell smoke sample measured `/api/status` at 148 ms then 24 ms, `/api/datasets` at 9 ms then 9 ms, `/api/inspections` at 15 ms, and `/api/ping` at 5 ms. A prior single baseline sample on this machine was approximately 778 ms for `/api/status` and 609 ms for `/api/datasets`. These are individual local round trips, not a statistically controlled benchmark.

### Health previously did not describe readiness

`/api/ping` is retained as a liveness check. The new `/api/v1/health` separately checks the primary SQLite ledger, metadata/checkpoint compatibility, and whether the RGB model has finished loading. It reports `warming` while the model initializes and `degraded` when the database or primary model cannot be used; non-ready health returns HTTP 503. It also reports thermal/crop model state and the independent hardware ledger. GET failures are logged and return an error status rather than an artificial success.

The first launcher probe can occur before the background model warm-up finishes. `Start-EYE.ps1` now waits for readiness for up to 45 seconds and reports a persistent degraded result clearly. `/api/ping` remains useful when diagnosing a live server whose models or database are not ready.

### Python environment and serial dependency

The application’s working environment is the existing `%USERPROFILE%\Envs\agastya-python-3.12` environment. It already contained Python 3.12.14, PyTorch, TorchVision, NumPy, Pillow, pytest, and CUDA support, but lacked pySerial. A separate Python 3.14 environment used by an older validation attempt lacked PyTorch, NumPy, and Pillow, which explains those prior import errors; it is not the environment used by the EYE launcher.

Installed **pySerial 3.5** with that environment’s `python.exe -m pip install pyserial`. No unrelated package was upgraded and no new virtual environment was created. The launcher now verifies the same Python interpreter can import PyTorch, TorchVision, NumPy, Pillow, and `serial` before selecting it.

### Startup, request errors, and stop handling

The application binds to loopback by default and the launcher scans its documented local port range. Device-network binding still requires the existing upload token. Browser requests now have a 60-second abort timeout and display actionable network/timeout errors. The launcher records the PID and script path only for a server it starts. `Stop-EYE.ps1` verifies that identity, requests the loopback shutdown endpoint, waits for orderly exit, and never force-kills the process.

During the audit, the existing PC simulator initially failed because its stub classifiers did not implement the new `status(load=False)` health interface. The simulator stubs were updated to match the production interface; the simulator then passed. This exposed and fixed a test harness compatibility issue, not a production inference failure.

No production logs or reproducible evidence of a memory leak or a concurrent database failure were present. This work did not run a prolonged memory soak or high-concurrency load test, so those possibilities are not ruled out.

## Arduino extension and approval boundary

The existing classifier remains independent. Hardware activation defaults to disabled (`AGASTYA_HARDWARE_ENABLED=0`). The local-only hardware card/API requires a separate operator ID and exact panel ID confirmation after the existing workflow has recorded a fresh, front-view RGB inspection whose image still matches its stored SHA-256, c-Si technology, a high-confidence clean result with the existing confidence/margin limits, the `SECOND_LIFE_REVIEW` route, human-confirmed `REUSED` disposition and note, and an instrumented electrical pass with voltage/current readings. The Arduino Gate site panel can enable activation for the current session after the operator enters a Windows COM port; it does not open that port until the separate Connect action. Pending, rejected, stale, uncertain, incomplete, unsupported-modality, or already-used inspections are refused.

The controller uses pySerial, configurable COM port and baud rate, bounded serial timeouts, a nonce readiness handshake, command validation, command acknowledgements, one-time request/event audit, and no retry after an uncertain result. Partial writes, bad acknowledgements, duplicates, and reconnect failures fail closed. An Arduino `ACK`/`DONE` proves only that the sketch issued open/close commands; there is no position sensor to verify the SG90 or barrier physically moved.

The Uno/Nano sketch is `firmware\servo_gate\servo_gate.ino`: Servo library, D9 signal, 0-degree closed and 90-degree open command, 9600 baud, 1–30 second timed opening, duplicate-ID rejection, and non-blocking return to the commanded closed position. The separate [Arduino guide](ARDUINO_SERVO_GATE.md) has Windows setup, upload, wiring, power, troubleshooting, and demo instructions. Use an external regulated 5 V supply sized for the servo and common ground; do not power a loaded SG90 from the Uno/Nano 5 V pin.

Automated tests use a mocked serial device. On this PC, all enumerated COM ports were identified as Standard Serial over Bluetooth links; no Uno/Nano was detected. Arduino CLI 1.5.1, AVR core 1.8.8, and Servo library 1.3.0 are available; the sketch compiles for both Uno and Nano. No firmware was uploaded and no physical servo, barrier, panel, or camera demonstration was performed.

## Verification

From the project directory, with the selected interpreter:

```powershell
$EyePython = Join-Path $env:USERPROFILE 'Envs\agastya-python-3.12\Scripts\python.exe'
& $EyePython -m unittest discover -s tests -v
& $EyePython tools\simulate_esp32.py
node --check web\app.js
```

Post-change results on 19–20 November 2026:

- Full `unittest` suite: **65/65 passed** (the original 46 plus 19 new health, preprocessing, serial, site-activation, and approval checks).
- Existing PC-only simulator: passed all synthetic upload, retry, image hash, routing, passport, and Stage 2–4 checks.
- Python `compileall` and JavaScript syntax check: passed.
- Real launcher smoke check: all three model statuses reported loaded; `/api/v1/health` reported ready; status, dataset, inspection, and ping endpoints returned success; the disabled hardware connect/release endpoints returned HTTP 503 without opening a serial port.
- `Stop-EYE.ps1` stopped the launcher-managed server cleanly. The inspection database hash matched its pre-change copy.
- After adding site activation controls, the local API was exercised with a placeholder `COM99`: it enabled and disabled the session without opening a port, then the test port was cleared. No actual Arduino COM port was opened.

## GitHub status

The configured public GitHub repository exists but is empty (no remote refs were returned). No content was pushed. Changes are kept in the local development branch and committed in stages; do not push this broad parent checkout into the empty public repository without first confirming the intended repository contents.

## Remaining checks

- Compile/upload the sketch after installing the Uno/Nano AVR platform and Servo library through Arduino IDE/CLI, then verify the unloaded guarded tabletop linkage in person.
- Run a physical end-to-end demonstration with an actual inspection and operator approval. The software checks cannot verify real servo travel, barrier closure, pinch guarding, or any production safety function.
- Run a longer concurrency/memory soak if intermittent failures continue after the readiness, cache, and request-timeout repairs.
