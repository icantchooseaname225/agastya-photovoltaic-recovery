# AGASTYA final consistency audit — 2026-10-11

## Scope

This audit closes the current desk-research, documentation and presentation pass. It checks project navigation, generated research outputs, software execution records, slide structure, and print-file dimensions. It does not represent a physical experiment or independent laboratory validation.

## Workspace and navigation

- The root index and README link to the organized research, engineering, logbook, presentation, NCSC display, reports and software records.
- The previous index is preserved under `99_Archive/Historical_Artifacts/`.
- The latest inventory contains **53,859 files** (the exact size is recorded in `file_inventory_summary.md`). It includes the large Agastya-EYE image collection, application/build files and caches, so it is a workspace inventory rather than a count of curated research records.
- The curated file catalog contains **86 records**, the migration log contains **64 moves**, and the print/build register contains **17 decisions**. Every current catalog path and migration destination exists; all print outputs remain unapproved for printing.
- The Markdown checker inspected **262 local links** and found **zero broken links**. A separate scan found no stale root `Logbook/` references outside the archive.
- Original logbook records, presentations, thesis, abstract and conceptual drawings were retained at their organized destinations; the migration record lists these moves.

## Research and calculations

- The Phase B/C evidence database contains 14 source records, the route comparison covers five candidate routes, and the software access matrix has seven entries.
- Published-data reproduction and scenario/sensitivity outputs are saved alongside their scripts and reports. Literature values remain source-specific and are not represented as AGASTYA measurements.
- For the Saffarian et al. reported rounded mean table row, the reproduced tail-depletion recovery is 97.5417%, close to the reported 97.55%. The ratio-of-means concentrate recovery is 90.4727%, and the derived three-stream Ag balance closes at 92.9310%. These are diagnostics from rounded means; replicate-level measurements are required to establish the source study's balance.
- The 300 ppm review scenario, 600 g/t publisher-abstract wording and secondary 630 g/t excerpt are separate and have unresolved source-basis limitations. They are not pooled into an AGASTYA feed grade or statistical interval.
- Current evidence supports mechanical size classification as a candidate preparation step and direct Ag-bearing flotation literature as a stronger quantitative benchmark than the accessible electrostatic studies. The reviewed electrostatic sources do not supply enough mass-weighted Ag recovery and grade data to validate Stage 3. None of these literature results establishes AGASTYA performance.

## Software and computational validation

- The documented desk calculations and validation scripts were run with CPython 3.14.4. The presentations were generated with PptxGenJS; `python-pptx` was used for structural inspection, and Poppler was used to inspect/render poster PDFs. See [programs and simulation scope](../09_Software_and_Environment/PROGRAMS_USED_AND_SIMULATION_SCOPE.md).
- The v2 accounting unit suite passed **28/28 tests**.
- The preserved Phase A kernel audit passed **22/25 probes**. Three known gaps remain in the historical implementation: it accepts recovery above 100%, grade above 100%, and NaN. The v2 tests reject those invalid inputs; the legacy implementation was preserved and its gaps are recorded.
- Existing thermal outputs are a lumped thermal RC model and virtual scenario/time-history rows. The previously recorded 200,080 rows are not independent physical replicates.
- **No electrostatic, DEM, CFD, FEM, particle, chemistry or assay engine was run.** No actual panels, coupons, particles or samples were tested; the physical sample count is zero.

## Presentations and display files

- The current master has 19 slides and the concise deck has 15. Structural XML inspection found notes on every slide, no empty slides, no out-of-bounds shapes and no replacement glyphs; the master has two attributed illustrative photographs and the concise deck has the cover photograph. Target-app visual review remains outstanding.
- The four A1 poster PDFs were checked at 594 × 841 mm page size; the four companion PDFs were checked at A4 page size. All eight PDFs passed prior one-page and extracted-text checks, were rendered and visually inspected as working layouts, and remain pending student/teacher proof and event-rule approval. They are now together in the project-root `printables/` folder.
- PDF export of the new PowerPoint decks could not be confirmed in this Windows environment. The PPTX files have structural checks, but their final slide rendering remains to be reviewed in PowerPoint or another compatible renderer.
- A1 is the prepared draft size, not a confirmed NCSC rule. A coordinator must confirm the current category, abstract, time limit, display size/count and local event requirements before submission or printing.

## Conclusions and remaining dependencies

The project now has an organized, traceable desk-research package: source-linked evidence, transparent arithmetic, explicit software scope, versioned accounting checks, draft logbook summaries, presentations and display materials. The defensible conclusion is that AGASTYA has a research plan and candidate separation approaches; it does not yet have measured recovery, grade, purity, throughput, safety, environmental benefit or cost performance.

Physical validation depends on verified samples, a qualified facility, documented equipment and assay methods, and an approved procedure. Solver work additionally depends on measured feed/particle properties and an appropriate validated solver. NCSC submission depends on the student/team, guide, local problem and event-specific instructions. These dependencies are tracked in the [master task list](MASTER_TASK_LIST.md).

## Acceptance status

| Category | Status | Evidence / reason |
|---|---|---|
| Project organization | COMPLETE | Root navigation, 81-record catalog, 56-row migration log, documented archive and verified current paths. |
| Scientific quality | PARTIAL | Source-qualified literature arithmetic and evidence limits are documented; sample provenance and Stage 3 performance remain unresolved. |
| Repair and verification | PARTIAL | 28/28 accounting tests and 42/42 EYE unit tests pass; 22/25 legacy probes pass with three known flaws; 246 links and eight PDFs validate. PowerPoint slides and the updated browser walkthrough still need visual review in a compatible renderer. |
| Human usability | COMPLETE | Start page, project index, status dashboard, task list, research/engineering/data guides and logbook index are present and cross-linked. |
| NCSC readiness | BLOCKED | Local event rules, student/teacher review and notebook/project approval are outstanding; no display file is authorized for printing. |

## Follow-up update — presentation and printables (2026-10-11)

This later same-day update supersedes the earlier presentation counts and print-file location above.

- Rebuilt the authoritative master at **19 slides** and the concise deck at **15 slides** from the current source. Structural inspection found one notes slide per content slide, no replacement glyphs, two attributed illustrative photos in the master and the cover photo in the concise deck. Target-app visual review remains outstanding.
- Added a model inventory slide whose categories reconcile to the saved dataset summary: 1,536 routing/material-balance rows + 7,080 thermal rows + 129,220 size-model rows + 62,208 conditional Ag-arithmetic rows + 36 capacity cases = **200,080 virtual records**. They are scenarios, model histories and conditional literature arithmetic—not physical experiments.
- Consolidated the eight generated A1/A4 PDFs in the project-root `printables/` folder. Poppler `pdfinfo` verified one page per file and the generated A1/A4 page sizes. The dedicated Python validator could not be rerun in the current interpreter because `pypdf` is not installed; the earlier text/render checks are recorded above. All files remain working layouts and `print_ready=NO` pending event rules and human proof.
- The current Markdown-link check inspected **262 local links with zero broken/failed links**. The refreshed catalog contains 86 records, the migration log has 64 moves, the print/build register has 17 decisions, and the recursive inventory contains 53,859 files.
- Images: Fomanu's 2015 PV panel photograph and Fdenicola's 2013 solar-cell photograph are illustrative, attribution/licence recorded in the visual asset register, and not AGASTYA equipment or samples.
