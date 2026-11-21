# AGASTYA research logbook — Day 44

**Date:** 21 November 2026
**Status:** AI-assisted digital continuation; draft pending owner review. No physical hardware test was performed.

## Objective

Repair the local AGASTYA-EYE restart workflow so the operator can start it after a PC reboot without leaving the model server running continuously; record the verified software and GitHub state and continue the full/short research-logbook sequence.

## Work undertaken

I checked the EYE checkout and repository before editing. `C:\Agastya\Agastya-EYE` is part of the `C:\Agastya` Git repository. The working branch was `main`, with a clean tree and `HEAD` matching `origin/main` at `06cb5d5`. The latest existing research-logbook pair was Day 43, so I recorded this work as Day 44 instead of creating entries for already documented days.

I reviewed `Start-EYE.ps1` and `Stop-EYE.ps1`. The existing start launcher already starts the Python app in the background on demand, waits for the local API, and opens the browser. The existing stop script requests graceful shutdown and verifies the process ended. There is no need to keep a resident helper or add a boot-time task. A site page cannot launch the server while it is stopped because that same server hosts the page.

I added `Stop-EYE.bat` to make graceful stop available by double-click, plus `docs/START_EYE_QUICKSTART.md` explaining post-reboot startup, shutdown, memory behavior and troubleshooting. I updated the main README to state that EYE is intentionally on-demand and to explain why an offline site cannot start its own backend. On this Windows profile I created desktop shortcuts named **Start AGASTYA-EYE** and **Stop AGASTYA-EYE**, targeting the repository's batch launchers. These shortcuts do not run in the background by themselves.

## Checks and findings

- Before edits, `git status` was clean on `main`; `git fetch origin` completed and local `HEAD` matched `origin/main` at `06cb5d5`.
- The local ping scan found no running EYE server, matching the reported connection failure. I left the model server stopped so it does not consume memory until the user chooses Start.
- The start target remains the existing `Start-EYE.bat`/`Start-EYE.ps1` flow. The new stop target invokes `Stop-EYE.ps1`; it does not force-kill processes.
- I verified the new documentation and launcher file locations and created the two on-demand desktop shortcuts. No Windows startup task, service, or always-running helper was installed.
- No model weights, database, inspection records or hardware settings were changed. No Arduino port was opened and no physical hardware was tested.

## Findings and decisions

1. The earlier localhost error occurs when EYE is not running; after a PC reboot the server is expected to be off because startup is manual.
2. Keep EYE off until needed to avoid continuous RAM use. Start from the desktop shortcut; use the Stop shortcut when done. Browser close alone leaves the server process running.
3. A start button inside the EYE page cannot help when EYE is off. A separate always-on helper could bridge that gap but would stay resident, so it was not installed.
4. Before these edits, the public GitHub repository was synced with local `main`. This entry records the new on-demand start/stop usability work in the project history.

## Next steps

Double-click **Start AGASTYA-EYE** after a reboot and confirm the browser opens at the printed localhost URL. When the inspection session is finished, double-click **Stop AGASTYA-EYE** to release model/server memory. If startup reports an error, use the log paths printed by the launcher and share them for diagnosis.

## Supporting records

- [EYE on-demand start/stop guide](../Agastya-EYE/docs/START_EYE_QUICKSTART.md)
- [Start launcher](../Agastya-EYE/Start-EYE.ps1)
- [Stop launcher](../Agastya-EYE/Stop-EYE.ps1)
- [Day 44 short entry](Short%20Versions/DAY_44_SHORT_ENTRY.md)
