# AGASTYA migration plan and record — 2026-10-11

## Principles
- Preserve every source artifact; no deletion of project content.
- Move only root-level loose artifacts and the original logbook into the new navigation structure.
- Keep the four existing application/research roots in place so their runtime paths and internal assumptions remain stable.
- Keep Agastya-EYE datasets and original media where they are; add inventory links instead of moving bulk datasets.
- Retain original presentation and thesis files byte-for-byte; new presentation files are separate derivatives.
- Update links and script paths, then verify destinations and key links.

## Planned moves
| Source | Destination | Reason |
|---|---|---|
| `Logbook/*` | `04_Logbook/*` | Consolidate all original entries at the logbook root while preserving their relative nesting and links. |
| `Agastya_Presentation*.pptx` | `05_Presentation/Existing_Presentations/` | Preserve the original decks and distinguish them from the new master. |
| `Agastya_Thesis.docx` | `08_Reports/Technical_Reports/` | Preserve the original thesis with its claims clearly audited. |
| `Agastya_Abstract.docx` | `08_Reports/Abstracts/` | Preserve the original abstract. |
| `Agastya_*.svg` concept drawings | `07_Visual_Assets/Conceptual_Illustrations/` | Group conceptual illustrations and keep them distinct from evidence photographs. |
| hidden PowerPoint QA/build utilities | `05_Presentation/Working_Drafts/Build_Utilities/` | Keep historical build/inspection scripts with the presentation work. |

## Link changes to apply
- Update the root project index and all markdown references from `Logbook/` to `04_Logbook/`.
- Update references to the original thesis/abstract and SVGs to their new destinations.
- Retarget the historical PowerPoint utilities to the moved enhanced deck and keep their outputs inside the build-utilities folder.
- Preserve the Stage 3 workbook, thermal and physics modules, Phase A/B-C directories, EYE application, and all datasets at their current paths.

## Verification
- Confirm each source file has exactly one destination copy and no originals were lost.
- Search markdown, scripts, and CSVs for stale references to moved root files.
- Validate the project index links after it is rewritten.
- Record all new outputs, paths and checks in the change log and tracker.

## Execution record — 2026-10-11
- Archived the previous project index at 99_Archive/Historical_Artifacts/AGASTYA_PROJECT_INDEX_2026-10-10.md.
- Moved original Logbook contents to 04_Logbook, preserving their internal folder structure and peer-relative links.
- Moved both original PowerPoint decks to 05_Presentation/Existing_Presentations.
- Moved the original thesis and abstract to 08_Reports/Technical_Reports and 08_Reports/Abstracts.
- Moved six conceptual SVG files to 07_Visual_Assets/Conceptual_Illustrations.
- Moved the original hidden presentation build/inspection utilities to 05_Presentation/Working_Drafts/Build_Utilities and retargeted paths.
- Updated simulation, thermal, EYE and project links to moved files.
- Rewrote the root index and README, created logbook entries and added project management records.
- Key-link search and destination checks are included in the final consistency audit.
