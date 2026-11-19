# AGASTYA final quality assurance report

**QA date:** 26 October 2026  
**Project root:** C:\Agastya  
**Final package:** C:\Agastya\district level final

## Verification summary

| Check | Result | Evidence boundary |
|---|---|---|
| EYE test suite | 46/46 passed after repair; 42/42 before repair | Software behavior only |
| Device regression tests | 4/4 passed | Includes real checkpoint CUDA inference when available |
| Stage 4 model suite | 7/7 passed | Calculation checks, not a physical process |
| Python compilation | Passed | Syntax/import compilation, not hardware validation |
| Launcher and server | Fresh server ready at 127.0.0.1:8765 | Previous failure not reproduced; environment selection repaired |
| Vision models | RGB, visible-crop and thermal checkpoints ran on cuda:0 / RTX 4050 | Does not reproduce benchmark metrics or establish field accuracy |
| API and static routes | Tested read-only routes returned HTTP 200 | Does not validate external device integration |
| SQLite | integrity_check=ok; foreign_key_check=0 | Existing data read only |
| Short logbook | 29 canonical records plus 5 separate review drafts; 34/34 matched in DOCX and PDF | Drafts unauthenticated; Days 1, 2, 14 and 22 remain unresolved |
| Scientific visuals | 21 registered figures F01–F21; F08 updated to show 46 EYE and 7 Stage 4 tests | No new experimental data or measurement graph created |
| Verification reports | Three reports, each with one summary table | Environment, repair and QA evidence |

## Document and presentation checks

The competition project report, abstract, Stage 1 report, expanded thesis, project file, model register and both speaking scripts were regenerated from their Markdown sources. DOCX files were exported to PDF using Microsoft Word because LibreOffice is not installed. Rendered pages were converted to PNG for visual review; extracted PDF text was checked for content and page output.

The presentation remains 18 slides. The updated PPTX and PDF were exported, all slides rendered, and slide text was inspected. The revised script and presentation claims state that local checkpoint loading and inference are verified while sidecar metrics and field accuracy remain unverified.

## Scientific claim checks

- No physical AGASTYA panel-processing run, silver recovery, purity assay, throughput or cost result is claimed.
- Stage 3 output remains glass plus cell/EVA/backsheet laminate.
- Stage 4 scenarios remain assumption-driven arithmetic; ECS is conditional and bypassed by default.
- The published flotation table's 92.93% calculated silver closure and unresolved discrepancy remain attributed to the source table.
- Model inference on CUDA is distinguished from benchmark reproduction and field validation.

## Unresolved submission and engineering gates

Participant/school/guide fields and local competition rules require confirmation from official records. The showcase build dates and eligible logbook drafts still need owner/guide review. Camera and electrical hardware, independent panel labels, Stage 3 feed characterization, supervised physical trials, downstream receiver, assay, product purity, waste route, cost and life-cycle results remain open. No physical experiment is implied by this QA.

## Integrity and status

Historical logbooks and dated audit records were preserved. This report is a verification summary; final page counts, hashes and render counts will be appended after the last build and manifest verification.
