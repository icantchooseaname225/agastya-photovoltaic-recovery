# AGASTYA research logbook — Day 44 (short entry)

**Date:** 21 November 2026
**Status:** AI-assisted digital draft for my review. No physical hardware test was done.

I checked AGASTYA-EYE after the reported localhost connection error. The existing launcher already starts the app on demand and its stop script shuts it down gracefully. The checkout was clean on `main` and matched public `origin/main` at `06cb5d5`; Day 43 was the newest existing logbook pair.

I kept EYE manual-start so its model server does not consume memory when unused. I added `Stop-EYE.bat`, a short start/stop guide, and README guidance explaining that the website cannot start its own server while offline. I created desktop shortcuts **Start AGASTYA-EYE** and **Stop AGASTYA-EYE** for this Windows profile. The local ping scan found no server, so I left it stopped. No boot-time task, background helper, model, database or hardware setting was changed.

**Outcome:** EYE can be started after reboot from the desktop shortcut and stopped with the companion shortcut. The update is designed for on-demand use; no server stays running until the operator starts it.

**Next step:** Start EYE from the desktop after reboot; when done, use Stop to free its memory. If it fails, capture the `.out.log` and `.err.log` paths from the launcher.

**Full counterpart:** [Day 44 full entry](../PROJECT_LOGBOOK_DAY_44.md).
