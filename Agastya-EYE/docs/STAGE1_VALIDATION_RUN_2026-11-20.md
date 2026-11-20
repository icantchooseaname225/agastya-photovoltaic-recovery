# Stage 1 software validation run — 20 November 2026

## Unit-test suite

I ran the existing EYE unit tests using the launcher's existing Python 3.12.14 environment. No packages were installed for this run.

```powershell
& "$env:USERPROFILE\Envs\agastya-python-3.12\Scripts\python.exe" -m unittest discover -s tests -v
```

**Result: 65 tests passed.** This covers the existing EYE unit-test suite, including routing, the append-only material ledger, inference preprocessing, dataset contracts, system-health reporting, serial-controller behavior and hardware-approval rules.

## Synthetic device-protocol workflow

I ran the documented PC-only simulator with the same Python environment:

```powershell
& "$env:USERPROFILE\Envs\agastya-python-3.12\Scripts\python.exe" tools\simulate_esp32.py
```

The simulator completed successfully. Its checks use synthetic images, a stub classifier, a temporary database and loopback HTTP calls. It verifies the health endpoint, authenticated synthetic uploads, image hash retrieval, retries, panel passports, modality handling, safety routing, Stage 2–4 event sequencing and hash integrity.

## Limits

The unit tests and simulator do not validate live camera capture, model accuracy on new panels, actual serial communication with an Arduino, physical servo movement, an electrical test, a PV panel, or any thermal or recovery process. The Day 39 record reports successful compile checks for Uno and Nano. No board was connected and no firmware was uploaded during this continuation.

The earlier 19 November attempt used a separate Python 3.14 interpreter without the ML/image packages and therefore had six dependency errors. The complete Python 3.12 result above supersedes it for current software-suite status; the earlier report is retained as a dated record of that attempt.
