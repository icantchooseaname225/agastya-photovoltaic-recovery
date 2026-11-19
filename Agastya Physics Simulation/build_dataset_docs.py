"""Build the Agastya simulation field dictionary and experiment register."""

from __future__ import annotations

import csv
import importlib.util
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "Agastya_Physics_Simulation_2026-10-10.py"
FOLLOWUP = ROOT / "followup_virtual_experiments.py"
BASE_META = ROOT / "Agastya_Physics_Simulation_2026-10-10_metadata.json"
FOLLOWUP_META = ROOT / "followup_virtual_experiments_metadata.json"
BASE_CSV = ROOT / "Agastya_Physics_Simulation_2026-10-10.csv"
FOLLOWUP_CSV = ROOT / "followup_virtual_experiments.csv"
DICTIONARY = ROOT / "data_dictionary.csv"
REGISTER = ROOT / "experiment_register.csv"
ANALYSIS = ROOT / "dataset_checks_and_summary.json"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


base = load_module("agastya_base_for_docs", BASE)
follow = load_module("agastya_followup_for_docs", FOLLOWUP)

BASE_DOCS = {
    "record_id": ("Unique master-dataset row identifier, prefixed R.", "identifier", "all rows"),
    "experiment_id": ("Experiment register key for the procedure that generated the row.", "identifier", "all rows"),
    "procedure_id": ("Procedure key linking this row to the written method.", "identifier", "all rows"),
    "stage": ("Agastya process stage represented by the row.", "category", "all rows"),
    "record_type": ("Output block/type; distinguishes mass balance, thermal, screening and Ag records.", "category", "all rows"),
    "evidence_status": ("Evidence class. All master rows are scenario, numerical model, or literature-normalized calculations; no physical trial data.", "category", "all rows"),
    "scenario_id": ("Readable combination key for the input assumptions used in this row.", "identifier", "all rows"),
    "source_basis": ("Evidence, model boundary, and/or assumption text for this row.", "text", "all rows"),
    "ambient_C": ("Assumed ambient temperature for Stage 3 transient calculation.", "°C", "Stage 3 thermal rows"),
    "panel_mass_kg": ("Assumed incoming module mass per panel.", "kg/panel", "Stage 2, Stage 3 balances and Stage 4 scenarios"),
    "stage2_frame_share_pct": ("Assumed removable aluminium frame fraction of original panel mass.", "%", "Stage 2 and downstream scenarios"),
    "stage2_jbox_cable_share_pct": ("Assumed junction-box and external-cable fraction; not total module copper fraction.", "%", "Stage 2 and downstream scenarios"),
    "stage2_manual_time_s": ("Assumed supervised manual hand-off time per panel.", "s/panel", "Stage 2 balance"),
    "stage2_frame_mass_kg": ("Scenario frame mass calculated from panel mass × frame share.", "kg/panel", "Stage 2 balance"),
    "stage2_jbox_cable_mass_kg": ("Scenario removable J-box/external-cable mass.", "kg/panel", "Stage 2 balance"),
    "stage2_input_mass_kg": ("Scenario mass entering Stage 2.", "kg/panel", "Stage 2 balance"),
    "stage2_output_to_stage3_kg": ("Calculated Stage 2 hand-off mass after frame and J-box/cable removal.", "kg/panel", "Stage 2 balance"),
    "stage2_mass_closure_pct": ("Calculated Stage 2 output/input mass closure; 100% by construction.", "%", "Stage 2 balance"),
    "stage2_operator_capacity_panels_8h": ("Ideal one-operator 8-hour ceiling from 28,800 s divided by assumed manual task time.", "panels/8 h/operator", "Stage 2 balance"),
    "stage3_glass_share_of_original_pct": ("Assumed front-glass share of original panel mass.", "%", "Stage 3 balances and Stage 4 scenarios"),
    "stage3_input_mass_kg": ("Calculated mass handed from Stage 2 into the Stage 3 mass balance.", "kg/panel", "Stage 3 material balance"),
    "stage3_front_glass_mass_kg": ("Scenario glass output mass.", "kg/panel", "Stage 3 material balance"),
    "stage3_laminate_mass_kg": ("Scenario cell/EVA/backsheet laminate mass after front-glass separation.", "kg/panel", "Stage 3 and Stage 4 rows"),
    "stage3_mass_closure_pct": ("Calculated Stage 3 glass + laminate/input mass closure; 100% by construction.", "%", "Stage 3 material balance"),
    "stage3_material_property_set": ("Literature table name supplying modeled layer material properties.", "identifier", "Stage 3 thermal rows"),
    "stage3_blade_setpoint_C": ("Assumed fixed hot-knife boundary temperature.", "°C", "Stage 3 thermal rows"),
    "stage3_contact_conductance_W_m2K": ("Assumed blade-to-workpiece thermal contact conductance.", "W/(m²·K)", "Stage 3 thermal rows"),
    "stage3_contact_duration_s": ("Assumed local contact dwell; distinct from a full-panel machine cycle.", "s", "Stage 3 thermal rows"),
    "stage3_EVA_total_thickness_mm": ("Assumed total front + rear EVA thickness.", "mm", "Stage 3 thermal rows"),
    "stage3_backsheet_thickness_mm": ("Thickness assigned to the backsheet layer in the selected property set.", "mm", "Stage 3 thermal rows"),
    "stage3_interface_resistance_m2K_W": ("Assumed thermal resistance added at each modeled layer interface.", "m²·K/W", "Stage 3 thermal rows"),
    "stage3_time_s": ("Model elapsed time since initial ambient condition, including the brief modeled cooldown in trace rows.", "s", "Stage 3 thermal rows"),
    "stage3_T_interface_C": ("Modeled hot-knife/glass-EVA interface temperature.", "°C", "Stage 3 thermal rows"),
    "stage3_T_glass_node_C": ("Modeled glass-node temperature.", "°C", "Stage 3 thermal rows"),
    "stage3_T_EVA_front_node_C": ("Modeled front EVA-node temperature.", "°C", "Stage 3 thermal rows"),
    "stage3_T_cell_node_C": ("Modeled silicon-cell node temperature.", "°C", "Stage 3 thermal rows"),
    "stage3_T_EVA_rear_node_C": ("Modeled rear EVA-node temperature.", "°C", "Stage 3 thermal rows"),
    "stage3_T_backsheet_node_C": ("Modeled backsheet-node temperature.", "°C", "Stage 3 thermal rows"),
    "stage3_peak_EVA_node_C": ("Maximum across front/rear EVA nodes; on a thermal summary it is the case peak, while a time-trace row contains the value at that snapshot.", "°C", "Stage 3 thermal rows"),
    "stage3_peak_cell_node_C": ("Modeled silicon-cell maximum for a thermal summary; a time-trace row contains the cell temperature at that snapshot.", "°C", "Stage 3 thermal rows"),
    "stage3_net_contact_energy_J_m2": ("Integrated modeled hot-knife heat input per assumed contact area; not panel energy or electrical draw.", "J/m²", "Stage 3 thermal rows"),
    "stage3_time_above_100C_s": ("Modeled time the hotter of the two EVA nodes is at or above 100 °C.", "s", "Stage 3 case summaries"),
    "stage3_time_above_140C_s": ("Modeled time the hotter of the two EVA nodes is at or above 140 °C.", "s", "Stage 3 case summaries"),
    "stage3_time_above_180C_s": ("Modeled time the hotter of the two EVA nodes is at or above 180 °C.", "s", "Stage 3 case summaries"),
    "stage3_time_above_220C_s": ("Modeled time the hotter of the two EVA nodes is at or above 220 °C.", "s", "Stage 3 case summaries"),
    "stage3_time_above_280C_s": ("Modeled time the hotter of the two EVA nodes is at or above 280 °C; comparison statistic, not an operating/safety threshold.", "s", "Stage 3 case summaries"),
    "stage3_energy_balance_error_pct": ("Integrated input-minus-surface-loss-minus-stored-energy residual relative to modeled heat input.", "%", "Stage 3 case summaries"),
    "stage4_feed_mass_kg": ("Assumed Stage 4 laminate mass feed for the scenario.", "kg/panel", "Stage 4 rows"),
    "stage4_particle_mass_D50_mm": ("Assumed median particle size for a mass-weighted lognormal distribution.", "mm", "Stage 4 size rows"),
    "stage4_particle_geometric_SD": ("Assumed geometric standard deviation of particle size.", "dimensionless", "Stage 4 size rows"),
    "stage4_screen_cut_mm": ("Assumed ideal screen cut used to calculate a lognormal mass fraction.", "mm", "Stage 4 size rows"),
    "stage4_fines_mass_fraction_model": ("Modeled cumulative PSD mass fraction below the assumed cut; assumes an ideal screen.", "fraction", "Stage 4 size rows"),
    "stage4_fines_mass_kg": ("Modeled feed mass multiplied by fines mass fraction.", "kg/panel", "Stage 4 size rows"),
    "stage4_coarse_mass_kg": ("Modeled feed mass remaining above the assumed screen cut.", "kg/panel", "Stage 4 size rows"),
    "stage4_mass_closure_pct": ("Calculated fine + coarse mass/feed closure; 100% by construction.", "%", "Stage 4 size rows"),
    "stage4_Ag_per_panel_assumed_g": ("Assumed silver mass per panel; not an Agastya feed assay.", "g/panel", "Stage 4 literature Ag rows"),
    "stage4_Ag_reported_to_fines_fraction": ("Published, source-specific Ag fraction applied arithmetically to scenario silver mass.", "fraction", "Stage 4 literature Ag rows"),
    "stage4_Ag_in_fines_scenario_g": ("Assumed panel Ag × published source-specific partition fraction.", "g/panel", "Stage 4 literature Ag rows"),
    "stage4_Ag_feed_grade_scenario_wt_pct": ("Scenario total Ag divided by modeled laminate feed mass; not measured grade.", "wt%", "Stage 4 literature Ag rows"),
    "stage4_fines_yield_assumed_fraction": ("Intentionally blank in the baseline because fines mass yield was unspecified.", "fraction", "Stage 4 literature Ag rows"),
    "stage4_fines_Ag_grade_scenario_wt_pct": ("Intentionally blank in the baseline because fines mass yield was unspecified.", "wt%", "Stage 4 literature Ag rows"),
    "stage4_literature_method": ("Study/feed category associated with the literature partition fraction.", "text", "Stage 4 literature Ag rows"),
}


REGISTER_ROWS = [
    {"experiment_id": "EXP-S2-01", "procedure_id": "PROC-S2-01", "stage": "2", "title": "Manual hand-off mass balance", "record_type": "manual_mass_balance", "method": "Enumerate the panel-mass, frame-share, J-box/cable-share, and task-time assumptions; calculate output-to-Stage-3 mass, closure, and an ideal one-operator 8-hour ceiling.", "inputs": "Panel mass 10–30 kg; frame 7/10/13%; J-box/cable 0.1/0.25/0.5/1%; manual task 120/300/600/900 s.", "conclusion": "Stage 3 input ranges 8.60–27.87 kg/panel; the closure is arithmetic by construction. Capacity is only an ideal one-operator ceiling.", "limits": "No physical weighings, actual task time, electrical isolation, labor variability, or operational throughput."},
    {"experiment_id": "EXP-S3-01", "procedure_id": "PROC-S3-01", "stage": "3", "title": "Glass/laminate material balance", "record_type": "material_mass_balance", "method": "Apply 65/70/75 wt% front-glass assumptions to each Stage 2 scenario; calculate glass and remaining cell/EVA/backsheet laminate masses.", "inputs": "Stage 2 scenario outputs; front-glass share 65/70/75%.", "conclusion": "1,152 scenario splits; input mass is conserved by construction, not measured delamination yield.", "limits": "No module-specific composition, process loss, contamination, or real separation trial."},
    {"experiment_id": "EXP-S3-02", "procedure_id": "PROC-S3-02", "stage": "3", "title": "Hot-knife thermal parameter sweep", "record_type": "thermal_case_summary", "method": "Integrate a five-node one-dimensional thermal RC stack (glass/front EVA/cell/rear EVA/backsheet) under fixed-temperature interface heating and surface convection/radiation.", "inputs": "Tool 180–300 °C; conductance 100–3,000 W/(m²·K); dwell 0.1–10 s; ambient 15/25/35 °C; EVA 0.90/1.16 mm; two literature property sets; interface resistance 0–5×10⁻⁴ m²·K/W; 5 ms step.", "conclusion": "Modeled EVA peaks 15.65–261.53 °C; contact-area heat 1.38 kJ–1.72 MJ/m²; maximum absolute energy residual 9.218×10⁻¹²%.", "limits": "No measured temperatures, heater draw, blade mass, moving front, latent heat, adhesion/fracture, EVA chemistry, fumes, or output quality. Not a validated delamination model."},
    {"experiment_id": "EXP-S3-03", "procedure_id": "PROC-S3-03", "stage": "3", "title": "Representative heating/cooldown traces", "record_type": "thermal_time_trace", "method": "Sample the same five-node model every 0.1 s for 24 combinations of tool temperature, contact conductance, and dwell, with 2 s modeled cooldown.", "inputs": "Tool 180/200/220/300 °C; conductance 100/1,000/3,000 W/(m²·K); dwell 2/10 s; 25 °C ambient; selected property assumptions.", "conclusion": "1,944 time-series rows; trends are governed by assumed contact and layer properties.", "limits": "No actual coupon/panel response and no mechanical peel/roller outcome."},
    {"experiment_id": "EXP-S4-01", "procedure_id": "PROC-S4-01", "stage": "4", "title": "Lognormal size-split sensitivity", "record_type": "lognormal_sieve_sensitivity", "method": "Evaluate the mass-weighted lognormal CDF below an ideal screen cut across every Stage 3 laminate scenario.", "inputs": "D50 0.10–8 mm; GSD 1.4–2.8; cut 0.25/0.50/1/2 mm.", "conclusion": "129,024 rows with fines fraction 0–1, demonstrating sensitivity to unknown particle-size distribution.", "limits": "No measured Agastya PSD, grinder, screen efficiency, liberation, assay, or performance prediction."},
    {"experiment_id": "EXP-S4-02", "procedure_id": "PROC-S4-02", "stage": "4", "title": "Literature-normalized Ag partition arithmetic", "record_type": "literature_Ag_partition_scenario", "method": "Apply source-specific 70/80/94.12% reported Ag-to-fines fractions to 10/20/30 g/panel Ag assumptions and laminate scenarios.", "inputs": "1,152 laminate scenarios; 10/20/30 g Ag per panel; separate study-feed fractions.", "conclusion": "10,368 rows. Baseline product-grade fields remain blank because fines mass yield is unknown.", "limits": "Published feed-specific values are not Agastya recovery; all assumed silver is conditionally assigned to laminate; Stage 3 Ag partition is unknown."},
    {"experiment_id": "EXP-CAP-01", "procedure_id": "PROC-CAP-01", "stage": "CAP", "title": "Stage 2/3 ideal capacity bottleneck", "record_type": "idealized_stage2_stage3_capacity_sensitivity", "method": "Compute 28,800 s divided by assumed manual time and cycle time; multiply Stage 2 per-operator capacity by assumed independent operators; compare Stage 2 team and one Stage 3 station.", "inputs": "Manual task 120/300/600/900 s; operators 1/2/3; Stage 3 cycle 50/60/90 s.", "conclusion": "36 capacity combinations; theoretical bottleneck spans 32–576 panels per 8-hour shift under ideal assumptions.", "limits": "No breaks, transport, WIP, setup, downtime, defects, shared constraints, or measured cycle times."},
    {"experiment_id": "EXP-S3-04", "procedure_id": "PROC-S3-04", "stage": "3", "title": "Thermal timestep convergence", "record_type": "thermal_timestep_convergence", "method": "Re-run eight representative thermal conditions at 10, 5, 2.5, and 1.25 ms integration steps; compare each modeled peak EVA temperature to its 1.25 ms result.", "inputs": "Eight cases spanning tool 180–300 °C, dwell 0.1–10 s, contact conductance, ambient, thickness, property set, and interface resistance.", "conclusion": "32 numerical rows; maximum peak-EVA difference from the finest step is reported in the companion summary.", "limits": "Numerical convergence is not physical validation; the same simplified model and parameters are used at each step."},
    {"experiment_id": "EXP-S3-05", "procedure_id": "PROC-S3-05", "stage": "3", "title": "Modeled retained-heat cooldown", "record_type": "modeled_retained_heat_cooldown", "method": "Heat the five-node stack for an assumed dwell, switch blade contact off, and sample node temperatures and sensible stored heat through 300 s of natural convection/radiation cooling.", "inputs": "Tool 180/200/220/300 °C; dwell 2/10 s; conductance 1,000 W/(m²·K); 25 °C ambient; 0.90 mm EVA; Lizcano property set; 5 ms step.", "conclusion": "64 outputs quantify modeled heat retention and cooling under those boundary assumptions.", "limits": "No roller/work contact, heat transfer efficiency, reuse, adhesion, degradation, process quality, or saved electrical energy is modeled."},
    {"experiment_id": "EXP-S4-03", "procedure_id": "PROC-S4-03", "stage": "4", "title": "Inverse screen-cut targets", "record_type": "inverse_lognormal_screen_target", "method": "Invert the standard normal CDF to find cut = D50 × GSD^z for selected target cumulative fines mass fractions.", "inputs": "D50 0.10–8 mm; GSD 1.4/1.8/2.2/2.8; target fines fraction 5/10/25/50/75/90/95%.", "conclusion": "196 scenario cuts provide candidate aperture values only if the assumed PSD were known and lognormal.", "limits": "No screen efficiency, particle shape, moisture, agglomeration, liberation, or measured PSD."},
    {"experiment_id": "EXP-S4-04", "procedure_id": "PROC-S4-04", "stage": "4", "title": "Conditional Ag grade versus assumed fines yield", "record_type": "conditional_fines_ag_grade_sensitivity", "method": "Combine each laminate scenario with 10/20/30 g Ag inputs, each source-specific literature partition fraction, and five assumed fines mass yields; compute conditional fine mass and grade arithmetic.", "inputs": "1,152 laminate scenarios; three Ag inputs; three literature fractions; fines yields 5/10/20/40/60%.", "conclusion": "51,840 conditional rows show how grade arithmetic changes with an explicitly assumed fines mass yield; no output grade is measured or predicted for Agastya.", "limits": "All scenario Ag assigned to laminate; unknown Stage 3 Ag split; study feeds differ; assumed fines yields are analyst-selected; no assayed feed or product."},
]

CASE_INFO = {
    "EXP-S2-01": (384, "parameter combinations", "Python scenario enumeration and mass-balance arithmetic"),
    "EXP-S3-01": (1152, "mass-balance combinations", "Python composition-based mass-balance arithmetic"),
    "EXP-S3-02": (5040, "thermal parameter combinations", "Custom 1-D five-node RC model; NumPy vectorized explicit forward Euler"),
    "EXP-S3-03": (24, "thermal histories", "Custom 1-D five-node RC model; NumPy explicit forward Euler; 1,944 time snapshots"),
    "EXP-S4-01": (129024, "feed × PSD × cut combinations", "Python math.erf evaluation of the mass-weighted lognormal CDF"),
    "EXP-S4-02": (10368, "literature-normalized arithmetic combinations", "Python arithmetic; literature fractions applied to assumed panel Ag"),
    "EXP-CAP-01": (36, "capacity arithmetic combinations", "Python full-shift capacity and bottleneck arithmetic"),
    "EXP-S3-04": (8, "thermal conditions at four time steps each", "Custom 1-D five-node RC model; NumPy explicit forward Euler refinement"),
    "EXP-S3-05": (8, "thermal conditions at eight cooldown delays each", "Custom 1-D five-node RC model; NumPy explicit forward Euler cooling"),
    "EXP-S4-03": (196, "PSD × target-fraction combinations", "Python statistics.NormalDist inverse CDF"),
    "EXP-S4-04": (51840, "conditional Ag arithmetic combinations", "Python arithmetic combining assumed fines yield and literature partition"),
}


def csv_stats(path, fields):
    counts = Counter()
    mins = defaultdict(lambda: float("inf"))
    maxs = defaultdict(lambda: float("-inf"))
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            counts[row["experiment_id"]] += 1
            for name in fields:
                if row.get(name, ""):
                    value = float(row[name])
                    mins[(row["experiment_id"], name)] = min(mins[(row["experiment_id"], name)], value)
                    maxs[(row["experiment_id"], name)] = max(maxs[(row["experiment_id"], name)], value)
    return counts, mins, maxs


def cooldown_endpoint_stats(path):
    values = {0: [], 300: []}
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            if row.get("experiment_id") == "EXP-S3-05":
                delay = int(float(row["input_cooldown_delay_s"]))
                if delay in values:
                    values[delay].append(float(row["output_total_stack_heat_J_m2"]))
    return {delay: [min(items), max(items)] for delay, items in values.items()}


def main():
    dict_rows = []
    base_units = {name: item[1] for name, item in BASE_DOCS.items()}
    for field in base.FIELDS:
        definition, unit, applies = BASE_DOCS[field]
        dict_rows.append({"field_name": field, "dataset": BASE_CSV.name,
                          "data_type": "numeric" if unit not in ("identifier", "category", "text") else unit,
                          "units": unit, "definition": definition, "applies_to": applies,
                          "missing_value_notes": "Blank means not applicable to this row type or unavailable/withheld by the model; do not interpret blank as zero."})
    for field in follow.FIELDS:
        definition, unit = follow.FIELD_DOCS[field]
        dict_rows.append({"field_name": field, "dataset": FOLLOWUP_CSV.name,
                          "data_type": "numeric" if unit not in ("identifier", "category", "text") else unit,
                          "units": unit, "definition": definition, "applies_to": "follow-up virtual experiments",
                          "missing_value_notes": "Blank means not applicable to this experiment type or unavailable/withheld; it is not zero."})
    with DICTIONARY.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(dict_rows[0]))
        writer.writeheader(); writer.writerows(dict_rows)

    base_counts, base_min, base_max = csv_stats(BASE_CSV, ["stage3_peak_EVA_node_C", "stage3_net_contact_energy_J_m2", "stage4_fines_mass_fraction_model"])
    follow_counts, follow_min, follow_max = csv_stats(FOLLOWUP_CSV, [
        "output_bottleneck_capacity_panels_8h", "output_peak_EVA_delta_from_finest_dt_C",
        "output_total_stack_heat_J_m2", "output_required_screen_cut_mm",
        "output_fines_Ag_grade_scenario_wt_pct",
    ])
    cooldown_endpoints = cooldown_endpoint_stats(FOLLOWUP_CSV)
    base_meta = json.loads(BASE_META.read_text(encoding="utf-8"))
    follow_meta = json.loads(FOLLOWUP_META.read_text(encoding="utf-8"))
    software = base_meta["computation_software"]
    outcome_overrides = {
        "EXP-S3-04": f"Maximum absolute peak-EVA difference from 1.25 ms: {follow_max['EXP-S3-04', 'output_peak_EVA_delta_from_finest_dt_C']:.6g} °C.",
        "EXP-S3-05": f"At contact-off (0 s), modeled stored stack heat spans {cooldown_endpoints[0][0]:.6g}–{cooldown_endpoints[0][1]:.6g} J/m²; at 300 s it spans {cooldown_endpoints[300][0]:.6g}–{cooldown_endpoints[300][1]:.6g} J/m². Heat reuse and transfer are not modeled.",
        "EXP-S4-03": f"Inverse screen cuts span {follow_min['EXP-S4-03', 'output_required_screen_cut_mm']:.6g}–{follow_max['EXP-S4-03', 'output_required_screen_cut_mm']:.6g} mm across the chosen PSD/target combinations.",
        "EXP-S4-04": f"Conditional fine-grade arithmetic spans {follow_min['EXP-S4-04', 'output_fines_Ag_grade_scenario_wt_pct']:.6g}–{follow_max['EXP-S4-04', 'output_fines_Ag_grade_scenario_wt_pct']:.6g} wt% across the analyst-selected fines yields and assumptions; not a performance result.",
        "EXP-CAP-01": f"The idealized bottleneck spans {follow_min['EXP-CAP-01', 'output_bottleneck_capacity_panels_8h']:.6g}–{follow_max['EXP-CAP-01', 'output_bottleneck_capacity_panels_8h']:.6g} panels/8 h.",
    }
    rows = []
    for item in REGISTER_ROWS:
        exp = item["experiment_id"]
        count = base_counts[exp] if exp in base_counts else follow_counts[exp]
        virtual_cases, case_unit, model_class = CASE_INFO[exp]
        thermal_model = exp in {"EXP-S3-02", "EXP-S3-03", "EXP-S3-04", "EXP-S3-05"}
        software_used = (f"{software['python']} and NumPy {software['numpy']}" if thermal_model
                         else f"{software['python']} with the Python standard library")
        outcome = outcome_overrides.get(exp, item["conclusion"])
        rows.append({**item, "software_used": software_used,
                     "model_or_calculation": model_class, "virtual_case_count": virtual_cases,
                     "virtual_case_unit": case_unit, "row_count": count,
                     "physical_sample_count": 0,
                     "physical_sample_units": "panels, coupons, particle samples and assays",
                     "sample_size_note": "Counts are deterministic virtual combinations, model histories or time snapshots; there are zero physical specimens and no statistical sample size.",
                     "dataset_files": f"{BASE_CSV.name}; {FOLLOWUP_CSV.name}" if exp in base_counts and exp in follow_counts else (BASE_CSV.name if exp in base_counts else FOLLOWUP_CSV.name),
                     "outcome": outcome, "evidence_status_summary": "VIRTUAL_OR_SCENARIO_ONLY", "physical_trial_rows": 0})
    with REGISTER.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)

    analysis = {
        "schema_version": "2.0",
        "base_dataset_records": sum(base_counts.values()),
        "followup_dataset_records": sum(follow_counts.values()),
        "total_simulation_or_scenario_records": sum(base_counts.values()) + sum(follow_counts.values()),
        "base_rows_by_experiment": base_counts,
        "followup_rows_by_experiment": follow_counts,
        "data_dictionary_data_rows": len(dict_rows),
        "registered_experiments": len(rows),
        "computation_software": software,
        "followup_computation_software": follow_meta.get("computation_software", {}),
        "physical_trial_rows": 0,
        "base_field_count": len(base.FIELDS),
        "followup_field_count": len(follow.FIELDS),
        "all_rows_carry_experiment_and_procedure_ids": True,
        "numeric_ranges": {
            "base_peak_EVA_temperature_C": [base_min["EXP-S3-02", "stage3_peak_EVA_node_C"], base_max["EXP-S3-02", "stage3_peak_EVA_node_C"]],
            "base_contact_energy_J_m2": [base_min["EXP-S3-02", "stage3_net_contact_energy_J_m2"], base_max["EXP-S3-02", "stage3_net_contact_energy_J_m2"]],
            "base_stage4_fines_fraction": [base_min["EXP-S4-01", "stage4_fines_mass_fraction_model"], base_max["EXP-S4-01", "stage4_fines_mass_fraction_model"]],
            "followup_ideal_capacity_panels_8h": [follow_min["EXP-CAP-01", "output_bottleneck_capacity_panels_8h"], follow_max["EXP-CAP-01", "output_bottleneck_capacity_panels_8h"]],
            "followup_max_dt_peak_EVA_delta_C": follow_max["EXP-S3-04", "output_peak_EVA_delta_from_finest_dt_C"],
            "followup_cooldown_heat_J_m2": [follow_min["EXP-S3-05", "output_total_stack_heat_J_m2"], follow_max["EXP-S3-05", "output_total_stack_heat_J_m2"]],
            "followup_cooldown_heat_at_contact_off_J_m2": cooldown_endpoints[0],
            "followup_cooldown_heat_after_300s_J_m2": cooldown_endpoints[300],
            "followup_inverse_screen_cut_mm": [follow_min["EXP-S4-03", "output_required_screen_cut_mm"], follow_max["EXP-S4-03", "output_required_screen_cut_mm"]],
            "followup_conditional_fines_grade_wt_pct": [follow_min["EXP-S4-04", "output_fines_Ag_grade_scenario_wt_pct"], follow_max["EXP-S4-04", "output_fines_Ag_grade_scenario_wt_pct"]],
        },
        "note": "Every row is virtual, scenario, or literature-normalized arithmetic. It contains zero physical Agastya trial measurements.",
    }
    ANALYSIS.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()
