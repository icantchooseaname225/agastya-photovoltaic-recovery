# AGASTYA research logbook — Day 39 (short entry)

**Date:** 19–20 November 2026<br>
**Status:** AI-assisted digital continuation; pending owner review. No physical hardware experiment or servo movement was conducted.

**Objective:** Restore a usable local EYE service while preserving its data and models, confirm pySerial in the launcher’s Python environment, and prepare a site-controlled Arduino servo-gate demonstration.

**Work undertaken:** The local EYE service was started and checked ready at `http://127.0.0.1:8765`. pySerial 3.5 was installed in the existing Python 3.12 environment. Live RGB preprocessing was aligned with evaluation and reproduced the stored metrics on 104 existing test images (accuracy 84.6%, macro-F1 83.5%). Status/dataset caching, readiness reporting, and launcher start/stop handling were improved. A site Arduino Gate panel, independent controller, append-only hardware event ledger and Uno/Nano sketch were added. The gate requires a ready system, eligible reviewed inspection, serial handshake and one-time operator approval.

**Checks and outcome:** The unit suite passed 65/65; the synthetic simulator and syntax checks passed; Arduino CLI compiled for Uno and Nano. The site control was checked with placeholder `COM99`, without opening a port, and returned to disabled state. Port enumeration found only Bluetooth serial devices; no Uno/Nano was detected. No sketch was uploaded and no physical servo movement or panel release was tested. Existing checkpoints, labels and database schema were preserved. One additional pending inspection record of unknown origin was left untouched. No remote push was made.

**Next step:** Connect an actual board and guarded SG90; upload the sketch, use an external regulated 5 V supply with common ground, connect via the real COM port, and directly observe a tabletop test.

**Full counterpart:** [Day 39 full entry](../PROJECT_LOGBOOK_DAY_39.md).<br>
**Word version:** [Short logbook](DAY_39_SHORT_ENTRY.docx).
