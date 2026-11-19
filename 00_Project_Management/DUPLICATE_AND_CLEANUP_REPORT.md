# Duplicate and cleanup report — 2026-10-11

## Scan and preservation method

The exact-content scan covered 184 document/data/code files in the curated project, simulation, thermal, and build-note folders (Markdown, CSV, Python, JavaScript, JSON, SVG, PPTX, PDF, DOCX, XLSX, TXT and notebooks; dependency folders, raw image collections, caches and archives excluded). Same-size candidates were SHA-256 hashed. The broader image datasets have their own manifests; this report does not claim to have hashed every image or dependency file.

One exact duplicate group was found:

| Files | SHA-256 | Decision |
|---|---|---|
| `Agastya Physics Simulation/followup_virtual_experiments_metadata.json` and `followup_virtual_experiments_summary.json` | `a542c4095b166a81c1441cde18afc6f28f2ce9be6820db5158592bd7e209371a` | Preserve both. The follow-up generator writes both names, the README calls one a compatibility/convenience copy, and code reads the metadata filename. Removing one would break an expected output path. |

## Similar files that are not duplicates

- The original 11-slide and enhanced 14-slide presentations differ in structure and content. The current 19-slide master and 15-slide concise deck are separate derivatives. Original decks remain preserved in `05_Presentation/Existing_Presentations/`; they are not current competition finals.
- The Phase B/C `v2` outputs and source-qualified `v3` outputs are different versions with different provenance decisions. Keep v2 for audit history; cite v3 for current arithmetic.
- Original and short logbook records overlap by design but are not byte-identical or interchangeable. Original chronology is retained; reconstructed/draft entries are explicitly labelled.
- The Phase A source register and Phase B/C evidence database have different scope and extraction fields. Use the new source evidence register as the navigation/claim index; preserve both source datasets.

## Data requiring separate review

`Agastya-EYE/datasets/processed/pv_multi_defect/duplicate_conflicts.csv` is a dataset-specific duplicate/conflict record. Keep it with its manifest and split definitions; it is not permission to remove raw image files. Do not deduplicate image evidence without checking IDs, hashes, provenance, license, split leakage and the consuming scripts.

## Cleanup actions

- No project source, image, logbook, original presentation, thesis or abstract was deleted.
- No exact duplicate file was deleted. The one exact JSON pair is retained for documented compatibility.
- Old project index remains in `99_Archive/Historical_Artifacts/`; pre-edit rollback snapshots are preserved in `99_Archive/` and SHA-256 verified.
- The earlier project understanding audit is superseded and preserved in `99_Archive/Superseded_Documents/`; the current audit is at `00_Project_Management/PROJECT_UNDERSTANDING_AUDIT.md`.
- Earlier print/display planning and demonstration brainstorming documents were archived as dated history; `06_NCSC_Display/NCSC_PREPARATION_GUIDE.md` and `PRINT_AND_BUILD_REGISTER.csv` are now the single current decision sources.
- The earlier `TASK_TRACKER.csv` and `MILESTONES.md` duplicated status and contained stale completion states. They were preserved in the archive; `PROJECT_STATUS.md` and `MASTER_TASK_LIST.md` are the only current status/task sources. The old paths now contain pointers.
- The original decks remain in `Existing_Presentations` because presentation-inspection utilities reference that location; do not move them without updating and retesting those utilities.

## Human decisions still needed

- Confirm whether old reports and early thesis/abstract claims should remain only as historical reference or be annotated more prominently before any external sharing.
- Review EYE dataset licensing and duplicate/conflict policy before model data are repackaged or redistributed.
- No deletion is recommended from the large app/dependency/data trees as part of this cleanup.
