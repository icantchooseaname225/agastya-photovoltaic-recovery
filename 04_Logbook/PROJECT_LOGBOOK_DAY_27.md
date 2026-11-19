# Project Logbook — Day 27

**Date:** 21 October 2026  
**Entry type:** Digital continuation record prepared during project maintenance. It is not a handwritten student entry and records no physical experiment.

## Purpose

Record a provisional, route-agnostic interface between the corrected Stage 3 thermal-delamination concept and Stage 4 silver removal/recovery, then record the available Python/GPU development environment without implying that it was used to produce Agastya process results.

## Work recorded

- Read the project inheritance brief, current handoff, architecture, task list, open questions, research overview, and recent full and concise logbook entries.
- Added `STAGE3_STAGE4_INTERFACE.md`. It describes the Stage 2 feed identity records; expected Stage 3 glass and cell/EVA/backsheet laminate outputs; the need to record all actual secondary streams and measurements; and the route-specific preparation and product definition still required by Stage 4.
- Kept hot-knife delamination as a literature reference only. Did not set temperatures, times, sizes, yields, product specifications or an extraction recipe. The Stage 4 route remains open; no sample, trial, assay or recovered silver is documented.
- Installed official CPython 3.12.10 and created the external environment `%USERPROFILE%\Envs\agastya-python-3.12-clean`, with the package manifests under `%USERPROFILE%\Documents\Python-Environments\Agastya`. Installed the scientific/data, document, notebook, lint and test packages recorded in those manifests, plus CUDA-enabled PyTorch 2.14.1+cu132 and torchvision 0.29.1+cu132.
- Verified the explicit interpreter path reports Python 3.12.10, `pip check` reported no broken requirements, and a CUDA tensor operation ran on the NVIDIA GeForce RTX 4050 Laptop GPU. CUDA Toolkit 13.2 and VS Code Python/Jupyter/Ruff/SQLite extensions are installed. The environment is outside `C:\Agastya`.
- Checked the active Codex terminal after the user reported Python was missing. The Python executables run by explicit path and the saved Windows user PATH contains Python 3.12, but this already-running Codex process has an older PATH and does not resolve `python`. VS Code's workspace interpreter is configured to the external environment; restarting Codex/VS Code or opening a process with refreshed PATH is needed for the terminal command to resolve by name.

## Findings and limits

- This is a provisional documentation interface, not a physical process specification or approval. Actual feed construction, output condition, Stage 4 preparation, product form, receiver, facility and assay requirements remain unresolved.
- No Agastya code or simulation was run as part of the environment setup. Installing software and confirming a GPU operation do not validate a process model or material recovery.
- The prior Python cleanup was not absolute: a second temporary environment at `%USERPROFILE%\Envs\agastya-python-3.12` remains because the tool's safety policy blocked its recursive removal. The removed Miniconda files are gone, but a stale winget catalog record could not be removed because its registered application was not found. Codex's bundled Python runtime was retained to avoid damaging the application. The new standalone Python and project environment are installed and operational by explicit path.
- There is no verified sample or qualified facility in the project records. The next scientific action depends on those external facts; no answer is inferred here.

## Next action

Resolve P1-02: document whether a traceable representative c-Si sample and qualified supervised host are available. If not, remain at desk-study and cold-fixture planning. Keep Stage 4 route selection open until the actual feed, facility, assay and receiver requirements are known.

## Owner follow-up — Python cleanup status

After the initial environment work, the owner asked that automatic installation pause so they can install the current Python release themselves, after removing Python. The Python 3.15.1 installer was not run. The Python Install Manager check install was removed; the registered CPython 3.12.10 and Python Launcher were uninstalled through winget/Windows uninstallers. Registry and install-folder checks found no remaining standalone Python 3.12 application entry or install directory. The two pre-existing Agastya virtual-environment folders remain. The tool policy blocked recursive removal of the older venv, and deletion of two orphaned pip script files under `%USERPROFILE%\AppData\Local\Python\bin` was also rejected; no alternate deletion method was attempted. The obsolete Python bin folder has been removed from the persisted user PATH. Codex's bundled Python remains. The user will install Python 3.15.1; external dependency manifests were retained for later setup. No project computation was run during uninstall.

