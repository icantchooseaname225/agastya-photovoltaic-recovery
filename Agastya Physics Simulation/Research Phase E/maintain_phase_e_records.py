"""Maintain Phase E evidence, registers, research log and concise logbook copies."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SIMROOT = ROOT / "Agastya Physics Simulation"
PHASE = SIMROOT / "Research Phase E"
LOGBOOK = ROOT / "04_Logbook"


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def update_evidence_register() -> None:
    path = SIMROOT / "Research Phase D" / "Evidence_Register.csv"
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)
    assert fields
    existing = {row["ID"] for row in rows}
    additions = [
        {
            "ID": "E25", "Reference or project artifact": "Frischknecht, Komoto & Doi. Life Cycle Assessment of c-Si PV Module Delamination with Hot Knife Technology",
            "Year": "2023", "Source type": "IEA PVPS technical report; primary pilot-plant inventory",
            "URL or workspace path": "https://iea-pvps.org/wp-content/uploads/2023/07/Report_IEA-PVPS_T12-25-2023_LCA-PV-Recycling-Hot-Knife.pdf",
            "Feed / scope": "Hot-knife delamination of framed c-Si modules; functional unit is 1 kg at installation location",
            "Reported evidence used": "Pilot-plant data representative of 2018; described J-box removal, framing and glass/laminate separation; downstream Cu/Ag recovery identified as further treatment; data quality classified fair.",
            "AGASTYA use": "Clarifies the current Stage 3 thermal-delamination reference boundary and environmental inventory requirements.",
            "Limit / access status": "Full 24-page report reviewed. Different facility, feed, geography and functional unit; it is not an AGASTYA energy or recovery estimate.",
            "Confidence for stated claim": "High for report scope and stated pilot inventory; low transferability to AGASTYA.",
        },
        {
            "ID": "E26", "Reference or project artifact": "Hallam et al. The silver learning curve for photovoltaics and projected silver demand for net-zero emissions by 2050",
            "Year": "2023", "Source type": "Peer-reviewed research article",
            "URL or workspace path": "https://doi.org/10.1002/pip.3661",
            "Feed / scope": "Technology-specific photovoltaic silver consumption and demand scenarios",
            "Reported evidence used": "Reports markedly different 2020 Ag consumption estimates per cell and module for PERC, TOPCon and SHJ; describes changes over time.",
            "AGASTYA use": "Shows why a generic/module-age-independent silver inventory cannot substitute for identified-feed assay.",
            "Limit / access status": "Article content and tables reviewed. Manufacturing consumption is not residual Ag assay in an end-of-life module and does not state recoverability.",
            "Confidence for stated claim": "High for reported study estimates; not an AGASTYA feed composition.",
        },
        {
            "ID": "E27", "Reference or project artifact": "Tammaro et al. Thermal treatment of waste photovoltaic module for recovery and recycling: experimental assessment of metals in gas emissions and ashes",
            "Year": "2015", "Source type": "Peer-reviewed research article; abstract/metadata review",
            "URL or workspace path": "https://doi.org/10.1016/j.renene.2015.03.014",
            "Feed / scope": "Three c-Si panel samples treated in a furnace for polymer degradation",
            "Reported evidence used": "Samples heated up to 600 °C to complete EVA degradation; component mass changes and post-treatment cell surfaces were examined, including SEM-EDS.",
            "AGASTYA use": "Separates high-temperature polymer degradation questions from the local interface-heating model for thermal Stage 3 delamination.",
            "Limit / access status": "Abstract/metadata page reviewed; full text not available in this pass. Furnace conditions do not validate hot-knife behavior.",
            "Confidence for stated claim": "Moderate for abstract-reported methods; no transfer to AGASTYA.",
        },
        {
            "ID": "E28", "Reference or project artifact": "Shang et al. Kinetic characteristics and emission reduction potential during thermal treatment of PV modules with different encapsulants",
            "Year": "2026", "Source type": "Peer-reviewed research article; abstract review",
            "URL or workspace path": "https://doi.org/10.1016/j.jece.2026.121479",
            "Feed / scope": "Thermal treatment of decommissioned modules with EVA and alternative encapsulants",
            "Reported evidence used": "Abstract reports improved Coats–Redfern kinetic analysis, a Gompertz fit for VOC emissions, and encapsulant-dependent VOC/CO behavior.",
            "AGASTYA use": "Flags formulation-dependent emissions and the need for emissions data if a thermal degradation route is considered.",
            "Limit / access status": "Abstract reviewed, full article not available in this pass. Conditions concern thermal treatment and cannot parameterize hot-knife contact heating.",
            "Confidence for stated claim": "Moderate for abstract-reported claims; not transferable as an AGASTYA prediction.",
        },
    ]
    rows.extend(row for row in additions if row["ID"] not in existing)
    write_csv(path, list(fields), rows)


def registers() -> None:
    progress_fields = ["Task", "Previous status", "Current status", "Evidence of completion", "Remaining problem", "Next action", "Priority"]
    progress_rows = [
        {"Task": "Audit existing AGASTYA research and simulation state", "Previous status": "Executed in Phase D", "Current status": "Executed", "Evidence of completion": "Read Phase D reports/registers, current charter/crosswalk, historic code, procedures, master CSV, current logbook and project navigation; preserved prior files.", "Remaining problem": "Pre-write inventory snapshot is metadata inventory, not semantic review of every file; some original literature remains abstract-only.", "Next action": "Update semantic audit only when a decision-relevant artifact changes.", "Priority": "P1"},
        {"Task": "Map the historical Phase D/E records to the corrected architecture", "Previous status": "Phase E used the 13 October map", "Current status": "Corrected in current project records", "Evidence of completion": "The 16 October owner correction sets Stage 1 inspection/routing; Stage 2 manual mechanical preparation; Stage 3 thermal treatment/delamination; Stage 4 silver removal/recovery. Sampling and assay validate every stage.", "Remaining problem": "No process performance is physically validated; Phase D/E reports retain dated historical numbering.", "Next action": "Use AGASTYA_ARCHITECTURE.md for current documents and mark dated reports as historical.", "Priority": "P1"},
        {"Task": "Second-round literature review: material, thermal and process boundary", "Previous status": "Not Started for Phase E", "Current status": "Executed", "Evidence of completion": "Reviewed IEA PVPS 2023 hot-knife LCA, Hallam 2023 technology-specific silver inventory article, and abstracts for Tammaro 2015 and Shang 2026; added E25-E28.", "Remaining problem": "Tammaro and Shang were abstract-level only; no actual feed composition source resolves AGASTYA silver inventory.", "Next action": "Obtain full texts if they materially affect a chosen route; prioritize identified-feed assay.", "Priority": "P1"},
        {"Task": "Characterize module materials and silver inventory", "Previous status": "Blocked in Phase D", "Current status": "Blocked", "Evidence of completion": "Published technology-dependent differences documented; three previous literature cases retained separately.", "Remaining problem": "No identified AGASTYA module/lot, bill of materials, sample or validated Ag assay.", "Next action": "Register one feed lot and agree representative sampling and matrix-valid assay.", "Priority": "P1"},
        {"Task": "Assess the Stage 3 thermal reference model", "Previous status": "Executed, unvalidated historical model", "Current status": "Numerically reviewed; physically unvalidated", "Evidence of completion": "Historical five-node 5,040-case sweep analyzed; main effects ranked; 1-D spatial finite-volume extension executed.", "Remaining problem": "Thermal properties/contact boundary are assumed; no adhesion, fracture, EVA kinetics, emissions or experimental temperatures; mesh 8-to-16 peak EVA difference reaches about 2.09% in nominal case.", "Next action": "After sample and host gates, define a supervised coupon measurement and separation-quality metric; retain further mesh/timestep work only if it informs that validation.", "Priority": "P2"},
        {"Task": "Thermal sweep main-effect sensitivity", "Previous status": "Not Started for Phase E", "Current status": "Executed", "Evidence of completion": "Equal-weight variance decomposition on all 5,040 balanced scenarios; dwell and contact conductance dominate modeled outputs.", "Remaining problem": "Factor levels are analyst/design inputs, not measured distributions; interaction share remains.", "Next action": "Use rank only to guide measurements; do not assign probabilities.", "Priority": "P2"},
        {"Task": "Spatial mesh and numerical verification", "Previous status": "Not Started for Phase E", "Current status": "Executed", "Evidence of completion": "Four cases across 5 mesh levels; explicit divergence preserved; backward Euler run; coarse limit and energy residual checked.", "Remaining problem": "Local EVA peak has mesh sensitivity; numerical convergence is not physical validation.", "Next action": "If thermal design is active, extend mesh and validate against instrumented coupons.", "Priority": "P2"},
        {"Task": "Thermal time-step sensitivity", "Previous status": "Not Started for Phase E", "Current status": "Executed", "Evidence of completion": "Two conditions at 80 nodes and 1.0, 0.5, 0.25 ms; max 0.5-vs-0.25 ms relative difference about 0.00126% across tracked outputs.", "Remaining problem": "Only two conditions; solver comparison does not address model-form uncertainty.", "Next action": "Expand only if thermal route decision requires it.", "Priority": "P2"},
        {"Task": "Stage 2 manual mechanical preparation and stream tracking", "Previous status": "Documented under prior numbering", "Current status": "Blocked pending a traceable feed", "Evidence of completion": "Current architecture defines manual removal of accessible components and preparation of a traceable laminate feed.", "Remaining problem": "No feed lot, measured component streams, dust capture or facility trial.", "Next action": "Define the Stage 2 feed boundary and record all outputs when an approved sample is available.", "Priority": "P1"},
        {"Task": "Stage 4 silver-removal route and model readiness", "Previous status": "Electrostatic mechanism assessed under prior numbering", "Current status": "Route open; no Agastya model or result", "Evidence of completion": "Electrostatic and flotation literature are source-qualified as route comparators; required measurements are documented.", "Remaining problem": "No characterized Stage 3 feed, receiver/product form, qualified facility, route-specific inputs or Ag assays.", "Next action": "Define feed/product requirements and facility/assay gates before selecting or parameterizing any route model.", "Priority": "P1"},
        {"Task": "All-stage sampling, assay and accounting", "Previous status": "Executed at formula/template level", "Current status": "Formula checked; physical inputs absent", "Evidence of completion": "Accounting equations, null propagation, source conversions and synthetic self-check documented; measurement is assigned across all stages.", "Remaining problem": "No representative stream samples, qualified preparation/assay, QA/QC or uncertainty.", "Next action": "Agree assay acceptance and sampling plan with a qualified laboratory before processing.", "Priority": "P1"},
        {"Task": "Integrated mass, Ag and energy performance", "Previous status": "Blocked in Phase D", "Current status": "Blocked", "Evidence of completion": "Stage interfaces and required stream ledger documented.", "Remaining problem": "Measured feed, yields, assays, losses, power, consumables and downstream boundary absent.", "Next action": "Populate only from measured stream records after feed trial.", "Priority": "P1"},
        {"Task": "Simulation campaign traceability", "Previous status": "Partial historical registers", "Current status": "Executed", "Evidence of completion": "Phase E simulation register lists historical, Phase D, Phase E and blocked model families with statuses and limitations.", "Remaining problem": "Some inherited outputs have historical names and separate schemas.", "Next action": "Assign unique IDs and preserve historical outputs for every new run.", "Priority": "P2"},
        {"Task": "Seven-report publication collection and master index", "Previous status": "Not Started for Phase E", "Current status": "Executed", "Evidence of completion": "Seven substantive Markdown sources, seven A4 technical PDFs and a PDF index generated; automated page/font/text checks passed; representative pages visually inspected.", "Remaining problem": "Target-printer proof and any presentation-specific print requirements remain external to this digital check.", "Next action": "Use the PDF index and review target print settings before physical printing.", "Priority": "P1"},
        {"Task": "Shorten Day 24 onward logbook entries", "Previous status": "Long original entries retained", "Current status": "Executed", "Evidence of completion": "Day 24 and Day 25 originals preserved; concise versions plus a Day 26 counterpart are maintained in Short Versions.", "Remaining problem": "Day 26 is a dated digital continuation record with a concise counterpart; it documents no physical experiment.", "Next action": "Add a matching concise version for every new full digital logbook record.", "Priority": "P2"},
        {"Task": "Repository navigation and output quality check", "Previous status": "Phase D structure exists", "Current status": "Executed", "Evidence of completion": "Phase E README, root project index/status/changelog pointers, report index, source/PDF directories, simulation folders and logbook links updated.", "Remaining problem": "Target print workflow remains unverified; Phase D inventory is a pre-write snapshot.", "Next action": "Refresh file catalog/inventory during the next repository maintenance pass.", "Priority": "P2"},
    ]
    write_csv(PHASE / "Research_Progress_Register.csv", progress_fields, progress_rows)

    sim_fields = ["Simulation ID", "Research question", "Stage", "Model", "Inputs", "Sources", "Execution status", "Outputs", "Verification", "Validation", "Findings", "Limitations", "Next experiment"]
    sim_rows = [
        {"Simulation ID": "HIST-SIM-001", "Research question": "What values follow from the historic virtual-scenario campaign?", "Stage": "Legacy labels spanning several stages; do not remap outputs", "Model": "Python scenario arithmetic, simplified thermal RC and distribution calculations", "Inputs": "Historical sweep inputs documented in dataset metadata and procedure files", "Sources": "Historical project scripts and assumptions", "Execution status": "Executed", "Outputs": "147,912 master rows + 52,168 follow-up rows = 200,080 virtual/scenario records", "Verification": "Historical metadata records counts and selected arithmetic checks", "Validation": "No physical validation", "Findings": "Scenario rows are not physical samples or statistical replicates", "Limitations": "Several input assumptions are analyst-selected; output families have different meanings", "Next experiment": "Do not rerun wholesale; target a decision-relevant gap."},
        {"Simulation ID": "HIST-S3-02", "Research question": "How does assumed tool setpoint/contact/dwell affect a layered stack?", "Stage": "Current Stage 3 thermal/delamination reference; model developed before the 16 October correction", "Model": "Five-node 1-D thermal RC; explicit Euler", "Inputs": "5 tool levels, 4 conductance levels, 7 dwell levels, 3 ambients, 2 EVA thicknesses, 2 property sets, 3 interface resistances", "Sources": "Agastya_Physics_Simulation_2026-10-10.py and cited property sets in source docs", "Execution status": "Executed", "Outputs": "5,040 summary rows plus selected thermal traces", "Verification": "Numerical energy residual max about 9.22e-12%; historic time-step checks", "Validation": "Not compared to AGASTYA temperature/separation measurements", "Findings": "Peak EVA 15.65–261.53 °C and contact energy 1.38 kJ–1.72 MJ m-2 over assumed grid", "Limitations": "No chemistry, fracture, moving tool, actual stackup or equipment energy", "Next experiment": "If P1-01/P1-02 are resolved and the host approves, compare instrumented coupon temperatures and separation quality; do not treat the model as a validated setting."},
        {"Simulation ID": "HIST-S3-04", "Research question": "Does explicit integration step change the historical reduced-model peak?", "Stage": "Current Stage 3 thermal model; historical timestep comparison", "Model": "Five-node explicit Euler timestep comparison", "Inputs": "Eight representative cases; 10, 5, 2.5 and 1.25 ms", "Sources": "PROCEDURES_AND_RESULTS.md", "Execution status": "Executed", "Outputs": "32 follow-up records", "Verification": "Largest peak EVA difference from 1.25 ms was 0.154541 °C", "Validation": "Numerical sensitivity only", "Findings": "Small time-step sensitivity for the tested reduced-model cases", "Limitations": "No validation of properties, boundaries or physical process", "Next experiment": "No broad rerun; numerical method changed for spatial refinement."},
        {"Simulation ID": "PH-D-ACCOUNTING-001", "Research question": "Do source-normalized Ag unit conversions and null propagation behave as specified?", "Stage": "All-stage measurement/accounting support", "Model": "Guarded Python material/Ag ledger; standard-library arithmetic", "Inputs": "300 ppm, 600 g/t and unresolved 630 g/t, normalized to 1 kg", "Sources": "Research Phase D accounting script and evidence register", "Execution status": "Executed", "Outputs": "Normalized reference JSON and synthetic formula self-check", "Verification": "Unit conversions and synthetic equations checked; measured values remain null", "Validation": "Code self-check only; not physical process validation", "Findings": "0.300, 0.600 and 0.630 g/kg are distinct literature cases", "Limitations": "No identified AGASTYA feed or assays", "Next experiment": "Replace reference cases only with source-qualified feed assay."},
        {"Simulation ID": "PE-SIM-001", "Research question": "Which factors dominate output variance in the existing 5,040 thermal scenarios?", "Stage": "Current Stage 3 thermal reference model", "Model": "Balanced full-factorial one-way main-effect sums of squares", "Inputs": "Existing EXP-S3-02 outputs; equal weight per design row", "Sources": "Historical master CSV and Phase E run_phase_e_experiments.py", "Execution status": "Executed", "Outputs": "main_effect_variance.json and 300 dpi PNG", "Verification": "5,040 records; factor level counts balanced; interaction/unallocated share retained", "Validation": "Not physical uncertainty or process validation", "Findings": "Dwell and contact conductance rank highest across tracked outputs", "Limitations": "No distributions, probabilities, or measured factor ranges", "Next experiment": "Measure temperature/dwell and separation quality only in an approved supervised Stage 3 study."},
        {"Simulation ID": "PE-SIM-002", "Research question": "Does spatial refinement alter local layer temperatures in the historical thermal model?", "Stage": "Current Stage 3 thermal reference model", "Model": "1-D five-layer finite-volume model; backward Euler; Picard radiation update", "Inputs": "Four selected cases; 1/2/4/8/16 cells per layer; 0.5 ms step; two historical property sets", "Sources": "Historical thermal code/property sets; Phase E model script", "Execution status": "Executed", "Outputs": "20 processed rows, summary JSON, PNG; failed explicit run retained under raw/", "Verification": "N=1 coarse comparison, energy residual <6.3e-10%, explicit stability diagnosis", "Validation": "No experimental validation", "Findings": "N16 EVA peaks exceed N1 by up to ~29 °C in selected high-bound case; N8-to-N16 EVA differences up to 2.09%", "Limitations": "Same model form; assumed properties/contact; no EVA chemistry or separation-quality model", "Next experiment": "Compare with instrumented coupon temperatures and separation quality only after P1 gates and host approval."},
        {"Simulation ID": "PE-SIM-003", "Research question": "Is the 80-control-volume thermal result sensitive to timestep?", "Stage": "Current Stage 3 thermal reference model", "Model": "Same backward-Euler finite-volume model", "Inputs": "Nominal/high-bound cases at 1.0, 0.5 and 0.25 ms", "Sources": "Phase E run_phase_e_experiments.py and processed timestep CSV", "Execution status": "Executed", "Outputs": "Six timestep comparison rows", "Verification": "0.5 vs 0.25 ms maximum relative difference ~0.00126%; energy residual <7.6e-10%", "Validation": "Numerical sensitivity only", "Findings": "Reported outputs are time-step stable for these two selected conditions", "Limitations": "Two cases only; model-form and physical uncertainty remain", "Next experiment": "No expansion unless it supports a specific Stage 3 validation decision."},
        {"Simulation ID": "AG-S3-ELECTROSTATIC-001", "Research question": "Can an electrostatic process remove silver from the characterized Stage 3 output?", "Stage": "Stage 4 route comparator; not current process model", "Model": "Candidate field/particle trajectory or separator response model", "Inputs": "Defined product form, geometry, voltage, feed rate, humidity, PSD, shape, conductivity/charge distributions and assays", "Sources": "Historical Stage_3_Model specification and source-qualified literature", "Execution status": "Blocked", "Outputs": "None", "Verification": "Not applicable", "Validation": "No data", "Findings": "Cannot identify performance from current records", "Limitations": "Core inputs and silver-removal evidence are absent; literature conditions do not transfer automatically", "Next experiment": "Compare routes against characterized Stage 3 feed, receiver/product needs, qualified facility, assay plan and waste route before model selection."},
        {"Simulation ID": "AG-INTEGRATED-001", "Research question": "What are total silver recovery, energy and material losses?", "Stage": "Integrated four-stage process", "Model": "Stage-wise mass/Ag/energy balance", "Inputs": "Measured feed and stream masses, assays, losses, energy, consumables and process boundary", "Sources": "Current four-stage process model and accounting code", "Execution status": "Blocked", "Outputs": "None; unknowns remain null", "Verification": "Accounting formula self-check only", "Validation": "No physical validation", "Findings": "No integrated numerical outcome is defensible", "Limitations": "Stage measurements and feed assay absent", "Next experiment": "Populate ledger only after a traceable instrumented run."},
    ]
    write_csv(PHASE / "Simulation_Register.csv", sim_fields, sim_rows)


def logs_and_short_entries() -> None:
    (PHASE / "Research_Log.md").write_text(
        "# Phase E research log\n\n**Started:** 13 October 2026  \n**Scope:** second-round literature review, targeted computational experiments, reports, logbook compression and repository maintenance.\n\n"
        "## Work completed\n\n"
        "- Audited Phase D outputs, the historic model and data, current process mapping, evidence register, and original Day 24/Day 25 records. Confirmed that no AGASTYA physical sample, assay, electrostatic trial or external solver result exists.\n"
        "- Reviewed the IEA PVPS hot-knife LCA in full and source content from Hallam et al. (2023); examined abstracts/metadata for Tammaro et al. (2015) and Shang et al. (2026). Added evidence rows E25–E28 with access limits.\n"
        "- Executed PE-SIM-001: main-effect variance decomposition on 5,040 archived thermal summary rows. Dwell and contact conductance dominated temperature and energy variance in the specified grid. Equal-weight design shares are not probability distributions.\n"
        "- Executed PE-SIM-002: 20 spatial refinements across four selected cases and five mesh sizes. The initial explicit 0.5 ms method diverged at finer silicon meshes; the failed results were preserved under `Simulation_Campaign/raw/`. The final backward-Euler runs closed the numerical energy balance to below 6.3e-10% and matched the coarse limit closely.\n"
        "- Executed PE-SIM-003: 1.0, 0.5 and 0.25 ms timestep comparison for nominal and high-bound conditions at 80 control volumes. The maximum relative difference between 0.5 and 0.25 ms was approximately 0.00126% among tracked outputs.\n"
        "- Prepared the simulation/progress registers, seven report sources, eight A4 PDFs (seven reports plus index), and concise Day 24/Day 25 versions. Automated page/text/font checks passed; principal dossier, thermal, Stage 4 and mass-flow pages were visually inspected. A target-printer proof has not been performed.\n\n"
        "## Interpretation\n\n"
        "All new simulation results concern a historical thermal model that maps to current Stage 3 thermal treatment/delamination under inherited assumptions. They do not model peel quality, current Stage 4 silver removal, or a physical Agastya result. The thermal mesh study shows local temperature sensitivity to resolution; it does not validate material properties, contact conditions or delamination. Process performance remains blocked by absent feed, mass, stream and assay data.\n\n"
        "## Next decisions\n\n"
        "Prioritize P1-01 Stage 3/Stage 4 interface definition, then P1-02 traceable feed and qualified-host availability. Any thermal Stage 3 trial requires an approved facility, calibrated records, supervision, assay plan and waste route. Stage 4 silver-removal comparisons follow the characterized feed and required product form.\n",
        encoding="utf-8")

    versions = LOGBOOK / "Short Versions"
    versions.mkdir(exist_ok=True)
    day24 = """# Day 24 | 10 October 2026

**Objective:** Establish an evidence-based process map and accounting baseline before new simulations.

**Work performed:** Reviewed the project charter and literature, reconciled the current four stages with legacy thermal/comminution labels, prepared a normalized one-kilogram composition scenario, and added a reproducible accounting kernel. The scenario retained an unassigned mass remainder and kept the 0.630 g/kg silver reference separate.

**Key finding:** No traceable AGASTYA sample, assay, process stream or new solver run was documented; an integrated recovery estimate was not defensible.

**Next step:** Identify a representative c-Si feed and agree on sampling and assay before process modeling.
"""
    day25 = """# Day 25 | 13 October 2026

**Objective:** Audit prior work and continue evidence-led modeling and documentation.

**Work performed:** Reconciled the four-stage architecture, reviewed additional thermal, hot-knife and silver-metallization sources, and analyzed all 5,040 historical thermal scenarios. Ran spatial and timestep refinements; preserved the unstable explicit-mesh run and completed stable backward-Euler runs. Prepared research registers and the report collection.

**Key finding:** Dwell and contact conductance dominate modeled thermal-sweep variance. Spatial resolution raises local EVA peak predictions, while numerical energy closure and timestep checks pass; none validates a real panel or process.

**Next step:** Complete report quality checks, then prioritize a traceable feed lot, qualified Ag assay and measured Stage 1/2 data.
"""
    (versions / "DAY_24_SHORT_ENTRY.md").write_text(day24, encoding="utf-8")
    (versions / "DAY_25_SHORT_ENTRY.md").write_text(day25, encoding="utf-8")
    (versions / "README.md").write_text(
        "# Concise logbook versions\n\n"
        "Short versions begin at Day 24 and cover each subsequent day that exists in the surviving record. Original Day 24 and Day 25 files remain unchanged and are backed up under `../Originals_Before_Concise_Edit_2026-10-13/`. No missing days or unrecorded work were added. Day 25 and Day 26 are digital research records, not handwritten student notebook entries.\n\n"
        "- [Day 24 short entry](DAY_24_SHORT_ENTRY.md) — source date 10 October 2026.\n"
        "- [Day 25 short entry](DAY_25_SHORT_ENTRY.md) — source date 13 October 2026; updated to include work performed on that date in Phase E.\n"
        "- [Day 26 short entry](DAY_26_SHORT_ENTRY.md) — source date 21 October 2026; concise counterpart to the digital continuation record.\n",
        encoding="utf-8")

    index = LOGBOOK / "Logbook_Index.md"
    text = index.read_text(encoding="utf-8")
    if "## Concise entries from Day 24 onward" not in text:
        text += "\n## Concise entries from Day 24 onward\n\n- [Day 24 short entry](Short%20Versions/DAY_24_SHORT_ENTRY.md)\n- [Day 25 short entry](Short%20Versions/DAY_25_SHORT_ENTRY.md)\n- [Day 26 short entry](Short%20Versions/DAY_26_SHORT_ENTRY.md)\n- [Original-entry backup](Originals_Before_Concise_Edit_2026-10-13/)\n"
    index.write_text(text, encoding="utf-8")


def write_readmes() -> None:
    (PHASE / "Simulation_Campaign" / "README.md").write_text(
        "# Phase E simulation campaign\n\n"
        "The campaign contains raw preserved failures, processed calculations and figures generated from documented models. Read `../../Simulation_Register.csv` for status and limitations.\n\n"
        "- `models/run_phase_e_experiments.py` runs PE-SIM-001/002/003.\n"
        "- `raw/` preserves the first unstable explicit-Euler spatial-refinement outputs; do not use them as results.\n"
        "- `processed/` contains sensitivity JSON, spatial and timestep CSVs, coarse-model comparison and the experiment summary.\n"
        "- `figures/` contains 300 dpi plots.\n\n"
        "Run from the project environment with Python, NumPy, pandas and Pillow installed:\n\n"
        "```powershell\npython .\\models\\run_phase_e_experiments.py\n```\n\n"
        "All experiments are deterministic model calculations for a historical thermal model that now maps to current Stage 3. They do not predict delamination quality or Stage 4 silver removal. There are no physical inputs or independent validation measurements.\n",
        encoding="utf-8")
    (PHASE / "Simulation_Campaign" / "models" / "README.md").write_text(
        "# Phase E model notes\n\n"
        "`run_phase_e_experiments.py` imports the historical model from the project-local `Agastya Physics Simulation` directory, reads the master CSV, runs a balanced-grid main-effect decomposition, then runs one-dimensional finite-volume spatial/timestep studies for a hot-knife-like Stage 3 reference. The model does not predict separation quality or silver recovery.\n\n"
        "Dependencies recorded from the bundled runtime: Python 3.12.14, NumPy 2.3.5, pandas 3.0.1, Pillow 12.3.0. Re-run it from the campaign folder or provide the same fixed paths. Inputs and equations are described in the Computational Modeling and Simulation Atlas. Outputs are written to `../processed/` and `../figures/`; raw failed explicit outputs are preserved separately.\n\n"
        "No Stage 4 silver-removal model is executable: feed properties, route-specific inputs, measured streams and assays remain absent.\n",
        encoding="utf-8")


if __name__ == "__main__":
    update_evidence_register()
    registers()
    logs_and_short_entries()
    write_readmes()
    print("Updated evidence rows E25-E28, Phase E registers/log, concise Day 24/25 versions, and model/campaign readmes.")

