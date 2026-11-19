# AGASTYA-EYE software repair report

**Repair date:** 26 October 2026  
**Application:** C:\Agastya\Agastya-EYE  
**Result:** launcher and local inference path verified on this computer; no physical inspection or recycling process was tested.

## Reported issue and diagnosis

The user reported that the EYE server was not opening. At investigation time a Python 3.14 EYE server was already listening on port 8765, and the browser page and API were responsive. I therefore did not reproduce an active startup crash; the historical cause is unknown.

The code review found two concrete reliability defects. The PowerShell launcher hardcoded a machine-specific Python installation path. Also, the RGB, visible-crop and thermal model loaders forced both the model and inference tensors onto CPU, despite a working CUDA-enabled PyTorch installation being present.

## Changes made

| File or area | Change | Verification |
|---|---|---|
| Start-EYE.ps1 | Removed the fixed interpreter path. Added environment override, project venv, Python Launcher and PATH discovery; probes required imports and reports versions/GPU; startup errors include diagnostics. | Documented PowerShell launcher selected Python 3.14.9 and reached ready state. |
| inference/device.py | Added auto, cpu and cuda preferences. Auto mode falls back visibly if CUDA initialization or inference fails; forced CUDA and invalid settings fail clearly. | Four focused device tests passed. |
| RGB, visible-crop and thermal loaders | Move models and tensors to the selected device; report device and fallback state. | All three checkpoints loaded and produced real inference on cuda:0. |
| Browser status display | Shows the selected inference device in model status. | Refreshed page displayed the RTX 4050 device label. |
| README.md | Documented environment selection and device controls. | Reviewed against launcher behavior. |
| tests/test_inference_device.py | Added tests for CPU mode, visible CPU fallback, invalid preference and real checkpoint CUDA inference. | Four focused tests passed. |

## Test and integration results

- Before repair: the EYE suite passed 42/42 tests from the project root. The first discovery attempt used the wrong working directory and failed imports; rerunning from the correct root passed.
- Focused device regression suite: 4/4 passed.
- After repair: full EYE suite 46/46 passed.
- Python syntax compilation: passed.
- Documented launcher: selected Python 3.14.9, PyTorch 2.14.1+cu126, torchvision 0.29.1+cu126, CUDA 12.6 and RTX 4050; started a fresh server at 127.0.0.1:8765.
- Health/model path: RGB, visible-crop and thermal models all reported loaded and ready on cuda:0; real image inference completed for each.
- Read-only endpoints: /, /app.js, /process.js, /materials.js, /styles.css, /source-manifest.csv, /api/ping, /api/status, /api/v1/health, /api/datasets, /api/panels, /api/inspections, /api/material/records and /api/material/runs returned HTTP 200.
- Database: SQLite integrity_check returned ok; foreign_key_check returned zero rows. Existing counts were 5 panels, 5 inspections, 0 material-journal rows and 0 stage events. API checks were read-only.

## Remaining limits

The local server and CUDA inference path work. The old user-observed failure was not reproduced, so its historical trigger is not known. The RGB sidecar benchmark metrics were not recalculated; no independent local-panel evaluation, camera connection, calibrated electrical measurement, network-security review or physical sorter validation was performed. Software tests and GPU inference do not establish recycling performance.
