"""Build the curated file, migration, and NCSC print/build registers."""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = date(2026, 10, 11).isoformat()


def catalog(path: str, kind: str, purpose: str, status: str, authoritative: str,
            evidence: str, action: str, notes: str = "") -> dict[str, str]:
    return {
        "file_id": f"F{len(CATALOG) + 1:03d}", "filename": Path(path).name,
        "current_path": path, "file_type": kind, "purpose": purpose,
        "status": status, "authoritative_version": authoritative,
        "scientific_evidence_level": evidence, "last_verified": TODAY,
        "recommended_action": action, "notes": notes,
    }


CATALOG: list[dict[str, str]] = []
catalog_rows = [
    ("START_HERE.md", "Markdown", "Five-minute project entry point and navigation.", "AUTHORITATIVE", "Yes", "Project description and evidence boundaries", "Keep current; verify links after major edits.", ""),
    ("README.md", "Markdown", "Short root entry that directs the reader to START_HERE.", "AUTHORITATIVE", "Yes", "Project navigation", "Keep concise and link to START_HERE.", ""),
    ("AGASTYA_PROJECT_INDEX.md", "Markdown", "Navigable index of authoritative project records and preserved roots.", "AUTHORITATIVE", "Yes", "Project navigation; claims point to evidence", "Update when authoritative paths change.", ""),
    ("PROJECT_STATUS.md", "Markdown", "Current project dashboard and readiness state.", "AUTHORITATIVE", "Yes", "Status synthesis from saved files", "Update only when evidence or dependencies change.", ""),
    ("CHANGELOG.md", "Markdown", "Date-stamped record of completed project changes.", "AUTHORITATIVE", "Yes", "Administrative history", "Append completed and verified work only.", ""),
    ("00_Project_Management/PROJECT_UNDERSTANDING_AUDIT.md", "Markdown", "Plain-language audit of scope, evidence and missing work.", "AUTHORITATIVE", "Yes", "Literature and workspace audit; no physical experiment", "Review when new evidence arrives.", ""),
    ("00_Project_Management/MASTER_TASK_LIST.md", "Markdown", "Dependency-ordered actions for the student and guide.", "AUTHORITATIVE", "Yes", "Project-management plan", "Use the stated completion criteria; do not invent dates.", ""),
    ("00_Project_Management/TASK_TRACKER.csv", "CSV", "Compatibility pointer to the authoritative master task list.", "REFERENCE", "No", "Navigation only", "Use MASTER_TASK_LIST.md; do not maintain separate statuses.", "Previous tracker is archived."),
    ("00_Project_Management/MILESTONES.md", "Markdown", "Pointer to authoritative status dashboard and master tasks.", "REFERENCE", "No", "Navigation only", "Use PROJECT_STATUS.md and MASTER_TASK_LIST.md.", "Previous milestone table is archived."),
    ("00_Project_Management/OPEN_QUESTIONS.md", "Markdown", "Unresolved science, access and competition questions.", "AUTHORITATIVE", "Yes", "Known unknowns", "Close questions only with dated evidence.", ""),
    ("00_Project_Management/DECISIONS_LOG.md", "Markdown", "Decision history and scope decisions.", "AUTHORITATIVE", "Yes", "Administrative record", "Keep one decision log; singular-name pointer maintained for compatibility.", ""),
    ("00_Project_Management/MIGRATION_PLAN_2026-10-11.md", "Markdown", "Record of file moves and preservation approach.", "REFERENCE", "No", "Administrative record", "Compare with generated migration CSV.", ""),
    ("00_Project_Management/REPAIR_LOG.md", "Markdown", "Repairs made and the checks performed.", "AUTHORITATIVE", "Yes", "QA record", "Append only actions actually completed.", ""),
    ("00_Project_Management/DUPLICATE_AND_CLEANUP_REPORT.md", "Markdown", "Duplicate scan findings and preservation decisions.", "AUTHORITATIVE", "Yes", "Hash scan of curated document/code files", "No deletion is authorized by a near-match alone.", "Image collections and dependency trees were not content-hash compared."),
    ("00_Project_Management/FINAL_CONSISTENCY_AUDIT_2026-10-11.md", "Markdown", "Evidence, computation, presentation and safety audit.", "AUTHORITATIVE", "Yes", "Desk review and executed arithmetic tests", "Append follow-up checks; visual rendering remains a human review.", ""),
    ("00_Project_Management/FILE_CATALOG.csv", "CSV", "Curated catalog of significant files and their status.", "AUTHORITATIVE", "Yes", "Document-level audit; not a claim that every dataset byte was reviewed", "Regenerate with build_workspace_registers.py after major changes.", "Catalog covers high-value project records; file_inventory.csv covers all enumerated paths."),
    ("00_Project_Management/FILE_MIGRATION_LOG.csv", "CSV", "Source-to-destination migration record.", "AUTHORITATIVE", "Yes", "Migration plan and destination checks", "Update for future file moves.", ""),
    ("00_Project_Management/file_inventory.csv", "CSV", "Recursive path inventory of the workspace.", "REFERENCE", "No", "Filesystem listing; not content verification", "Regenerate if the tree changes materially.", ""),
    ("00_Project_Management/file_inventory_summary.md", "Markdown", "Summary of the recursive file inventory.", "REFERENCE", "No", "Filesystem listing", "Regenerate with inventory if stale.", ""),
    ("01_Research/RESEARCH_OVERVIEW.md", "Markdown", "Student-readable summary of the problem, evidence and limits.", "AUTHORITATIVE", "Yes", "Source-qualified synthesis", "Review each claim against the register before external submission.", ""),
    ("01_Research/03_Source_Evidence/SOURCE_EVIDENCE_REGISTER.csv", "CSV", "Claims-to-source register with methods and limitations.", "AUTHORITATIVE", "Yes", "Primary/review literature; source-level verification status recorded", "Resolve flagged 300 ppm and 600/630 g/t source bases.", ""),
    ("01_Research/Literature_Review/AGASTYA_EVIDENCE_REVIEW_2026-10-11.md", "Markdown", "Detailed source synthesis and route comparison.", "REFERENCE", "No", "Literature review", "Use the source register for claim boundaries.", ""),
    ("Build Files and Steps/Stage 4/STAGE4_LITERATURE_REVIEW.md", "Markdown", "Historical thesis Stage 4 eddy-current literature review.", "REQUIRES_REVIEW", "No", "Desk review; no AGASTYA build or test", "Use with the legacy-numbering warning; reconcile future stage references.", "Its thesis-stage numbering differs from the current charter."),
    ("02_Engineering/ENGINEERING_OVERVIEW.md", "Markdown", "Current process architecture, interfaces and design gaps.", "AUTHORITATIVE", "Yes", "Conceptual engineering; no validated prototype", "Keep every proposed component labelled as proposed.", ""),
    ("Agastya Physics Simulation/Research Baseline/AGASTYA_PHASE_A_BASELINE_2026-10-10.md", "Markdown", "Baseline literature and model plan for stages and thermal work.", "REFERENCE", "No", "Literature and equations; no physical test", "Preserve as historical baseline and use corrected source distinctions.", ""),
    ("Agastya Physics Simulation/Research Baseline/PHASE_B_ACCOUNTING_MODEL.md", "Markdown", "Historical Phase B accounting run description.", "SUPERSEDED", "No", "Normalized literature arithmetic only", "Use v3 interpretation; retain the v2 file for traceability.", ""),
    ("Agastya Physics Simulation/Research Baseline/preliminary_material_inventory.csv", "CSV", "Published composition scenario with an unassigned remainder.", "REFERENCE", "No", "Secondary-source normalized composition scenario", "Do not call it an AGASTYA bill of materials or measurement.", ""),
    ("Agastya Physics Simulation/Research Baseline/AGASTYA_PHASE_A_BASELINE_2026-10-10.md", "Markdown", "Phase A research baseline and model/solver limitations.", "REFERENCE", "No", "Literature synthesis and proposed model equations", "Use with the current source corrections and architecture crosswalk.", ""),
    ("Agastya Physics Simulation/Research Baseline/ARCHITECTURE_CROSSWALK_2026-10-10.md", "Markdown", "Maps current charter stages to older thesis/simulation numbering.", "AUTHORITATIVE", "Yes", "Project architecture mapping", "Include when interpreting historical simulation rows.", ""),
    ("Agastya Physics Simulation/Agastya_Physics_Simulation_2026-10-10.csv", "CSV", "Initial virtual scenario and thermal model output.", "REFERENCE", "No", "147,912 virtual rows; not physical observations or replicates", "Keep with its data dictionary, script and metadata; do not call rows samples.", "Large historical model output."),
    ("Agastya Physics Simulation/followup_virtual_experiments.csv", "CSV", "Follow-up virtual model/time-history output.", "REFERENCE", "No", "52,168 virtual rows; not physical observations or replicates", "Keep with its script and procedure documentation.", ""),
    ("Agastya Physics Simulation/Agastya_Physics_Simulation_2026-10-10_metadata.json", "JSON", "Manifest for the initial virtual model output.", "REFERENCE", "No", "Run metadata and assumptions", "Retain next to the CSV and script.", ""),
    ("Agastya Physics Simulation/experiment_register.csv", "CSV", "Procedure and run register for legacy virtual work.", "REFERENCE", "No", "Virtual scenarios/time histories", "Read each evidence class and specimen count field carefully.", ""),
    ("Agastya Physics Simulation/data_dictionary.csv", "CSV", "Field definitions and units for legacy model output.", "REFERENCE", "No", "Model output schema", "Keep with the virtual datasets.", ""),
    ("Agastya Physics Simulation/REAL_TEST_READINESS.md", "Markdown", "Readiness gaps for any supervised future physical trial.", "REFERENCE", "No", "Planning only; no approval/access asserted", "Use as a gate list, not as evidence of facility access.", ""),
    ("Agastya Physics Simulation/PROCEDURES_AND_RESULTS.md", "Markdown", "Historical thermal and virtual scenario/time-history procedure record.", "REFERENCE", "No", "Software model outputs, not physical observations", "Keep virtual rows distinct from samples and replicates.", ""),
    ("Agastya Physics Simulation/Research Phase B-C/evidence_database_v2.csv", "CSV", "Detailed source database for Phase B/C analysis.", "REFERENCE", "No", "Literature records with per-source boundaries", "Use v3 source-qualified outputs and register for current summary.", ""),
    ("Agastya Physics Simulation/Research Phase B-C/published_data_validation_v3.csv", "CSV", "Reproduced rounded-mean diagnostics and qualified 300/600/630 arithmetic.", "AUTHORITATIVE", "Yes", "Executed arithmetic from cited literature; no AGASTYA sample data", "Keep study denominators and unresolved source discrepancy visible.", ""),
    ("Agastya Physics Simulation/Research Phase B-C/published_data_reproduction_v3.py", "Python", "Reproduces v3 source-qualified literature arithmetic.", "AUTHORITATIVE", "Yes", "Executed with CPython standard library", "Run from its directory to regenerate the v3 validation CSV.", ""),
    ("Agastya Physics Simulation/Research Phase B-C/scenario_results_v3.csv", "CSV", "Three 1 kg normalized literature arithmetic records; process outputs blank.", "AUTHORITATIVE", "Yes", "Executed source-qualified arithmetic; not a process simulation", "Never fill process values without measured streams and assays.", "Physical sample count is 0."),
    ("Agastya Physics Simulation/Research Phase B-C/scenario_model_run_v3.json", "JSON", "Run manifest for the v3 normalized arithmetic output.", "AUTHORITATIVE", "Yes", "Execution metadata and declared limitations", "Retain with its script and CSV.", ""),
    ("Agastya Physics Simulation/Research Phase B-C/agastya_scenario_model_v3.py", "Python", "Generates source-qualified reference rows with blank stage outcomes.", "AUTHORITATIVE", "Yes", "Executed with CPython standard library", "Run from its directory; inspect input provenance before re-use.", "This is not a physics, chemistry or separator solver."),
    ("Agastya Physics Simulation/Research Phase B-C/scenario_results_v2.csv", "CSV", "Prior two-case normalized arithmetic output.", "SUPERSEDED", "No", "Historical normalized arithmetic", "Retain for audit; use v3 for current cited values.", ""),
    ("Agastya Physics Simulation/Research Phase B-C/accounting_unit_tests_v2.py", "Python", "Unit tests for accounting conversions and validation.", "AUTHORITATIVE", "Yes", "Executed unit suite, 28/28 pass", "Run after code changes.", ""),
    ("Agastya Physics Simulation/Research Phase B-C/validate_accounting_kernel_v2.py", "Python", "Legacy Phase A input-validation probe runner.", "REFERENCE", "No", "Executed 25 probes; 22 pass, 3 known failures", "Keep the limitations visible; do not use as the validated v2 kernel.", "Three failure probes document rejected inputs the legacy kernel does not guard."),
    ("03_Data_and_Analysis/DATA_AND_ANALYSIS_GUIDE.md", "Markdown", "Where calculations live and how to reproduce v3 arithmetic.", "AUTHORITATIVE", "Yes", "Reproducibility guide for saved scripts/outputs", "Update links when outputs change.", ""),
    ("04_Logbook/Logbook_Index.md", "Markdown", "Index of historical and reconstructed digital notes.", "AUTHORITATIVE", "Yes", "Available digital records; date/provenance qualifiers retained", "The student must maintain the real-time original handwritten notebook.", "No missing activities, dates or signatures should be backfilled."),
    ("05_Presentation/PRESENTATION_GUIDE.md", "Markdown", "Authoritative deck choice and review requirements.", "AUTHORITATIVE", "Yes", "Generated presentation plus structural checks", "Student/teacher must visually review on actual presentation hardware.", ""),
    ("05_Presentation/Final_Presentation/AGASTYA_MASTER_PRESENTATION_2026-10-11.pptx", "PPTX", "Current 19-slide overview of the full AGASTYA project.", "REQUIRES_REVIEW", "Yes", "19 slides with notes; EYE, process, thermal and model-row summary, literature evidence and validation plan", "Confirm timing and rules; review the render on the actual presentation computer.", "Two credited Wikimedia Commons photos are explicitly illustrative, not AGASTYA evidence."),
    ("05_Presentation/Final_Presentation/AGASTYA_NCSC_SHORT_PRESENTATION_2026-10-11.pptx", "PPTX", "15-slide concise overview for adaptation to the event format.", "REQUIRES_REVIEW", "Yes", "15 slides with notes; one attributed illustrative cover photo", "Confirm speaking time and review with student/teacher.", ""),
    ("05_Presentation/Presentation_Script/AGASTYA_PRESENTATION_SPEAKER_NOTES.md", "Markdown", "Speaker notes for the generated decks.", "AUTHORITATIVE", "Yes", "Claim boundaries mirrored from slide evidence", "Student should verify they can explain each point.", ""),
    ("05_Presentation/Final_Presentation/AGASTYA_SLIDE_EVIDENCE_REGISTER.csv", "CSV", "Slide-by-slide source and limitation mapping.", "AUTHORITATIVE", "Yes", "Claims mapped to listed sources", "Keep synchronized with slide edits.", ""),
    ("05_Presentation/Final_Presentation/AGASTYA_VISUAL_ASSET_REGISTER.csv", "CSV", "Slide-by-slide visual and image provenance register.", "AUTHORITATIVE", "Yes", "PowerPoint-native conceptual diagrams and attribution records", "Keep synchronized with slide edits.", ""),
    ("07_Visual_Assets/VISUAL_ASSET_REGISTER.csv", "CSV", "External image attribution, license and claim-boundary register.", "AUTHORITATIVE", "Yes", "Two Wikimedia Commons image pages and CC BY-SA 4.0 terms checked.", "Preserve source and license credits wherever the images are reused.", "Images are illustrative only."),
    ("07_Visual_Assets/01_Original_Photographs/PV_Panel_Fomanu_2015.jpg", "JPEG", "Illustrative external photograph used on the presentation cover.", "REFERENCE", "No", "Wikimedia Commons; Fomanu; CC BY-SA 4.0", "Use only with attribution and illustrative-image label.", "Not an AGASTYA panel or apparatus."),
    ("07_Visual_Assets/01_Original_Photographs/Silicon_Solar_Cells_Fdenicola_2013.jpg", "JPEG", "Illustrative external close-up used in the problem slide.", "REFERENCE", "No", "Wikimedia Commons; Fdenicola; CC BY-SA 4.0", "Use only with attribution and illustrative-image label.", "Not an AGASTYA sample or assay."),
    ("printables/README.md", "Markdown", "Explains all generated print layouts and their current approval status.", "AUTHORITATIVE", "Yes", "Eight one-page A1/A4 working layouts; no event specification confirmed", "Check the NCSC preparation guide and print/build register before printing.", ""),
    ("05_Presentation/Existing_Presentations/Agastya_Presentation.pptx", "PPTX", "Original 11-slide presentation retained as historical source.", "ARCHIVED", "No", "Historical student/author content; claims need review before reuse", "Do not use as current final; preserve unchanged.", ""),
    ("05_Presentation/Existing_Presentations/Agastya_Presentation_Enhanced.pptx", "PPTX", "Original enhanced presentation retained as historical source.", "ARCHIVED", "No", "Historical content and embedded visuals; asset review required", "Do not use as current final; preserve unchanged.", ""),
    ("05_Presentation/Working_Drafts/Presentation_QA/EXISTING_PRESENTATION_REVIEW.md", "Markdown", "Review of original decks and known evidence/asset issues.", "REFERENCE", "No", "Desk and structural review", "Use when deciding whether any original material can be reused.", ""),
    ("06_NCSC_Display/NCSC_PREPARATION_GUIDE.md", "Markdown", "Decision guide for printing, building, digital materials and unknown rules.", "AUTHORITATIVE", "Yes", "DST draft guidebook and local requirements unresolved", "Ask the local coordinator; update when a dated final rule arrives.", ""),
    ("06_NCSC_Display/PRINTED_MATERIALS_AND_DISPLAY_PLAN.md", "Markdown", "Compatibility pointer to the authoritative NCSC print/build guide.", "REFERENCE", "No", "Navigation only", "Use NCSC_PREPARATION_GUIDE.md and the CSV register.", "Superseded full plan preserved in the archive."),
    ("06_NCSC_Display/DISPLAY_IDEAS_AND_DEMONSTRATIONS.md", "Markdown", "Compatibility pointer to current safe display recommendation.", "REFERENCE", "No", "Navigation only", "Use NCSC_PREPARATION_GUIDE.md and the CSV register.", "Superseded brainstorm preserved in the archive."),
    ("06_NCSC_Display/PRINT_AND_BUILD_REGISTER.csv", "CSV", "Decision register for print/build/digital deliverables.", "AUTHORITATIVE", "Yes", "Output dimensions checked; competition specifications unknown", "Do not print WAIT/CONFIRM rows until prerequisites are met.", ""),
    ("06_NCSC_Display/Official_Requirements/NCSC_COMPLIANCE_CHECKLIST.md", "Markdown", "Official-source and local-rule compliance checklist.", "REQUIRES_REVIEW", "No", "DST activity guidebook listed as draft; local event unknown", "Confirm exact level, category and current rules.", ""),
    ("printables/AGASTYA_A4_Project_Summary.pdf", "PDF", "Optional one-page project summary layout.", "REQUIRES_REVIEW", "No", "Generated display layout, not an event rule", "Review latest source corrections and local size/content rules.", "Not authorized for printing by the current evidence."),
    ("printables/AGASTYA_A4_Architecture.pdf", "PDF", "Optional architecture display layout.", "REQUIRES_REVIEW", "No", "Proposed process architecture", "Check current stage labels and event requirements.", "Not an image of a working prototype."),
    ("printables/AGASTYA_A4_Evidence_and_Results.pdf", "PDF", "Optional evidence sheet layout.", "REQUIRES_REVIEW", "No", "Literature and calculation claims", "Student/teacher proof at intended print size and confirm local event rules.", "Regenerated with corrected source labels and visually previewed; not authorized to print until approval."),
    ("printables/AGASTYA_A4_Attribution_and_Sources.pdf", "PDF", "Optional source attribution sheet.", "REQUIRES_REVIEW", "No", "Bibliographic references", "Check citations against current source register before use.", ""),
    ("printables/AGASTYA_Poster_01_Problem_and_Question_A1.pdf", "PDF", "Working A1 problem/question poster layout.", "REQUIRES_REVIEW", "No", "Research framing", "Confirm local requirements and visually proof after final changes.", "A1 is the generated page size, not a verified competition requirement."),
    ("printables/AGASTYA_Poster_02_Architecture_A1.pdf", "PDF", "Working A1 architecture poster layout.", "REQUIRES_REVIEW", "No", "Conceptual architecture", "Confirm stage mapping, dimensions and local rules before printing.", "A1 is the generated page size, not a verified competition requirement."),
    ("printables/AGASTYA_Poster_03_Evidence_and_Findings_A1.pdf", "PDF", "Working A1 evidence poster layout.", "REQUIRES_REVIEW", "No", "Literature evidence; not an AGASTYA result", "Student/teacher proof at intended print size and confirm event rules.", "Regenerated with current source limits and visually previewed; not an AGASTYA result."),
    ("printables/AGASTYA_Poster_04_Conclusion_and_Next_Steps_A1.pdf", "PDF", "Working A1 conclusion/next-steps poster layout.", "REQUIRES_REVIEW", "No", "Limitations and proposed research", "Confirm local rules and visually proof after final changes.", ""),
    ("09_Software_and_Environment/SOFTWARE_INVENTORY.md", "Markdown", "Tools actually used versus researched or not run.", "AUTHORITATIVE", "Yes", "Environment inspection and execution records", "Update after tool runs; distinguish intended tools from executed tools.", ""),
    ("09_Software_and_Environment/ENVIRONMENT_SETUP.md", "Markdown", "Local runtime and known software setup.", "REFERENCE", "No", "Runtime-specific procedure", "Retain exact environment and dependency notes.", ""),
    ("09_Software_and_Environment/REPRODUCIBILITY_GUIDE.md", "Markdown", "Commands and caveats for reproducing calculations and outputs.", "AUTHORITATIVE", "Yes", "Executed Python/Node actions and run outputs", "Keep scripts, inputs, outputs and versions together.", ""),
    ("Agastya-EYE/README.md", "Markdown", "Application, image dataset and model evidence overview.", "REFERENCE", "No", "Software/demo and image-model records; not a silver assay", "Keep evaluation boundaries and dataset provenance with any reuse.", ""),
    ("Agastya-EYE/app.py", "Python", "Inspection/passport application source.", "REFERENCE", "No", "Advisory software; no material recovery measurement", "Do not describe visual classification as elemental assay.", ""),
    ("Agastya Simulation/README.md", "Markdown", "Browser walkthrough and Wokwi monitor mock-up description.", "REFERENCE", "No", "UI/demo only; not process physics", "Use only as a conceptual software demonstration.", ""),
    ("Agastya Thermal/README.md", "Markdown", "Thermal monitoring and build-note overview.", "REFERENCE", "No", "Conceptual hardware/model notes", "Do not claim built/tested equipment without evidence.", ""),
    ("Build Files and Steps/Stage 3/STAGE3_BUILD_PLAN.md", "Markdown", "Legacy Stage 3 thermal/build proposal.", "REFERENCE", "No", "Conceptual proposal; not a completed prototype", "Use only with current architecture crosswalk.", ""),
    ("Build Files and Steps/Stage 4/STAGE4_READINESS_AUDIT_2026-10-06.md", "Markdown", "Historical readiness assessment for the previous Stage 4 design.", "REFERENCE", "No", "Research/readiness review, no hardware trial", "Use the legacy-numbering notice in Stage 4 literature review.", ""),
    ("99_Archive/ARCHIVE_INDEX.md", "Markdown", "Explains retained historical files and rollback snapshots.", "AUTHORITATIVE", "Yes", "Archive record", "Add entries before future archive moves.", ""),
    ("99_Archive/Pre_cleanup_snapshot_2026-10-11.zip", "ZIP", "Verified rollback copy of curated documents/code before current repairs.", "RAW_EVIDENCE", "Yes", "150 entries SHA-256 checked against source files", "Retain unchanged until project owner approves archive lifecycle.", "Does not include bulk images, datasets or dependencies."),
    ("99_Archive/Pre_claim_repair_deliverables_2026-10-11.zip", "ZIP", "Verified pre-repair copy of presentation/display deliverables.", "RAW_EVIDENCE", "Yes", "18 entries SHA-256 checked against source files", "Retain unchanged until project owner approves archive lifecycle.", ""),
    ("Agastya-EYE/datasets/", "Folder", "Existing image-model data hierarchy.", "RAW_EVIDENCE", "No", "Dataset files and manifests exist; not every image reviewed in this audit", "Preserve; use the dataset README/manifests for individual records.", "Bulk dataset was not rehashed or reorganized."),
]
for item in catalog_rows:
    CATALOG.append(catalog(item[0], *item[1:]))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


CATALOG_PATH = ROOT / "00_Project_Management/FILE_CATALOG.csv"
write_csv(CATALOG_PATH, ["file_id", "filename", "current_path", "file_type", "purpose", "status", "authoritative_version", "scientific_evidence_level", "last_verified", "recommended_action", "notes"], CATALOG)

MIGRATION_FIELDS = ["migration_id", "date", "original_path", "current_path", "action", "reason", "verification", "rollback_or_preservation", "notes"]
migration: list[dict[str, str]] = []


def moved(source: str, destination: str, reason: str, verification: str, preservation: str, notes: str = "") -> None:
    migration.append({
        "migration_id": f"M{len(migration)+1:03d}", "date": TODAY,
        "original_path": source, "current_path": destination, "action": "MOVED",
        "reason": reason, "verification": verification,
        "rollback_or_preservation": preservation, "notes": notes,
    })


for item in sorted((ROOT / "04_Logbook").rglob("*")):
    if not item.is_file():
        continue
    rel = item.relative_to(ROOT / "04_Logbook").as_posix()
    if rel == "Logbook_Index.md" or rel.startswith("Day_01_to_05/"):
        continue
    moved(f"Logbook/{rel}", f"04_Logbook/{rel}", "Consolidate original logbook records while preserving relative paths.", "Destination exists; index distinguishes original records from later summaries.", "Pre-cleanup snapshot retained; no source deleted.", "Original source tree was removed after the earlier migration; original path is based on the recorded migration plan.")

for source, destination, reason in [
    ("Agastya_Presentation.pptx", "05_Presentation/Existing_Presentations/Agastya_Presentation.pptx", "Preserve the original deck and separate it from the current deck."),
    ("Agastya_Presentation_Enhanced.pptx", "05_Presentation/Existing_Presentations/Agastya_Presentation_Enhanced.pptx", "Preserve the prior enhanced deck."),
    ("Agastya_Thesis.docx", "08_Reports/Technical_Reports/Agastya_Thesis.docx", "Keep the source thesis as a historical document."),
    ("Agastya_Abstract.docx", "08_Reports/Abstracts/Agastya_Abstract.docx", "Keep the original abstract separately from future submissions."),
]:
    moved(source, destination, reason, "Destination exists and file is linked in the project index/catalog.", "Pre-cleanup snapshot retained; no source deleted.")

for filename in [
    "Agastya_3D_Cardboard_Model.svg", "Agastya_Cardboard_Prototype_3D.svg",
    "Agastya_Concept_Model_Diagram.svg", "Agastya_Cutaway_3D_Concept.svg",
    "Agastya_Structural_Model_Diagram.svg", "Agastya_Structure_Simple_Guide.svg",
]:
    moved(filename, f"07_Visual_Assets/Conceptual_Illustrations/{filename}", "Separate conceptual drawings from evidence photographs.", "Destination exists; asset catalogue identifies these as conceptual visuals.", "Pre-cleanup snapshot retained; no source deleted.")

for filename in [".build_agastya_enhanced.js", ".inspect_agastya_temp.py", ".render_agastya_temp.ps1", ".validate_agastya_temp.py"]:
    moved(filename, f"05_Presentation/Working_Drafts/Build_Utilities/{filename}", "Group hidden presentation build/inspection utilities with presentation work.", "Destination exists; original output remains available through the presentation folder.", "Pre-cleanup snapshot retained; no source deleted.")

moved("06_NCSC_Display/Working_Layouts/AGASTYA_A4_Architecture.pdf", "printables/AGASTYA_A4_Architecture.pdf", "Keep every generated print layout together in the requested project-root folder.", "Destination PDF retained and poster generator/validator now target printables/.", "Pre-cleanup snapshot retained; source move is reversible.")
moved("06_NCSC_Display/Working_Layouts/AGASTYA_A4_Attribution_and_Sources.pdf", "printables/AGASTYA_A4_Attribution_and_Sources.pdf", "Keep every generated print layout together in the requested project-root folder.", "Destination PDF retained and poster generator/validator now target printables/.", "Pre-cleanup snapshot retained; source move is reversible.")
moved("06_NCSC_Display/Working_Layouts/AGASTYA_A4_Evidence_and_Results.pdf", "printables/AGASTYA_A4_Evidence_and_Results.pdf", "Keep every generated print layout together in the requested project-root folder.", "Destination PDF retained and poster generator/validator now target printables/.", "Pre-cleanup snapshot retained; source move is reversible.")
moved("06_NCSC_Display/Working_Layouts/AGASTYA_A4_Project_Summary.pdf", "printables/AGASTYA_A4_Project_Summary.pdf", "Keep every generated print layout together in the requested project-root folder.", "Destination PDF retained and poster generator/validator now target printables/.", "Pre-cleanup snapshot retained; source move is reversible.")
moved("06_NCSC_Display/Working_Layouts/AGASTYA_Poster_01_Problem_and_Question_A1.pdf", "printables/AGASTYA_Poster_01_Problem_and_Question_A1.pdf", "Keep every generated print layout together in the requested project-root folder.", "Destination PDF retained and poster generator/validator now target printables/.", "Pre-cleanup snapshot retained; source move is reversible.")
moved("06_NCSC_Display/Working_Layouts/AGASTYA_Poster_02_Architecture_A1.pdf", "printables/AGASTYA_Poster_02_Architecture_A1.pdf", "Keep every generated print layout together in the requested project-root folder.", "Destination PDF retained and poster generator/validator now target printables/.", "Pre-cleanup snapshot retained; source move is reversible.")
moved("06_NCSC_Display/Working_Layouts/AGASTYA_Poster_03_Evidence_and_Findings_A1.pdf", "printables/AGASTYA_Poster_03_Evidence_and_Findings_A1.pdf", "Keep every generated print layout together in the requested project-root folder.", "Destination PDF retained and poster generator/validator now target printables/.", "Pre-cleanup snapshot retained; source move is reversible.")
moved("06_NCSC_Display/Working_Layouts/AGASTYA_Poster_04_Conclusion_and_Next_Steps_A1.pdf", "printables/AGASTYA_Poster_04_Conclusion_and_Next_Steps_A1.pdf", "Keep every generated print layout together in the requested project-root folder.", "Destination PDF retained and poster generator/validator now target printables/.", "Pre-cleanup snapshot retained; source move is reversible.")
moved("00_Project_Management/PROJECT_STATUS.md", "PROJECT_STATUS.md", "Make the current status dashboard visible at the root.", "Root dashboard exists and is linked from START_HERE.", "Pre-cleanup snapshot retained; pointer will remain at old path.")
moved("00_Project_Management/CHANGELOG.md", "CHANGELOG.md", "Make the change log visible at the root.", "Root changelog exists and is linked from START_HERE.", "Pre-cleanup snapshot retained; pointer will remain at old path.")
moved("PROJECT_UNDERSTANDING_AUDIT.md", "00_Project_Management/PROJECT_UNDERSTANDING_AUDIT.md", "Put the requested audit in project management and keep the root path as a pointer.", "Current audit path exists; the root pointer links to it.", "Original audit preserved in Superseded_Documents and in the pre-cleanup snapshot.")
moved("00_Project_Management/PROJECT_UNDERSTANDING_AUDIT.md", "99_Archive/Superseded_Documents/PROJECT_UNDERSTANDING_AUDIT_PRE_CLEANUP_2026-10-11.md", "Retain the earlier stale audit as history while replacing it with the current verified audit.", "Archive entry exists and is listed in ARCHIVE_INDEX.md.", "Pre-cleanup snapshot also preserves the earlier file.", "This path records the earlier version before replacement.")
moved("06_NCSC_Display/PRINTED_MATERIALS_AND_DISPLAY_PLAN.md", "99_Archive/Superseded_Documents/PRINTED_MATERIALS_AND_DISPLAY_PLAN_2026-10-11.md", "Consolidate print/build decisions in the current NCSC guide and register.", "Archived copy exists; old path now points to the authoritative guide.", "Archived dated original and pre-cleanup snapshot retained.")
moved("06_NCSC_Display/DISPLAY_IDEAS_AND_DEMONSTRATIONS.md", "99_Archive/Superseded_Documents/DISPLAY_IDEAS_AND_DEMONSTRATIONS_2026-10-11.md", "Remove duplicated brainstorm from the active guidance path.", "Archived copy exists; old path now points to the current guide.", "Archived dated original and pre-cleanup snapshot retained.")
moved("00_Project_Management/TASK_TRACKER.csv", "99_Archive/Superseded_Documents/TASK_TRACKER_2026-10-11_PRE_STATUS_REFRESH.csv", "Preserve the old tracker while consolidating current task status in the master task list.", "Archived copy exists; original path now contains a pointer row.", "Archived dated original and pre-cleanup snapshot retained.")
moved("00_Project_Management/MILESTONES.md", "99_Archive/Superseded_Documents/MILESTONES_2026-10-11_PRE_STATUS_REFRESH.md", "Preserve the earlier milestone table while consolidating current status in the dashboard.", "Archived copy exists; original path now contains a pointer.", "Archived dated original and pre-cleanup snapshot retained.")
write_csv(ROOT / "00_Project_Management/FILE_MIGRATION_LOG.csv", MIGRATION_FIELDS, migration)

PRINT_FIELDS = [
    "item_id", "item_name", "category", "purpose", "mandatory_or_optional", "source_file",
    "output_file", "physical_or_digital", "format", "dimensions", "copies_required",
    "estimated_cost", "estimated_effort", "prerequisites", "verification_status",
    "print_ready", "build_required", "priority", "final_decision", "notes",
]
PRINT = [
    ["NCSC-01", "Officially required forms, report or display", "Requirements to confirm", "Meet the specific local event rules.", "UNKNOWN", "Current local organizer instructions", "UNKNOWN", "PHYSICAL OR DIGITAL UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN", "Unknown until rules arrive", "Confirm event level, category and current dated rules.", "NOT VERIFIED; DST 2026–27 activity guidebook is listed as draft.", "NO", "UNKNOWN", "P0", "CONFIRM_WITH_ORGANISER", "No item can be called mandatory until the actual event requirements are known."],
    ["NCSC-02", "Original student project notebook", "Must maintain", "Contemporaneous student record; not a newly printed reconstruction.", "Guidebook advice; confirm local rules", "Student's actual bound handwritten notebook", "No generated output", "PHYSICAL", "Handwritten bound notebook", "UNKNOWN", "1 per student/team as locally directed", "UNKNOWN", "Ongoing", "Student and guide use it for genuine dated observations; do not backfill.", "DST draft guidebook says real-time handwritten notebook; local status unresolved.", "NOT APPLICABLE", "NO", "P0", "CONFIRM_WITH_ORGANISER", "Do not print digital summaries as a substitute for the original book."],
    ["PRINT-01", "A4 project summary", "Should print if useful", "One-page orientation for a visitor.", "Optional", "printables/AGASTYA_A4_Project_Summary.pdf", "Same PDF", "PHYSICAL", "PDF", "A4 (generated)", "UNKNOWN", "UNKNOWN", "Low", "Confirm event rules; update any claims; proof at 100%.", "Page size generated; local suitability and final content need review.", "NO", "NO", "P2", "OPTIONAL", "Print only if it serves a distinct purpose and is allowed."],
    ["PRINT-02", "A4 architecture sheet", "Should print if useful", "Explain the proposed four-stage process in one view.", "Optional", "printables/AGASTYA_A4_Architecture.pdf", "Same PDF", "PHYSICAL", "PDF", "A4 (generated)", "UNKNOWN", "UNKNOWN", "Low", "Confirm current stage labels and event rules; proof at 100%.", "Page size generated; concept status must remain visible.", "NO", "NO", "P2", "OPTIONAL", "Use only if the display needs more than one diagram."],
    ["PRINT-03", "A4 evidence and results sheet", "Wait for final human approval", "Summarize only source-specific findings and AGASTYA work completed.", "Optional", "printables/AGASTYA_A4_Evidence_and_Results.pdf", "Same regenerated PDF", "PHYSICAL", "PDF", "A4 (generated)", "UNKNOWN", "UNKNOWN", "Low", "Student/teacher proof at intended print size; confirm event rules.", "Source-corrected PDF visually previewed; final proof and event approval outstanding.", "NO", "NO", "P1", "WAIT", "There are no AGASTYA recovery or assay results to chart."],
    ["PRINT-04", "A4 attribution and sources sheet", "Should print if useful", "Make source attribution accessible beside an approved display.", "Optional", "printables/AGASTYA_A4_Attribution_and_Sources.pdf", "Same PDF after citation check", "PHYSICAL", "PDF", "A4 (generated)", "UNKNOWN", "UNKNOWN", "Low", "Check citations against source register and coordinator display rules.", "Generated page size; citations require current review.", "NO", "NO", "P2", "OPTIONAL", "Avoid printing if it duplicates a required bibliography elsewhere."],
    ["PRINT-05", "A1 problem and question poster", "Wait for event rules", "Introduce the problem and research question.", "Optional until confirmed", "printables/AGASTYA_Poster_01_Problem_and_Question_A1.pdf", "Same PDF after proof", "PHYSICAL", "PDF", "A1 portrait (generated, not official requirement)", "UNKNOWN", "UNKNOWN", "Medium", "Confirm poster count, dimensions, mounting, and current content.", "Generated PDF; event size/count and final proof not confirmed.", "NO", "NO", "P1", "WAIT", "Do not order based on generated A1 size alone."],
    ["PRINT-06", "A1 architecture poster", "Wait for event rules", "Show proposed stages and process boundaries.", "Optional until confirmed", "printables/AGASTYA_Poster_02_Architecture_A1.pdf", "Same PDF after proof", "PHYSICAL", "PDF", "A1 portrait (generated, not official requirement)", "UNKNOWN", "UNKNOWN", "Medium", "Confirm stage mapping, display rules and final proof.", "Generated PDF; event size/count and final proof not confirmed.", "NO", "NO", "P1", "WAIT", "Conceptual design only; not evidence of a working machine."],
    ["PRINT-07", "A1 evidence and findings poster", "Wait for final human approval", "Explain literature evidence and actual project status.", "Optional until confirmed", "printables/AGASTYA_Poster_03_Evidence_and_Findings_A1.pdf", "Same regenerated PDF", "PHYSICAL", "PDF", "A1 portrait (generated, not official requirement)", "UNKNOWN", "UNKNOWN", "Medium", "Student/teacher proof at intended print size; confirm size/count and local rules.", "Source-corrected PDF visually previewed; event size/count and final proof outstanding.", "NO", "NO", "P1", "WAIT", "Must not show literature values as AGASTYA measurements."],
    ["PRINT-08", "A1 conclusion and next steps poster", "Wait for event rules", "State limitations and the next validation gates.", "Optional until confirmed", "printables/AGASTYA_Poster_04_Conclusion_and_Next_Steps_A1.pdf", "Same PDF after proof", "PHYSICAL", "PDF", "A1 portrait (generated, not official requirement)", "UNKNOWN", "UNKNOWN", "Medium", "Confirm local rules and visually proof after final content.", "Generated PDF; event size/count and final proof not confirmed.", "NO", "NO", "P1", "WAIT", ""],
    ["DIGITAL-01", "Master and short presentations", "Digital only", "Explain the proposal, literature evidence, results status and limitations.", "Optional unless required", "05_Presentation/Final_Presentation/AGASTYA_MASTER_PRESENTATION_2026-10-11.pptx", "Master and short PPTX", "DIGITAL", "PPTX", "16:9 widescreen", "Not applicable", "No printing cost", "Medium", "Visually review; confirm time and event rules.", "Structural check passed; visual rendering not checked.", "NO", "NO", "P1", "DIGITAL_ONLY", "Carry files on the approved device and a permitted backup."],
    ["DIGITAL-02", "Source register, detailed calculations, scripts and raw/virtual data", "Digital only", "Maintain traceability and reproducibility without display clutter.", "Not a display print item", "01_Research/03_Source_Evidence/SOURCE_EVIDENCE_REGISTER.csv; Agastya Physics Simulation/Research Phase B-C/", "Existing source/data files", "DIGITAL", "CSV/JSON/Python/Markdown", "Not applicable", "Not applicable", "No printing cost", "Ongoing", "Keep scripts with inputs and outputs; back up project data.", "Files exist; historical virtual records are not physical samples.", "NOT APPLICABLE", "NO", "P2", "DIGITAL_ONLY", "Do not print large datasets or detailed code."],
    ["BUILD-01", "Paper-token material-flow board", "Physical display if useful", "Demonstrate stream IDs and accounting logic safely.", "Optional", "03_Data_and_Analysis/DATA_AND_ANALYSIS_GUIDE.md", "Student-made paper/card tokens", "PHYSICAL", "Paper/card, marker, reusable tokens", "Tabletop size to suit venue", "1", "UNKNOWN", "45–90 min", "Confirm venue rules; label 'accounting demonstration only'.", "Not built; plan only.", "NOT APPLICABLE", "YES", "P3", "OPTIONAL", "Shows material-flow bookkeeping only; does not demonstrate separation or silver recovery. No chemical or electrical materials."],
    ["BUILD-02", "Working high-voltage/electrostatic separator", "Do not make", "Would require engineered guarding, characterization and qualified supervision.", "Not appropriate now", "02_Engineering/ENGINEERING_OVERVIEW.md", "None", "PHYSICAL", "High-voltage equipment", "Not applicable", "0", "UNKNOWN", "Not estimated", "Qualified facility, design review, safety review, and validated question would be required.", "No build or test documented; school construction is not recommended.", "NO", "NO", "P0", "DO_NOT_PRODUCE", "Do not purchase or construct for the current display."],
    ["BUILD-03", "Chemical PV processing demonstration", "Do not make", "Chemical extraction/refining is outside the current student build boundary.", "Not appropriate now", "01_Research/RESEARCH_OVERVIEW.md", "None", "PHYSICAL", "Hazardous chemical process", "Not applicable", "0", "UNKNOWN", "Not estimated", "Qualified laboratory, trained staff, risk assessment, waste and approvals.", "No chemicals, assays or lab access are documented.", "NO", "NO", "P0", "DO_NOT_PRODUCE", "Do not buy reagents or process panels outside qualified approved facilities."],
    ["WAIT-01", "AGASTYA recovery, grade, purity or recovery graph", "Wait for data", "Report experimental performance only after matched feed and assays.", "Future only", "No measured AGASTYA data exists", "No output yet", "DIGITAL", "Chart", "Not applicable", "0", "UNKNOWN", "Not estimated", "Obtain representative sample, weigh all streams and get validated assay results.", "No experimental observations; sample count is 0.", "NO", "NO", "P1", "WAIT", "Do not make a decorative or literature-only graph that appears to be AGASTYA results."],
    ["SKIP-01", "QR code without an approved live destination", "Do not produce", "Avoid a dead link or unapproved student/data exposure.", "Not required", "No destination identified", "None", "DIGITAL/PHYSICAL", "QR code", "Not applicable", "0", "UNKNOWN", "Low", "A destination and event permission would need to exist first.", "No approved destination provided.", "NO", "NO", "P3", "DO_NOT_PRODUCE", ""],
]
print_rows = [dict(zip(PRINT_FIELDS, row)) for row in PRINT]
write_csv(ROOT / "06_NCSC_Display/PRINT_AND_BUILD_REGISTER.csv", PRINT_FIELDS, print_rows)

missing = []
for row in CATALOG:
    target = ROOT / row["current_path"]
    if not target.exists():
        missing.append(row["current_path"])
print(f"Wrote catalog ({len(CATALOG)} records), migration log ({len(migration)} moves), and print/build register ({len(print_rows)} decisions).")
if missing:
    print("CATALOG PATHS TO REVIEW:")
    for value in missing:
        print(" -", value)
