# Tools and software actually used — 2026-10-11

## Research, data and authoring

- Local filesystem search/read/write tools inspected project files and moved root loose assets.
- Web search verified primary study records and current official DST/NCSC material; links and source boundaries are preserved in reports.
- CPython 3.14.4 ran the Phase B/C evidence builder, scenario model, published-value reproduction, accounting unit tests and legacy validation probes.
- NumPy 2.5.3 is available and was used by the earlier thermal model; Phase B/C arithmetic uses deterministic standard-library code.
- Node.js 24 and PptxGenJS generated the master and short PowerPoint decks.
- Bundled Python packages python-pptx, ReportLab and Pillow supported slide inspection, vector PDF/poster creation and contact-sheet review.
- Poppler pdftoppm rendered poster PDFs for visual inspection. The skill validator passed both new PPTX files.
- The Codex PowerPoint skill was consulted and applied. Workspace dependency paths were loaded through the Codex app.

## Inspected or attempted

- The original 14-slide enhanced deck passed structural validation. Its 40 embedded PNG assets were extracted and inspected; all are line icons and no provenance register was present.
- PowerPoint COM export was attempted but did not reliably open the existing presentation in headless mode. The provided LibreOffice wrapper could not run because the Windows Python environment lacks AF_UNIX support.
- Plugin discovery identified optional design tools but none was installed or invoked. No connected PowerPoint document session was available.
- No external facility was contacted and no message was sent to another person.

## Not used as physics engines

PowerPoint, PptxGenJS, ReportLab, PowerShell, the EYE application and Wokwi do not establish material recovery. No Ansys Maxwell/Rocky, SimScale, FEM, DEM, CFD, chemistry solver, assay instrument or lab instrument was run in this continuation.


## Python/CUDA environment update — 2026-10-21

- Installed official CPython 3.12.10 at `%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe`; created the Agastya virtual environment at `%USERPROFILE%\Envs\agastya-python-3.12-clean`, outside the project.
- Installed NumPy, pandas, Pillow, pypdf, ReportLab, Matplotlib, SciPy, scikit-learn, OpenCV, openpyxl, JupyterLab, ipykernel, pytest and Ruff. Installed CUDA-enabled PyTorch 2.14.1+cu132 and torchvision 0.29.1+cu132. The full package lock and install manifests are under `%USERPROFILE%\Documents\Python-Environments\Agastya`.
- CUDA Toolkit 13.2 is installed. A CUDA tensor operation succeeded on the NVIDIA GeForce RTX 4050 Laptop GPU; `torch.cuda.is_available()` returned true. `pip check` reported no broken requirements.
- VS Code is installed with Python, Pylance, Python Environments, Jupyter and Ruff extensions; SQLite support was added. `C:\Agastya\.vscode\settings.json` points the project workspace to the external interpreter.
- The current Codex terminal has a stale inherited PATH: the explicit executable works, and the saved Windows user PATH contains Python, but the active shell cannot resolve `python` by name. Restart Codex/VS Code or use a newly refreshed process.
- Cleanup limitation: Miniconda's installation directory and Python 3.15 were removed, but a stale winget catalog entry could not be unregistered after its application was no longer found. A temporary venv at `%USERPROFILE%\Envs\agastya-python-3.12` remains because the tool safety policy blocked recursive removal; no alternate deletion was attempted. The Codex-bundled Python runtime was retained to avoid damaging Codex. Therefore the requested clean uninstall was not absolute, although the new standalone Python and project environment are operational.
- Software installation/GPU verification did not run an Agastya process model and provides no physical process or recovery evidence.

## Owner-directed Python removal follow-up — 2026-10-21

- The user asked that automatic current-version installation stop while they install Python themselves. Python 3.15.1 was not installed.
- Removed the Python Install Manager check install, the registered Python 3.12.10 standalone installation and Python Launcher through winget/Windows uninstallers. Subsequent registry/install-folder inspection found no standalone Python 3.12 registration or install directory.
- Two Agastya virtual-environment directories remain because the tool safety policy blocked recursive cleanup; no alternate deletion method was attempted. Codex's bundled Python runtime remains app-owned. The Miniconda install folder is absent, but a stale winget catalog entry remains. Therefore the request to remove every Python copy is not fully complete.
- Preserved package requirement manifests outside `C:\Agastya`; updated their README with the user-directed pause and commands for setup after the user installs Python 3.15.1. Cleared the Agastya VS Code interpreter override until the new interpreter is available.
- The previously verified CUDA/PyTorch check was performed before uninstalling Python 3.12. It is historical; the next Python environment must be verified after installation.

- Final cleanup inventory: no standalone Python 3.12 registry registration or install directory remains; the Python bin directory is no longer on user PATH. Two venv directories, two orphaned pip script stubs, the app-owned Codex runtime, and the stale Miniconda package catalog entry remain; the tool rejected deletion of the venv/stubs, so no alternate removal was attempted.

