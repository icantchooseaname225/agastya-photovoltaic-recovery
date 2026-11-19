# AGASTYA project understanding audit

**Updated:** 19 November 2026  
**Project root:** `C:\Agastya`  
**Scope:** current project structure, four-stage architecture, evidence status, research records, software access and repository readiness.

## Project structure and audit findings

A full metadata inventory generated on 19 November 2026 enumerated 47,546 files totaling about 3.81 GB with no traversal errors. It records relative path, extension, size and UTC modification time; it does not read or validate every file content. The largest content cluster is the EYE public-data image store. `work/` contains audit/scratch material and should not be treated as canonical project documentation. The local inventory CSV is ignored by Git because it exposes the full dataset path list.

The principal current references are [AGASTYA_ARCHITECTURE.md](../AGASTYA_ARCHITECTURE.md), [PROJECT_STATUS.md](../PROJECT_STATUS.md), [the project index](../AGASTYA_PROJECT_INDEX.md), [the Stage 3/4 interface](../STAGE3_STAGE4_INTERFACE.md), the [research overview](../01_Research/RESEARCH_OVERVIEW.md), and the dated Stage 2, Stage 3 and Stage 4 reviews linked there. Older decks, thesis sections, simulation rows and logbook entries remain historical and should be labelled before reuse rather than silently edited.

## Current architecture and evidence classes

The project-owner direction recorded on 19 November 2026 now governs current design:

| Stage | Current function | Evidence state |
|---|---|---|
| 1. AGASTYA-EYE | Vision-based triage and traceability. | Application and models implemented. RGB candidate benchmark: 104 group-aware held-out images, 84.6% accuracy and 83.5% macro-F1; results are mixed by class and not field-validated. Image analysis does not measure electricity, module composition, or silver. |
| 2. Robotic disassembly | Automated mechanical disassembly with a robotic-arm-centered workcell, fixture and task-specific tooling. | Architecture/design review plus one executed 2D reach screen. No CAD assembly, selected arm, force model, robot motion validation or physical disassembly. |
| 3. Thermal separation | Hot knife followed by foam-roller concept; assess adjacent post-thermal liberation. | Prior layered thermal conduction simulations exist for the hot-knife concept. They do not include foam-roller mechanics or delamination quality. No integrated build/trial. |
| 4. Liberation/separation/recovery | Characterize feed, concentrate/remove silver, and define downstream refining. | Literature and scenario calculations exist. No AGASTYA sample assay, process run, concentrate or recovered silver. Conventional ECS is not justified as the default. |

Keep the evidence categories separate: proposed, theoretically described, computationally modeled, numerically simulated, experimentally tested, and validated against measured AGASTYA results. For Stages 2–4, the last two categories have no project evidence.

## Research and model records

- EYE's RGB classifier is limited to four broad visual classes and a small single-source evaluation. A per-class regression is recorded: the candidate `bird_drop` F1 is 72.7% versus 82.9% for the earlier checkpoint. Thermal and close-up classifiers have distinct input/domain limitations and are advisory.
- The Stage 2 model checks only planar base-to-perimeter radius for an illustrative panel and fixed base. It is not CAD, inverse kinematics, collision, torque, repeatability or production-cycle validation.
- The Stage 3 five-node and spatial-refinement work is a numerical thermal-conduction study with explicit limitations. No physical calibration exists, and foam/roller contact, adhesion fracture, particle liberation and output quality are outside the model.
- Stage 4 contains literature-normalized calculations and scenario models. The 200,080 legacy virtual rows and the newer Stage 4 scenario outputs are not observations or statistical replicates from AGASTYA feed.
- The source evidence register now contains 18 aligned CSV records. Its malformed EV-005 row was corrected; new process-automation and ECS references are recorded as EV-016–EV-018.

## Logbooks and historical continuity

Day 30 remains the latest full entry located before this session. A combined short-only file documents Days 31–33 (16–18 November); no full counterparts were located, and none has been reconstructed. Day 34 (19 November) now has a full and short AI-assisted digital continuation based on work actually performed in this session. The logbook index states these boundaries and awaits owner verification of AI-assisted text.

## Software and version control

The workspace is **not** a Git repository and contains no remote URL. Git and Git LFS are installed; GitHub CLI is not on PATH. GitHub Desktop is listed as installed, but its app launch did not expose a targetable window in this review. The GitHub connector is available in the plugin directory but is not installed. No account was accessed, repository created, data uploaded, commit made or push attempted.

Start-menu inventory lists Autodesk Fusion, AutoCAD, KiCad, LTspice, Arduino IDE, VS Code, PyCharm, CLion, Docker Desktop and LM Studio. XFLR5 and JupyterLab did not appear in that inventory. The existing `agastya-python-3.12-clean` venv points to a missing Python 3.12 base executable. The installed Miniconda Python 3.14.10 runs the standard library and executed the Stage 2 model; scientific packages were not present in that interpreter. No software was installed or repaired.

The workspace includes a 1.37 GB cached EYE archive, other large raw datasets, generated virtual CSVs, a scratch `work/` tree, dependencies/build outputs, and outreach files that contain contact information. They require explicit filtering before any remote upload. See [repository preparation](GITHUB_REPOSITORY_PREPARATION_2026-11-19.md).

## Open engineering questions

1. Which actual panel sizes/constructions will Stage 2 accept, and what fixture/rail/tool arrangement reaches them?
2. What are the frame/box tool forces, masses, moments and cycle time on representative modules?
3. What is the foam roller's role, material, temperature range, line load, speed, wear and contamination behavior?
4. Can a modular liberation unit after Stage 3 provide clean, contained feed with measurable Ag retention and acceptable handling?
5. Does any actual feed contain a coarse liberated conductive fraction that warrants ECS?
6. Can a qualified lab accept the required prepared feed for flotation and downstream refining, and at what cost/limits?
7. What assay/receiver requirements establish a real mass balance and product specification?

## Claims and next evidence

No AGASTYA robot, foam roller, thermal process, silver-separation process, assay, recovery, purity, throughput, operating cost or profitability has been physically validated. The next useful evidence is measured feed geometry and composition, a qualified facility/supervisor, a cold Stage 2 fixture review, a fully specified foam roller, representative Stage 3 output, and paired mass-balanced Stage 4 tests.


