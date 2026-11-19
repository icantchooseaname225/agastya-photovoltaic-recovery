"""Follow-up virtual sensitivity experiments for the Agastya process study.

These are numerical or arithmetic studies only. No equipment is operated and
no Agastya measurements are synthesized. Inputs remain explicit scenarios.
"""

from __future__ import annotations

import csv
import importlib.util
import itertools
import json
import math
import platform
from pathlib import Path
from statistics import NormalDist

import numpy as np


ROOT = Path(__file__).resolve().parent
BASE_SCRIPT = ROOT / "Agastya_Physics_Simulation_2026-10-10.py"
FOLLOWUP_CSV = ROOT / "followup_virtual_experiments.csv"
META_PATH = ROOT / "followup_virtual_experiments_metadata.json"
SUMMARY_PATH = ROOT / "followup_virtual_experiments_summary.json"

spec = importlib.util.spec_from_file_location("agastya_base_sim", BASE_SCRIPT)
base = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(base)


FIELDS = [
    "record_id", "experiment_id", "procedure_id", "stage", "record_type",
    "evidence_status", "scenario_id", "source_basis",
    "input_stage2_manual_time_s", "input_stage2_operators",
    "input_stage3_cycle_time_s", "output_stage2_capacity_panels_8h_team",
    "output_stage3_capacity_panels_8h_station", "output_bottleneck_capacity_panels_8h",
    "input_tool_temperature_C", "input_contact_conductance_W_m2K",
    "input_contact_duration_s", "input_ambient_C", "input_EVA_total_thickness_mm",
    "input_property_set", "input_interface_resistance_m2K_W", "input_timestep_s",
    "output_peak_EVA_temperature_C", "output_peak_cell_temperature_C",
    "output_energy_balance_error_pct", "output_peak_EVA_delta_from_finest_dt_C",
    "input_cooldown_delay_s", "output_glass_temperature_C",
    "output_EVA_front_temperature_C", "output_cell_temperature_C",
    "output_EVA_rear_temperature_C", "output_backsheet_temperature_C",
    "output_stored_EVA_heat_J_m2", "output_stored_cell_heat_J_m2",
    "output_total_stack_heat_J_m2", "input_PSD_D50_mm", "input_PSD_GSD",
    "input_target_fines_fraction", "output_required_screen_cut_mm",
    "input_panel_Ag_scenario_g", "input_literature_Ag_partition_fraction",
    "input_fines_mass_yield_assumed_fraction", "input_laminate_feed_mass_kg",
    "output_laminate_Ag_feed_grade_scenario_wt_pct", "output_Ag_in_fines_scenario_g",
    "output_fines_mass_kg", "output_fines_Ag_grade_scenario_wt_pct",
]

FIELD_DOCS = {
    "record_id": ("Unique row identifier, prefixed F for follow-up data.", "identifier"),
    "experiment_id": ("Experiment register key; identifies the virtual study represented by this row.", "identifier"),
    "procedure_id": ("Procedure key; links to the repeatable method in PROCEDURES_AND_RESULTS.md.", "identifier"),
    "stage": ("Agastya process stage or CAP for the cross-stage capacity calculation.", "category"),
    "record_type": ("Follow-up study output type.", "category"),
    "evidence_status": ("Evidence class. These follow-up rows are virtual, scenario, or conditional arithmetic outputs; none are measurements.", "category"),
    "scenario_id": ("Readable combination key for input settings.", "identifier"),
    "source_basis": ("Compact per-row statement of assumptions and limits; see procedure record for full context.", "text"),
    "input_stage2_manual_time_s": ("Assumed Stage 2 manual task time per panel.", "s/panel"),
    "input_stage2_operators": ("Assumed number of independent Stage 2 operators.", "operators"),
    "input_stage3_cycle_time_s": ("Assumed Stage 3 station cycle time per panel.", "s/panel"),
    "output_stage2_capacity_panels_8h_team": ("Ideal full-shift Stage 2 team capacity, operators × 28,800 s / task time.", "panels/8 h"),
    "output_stage3_capacity_panels_8h_station": ("Ideal full-shift capacity of one Stage 3 station.", "panels/8 h"),
    "output_bottleneck_capacity_panels_8h": ("Lower of assumed Stage 2 team and one Stage 3 station capacities, assuming parallel operation and unrestricted feed.", "panels/8 h"),
    "input_tool_temperature_C": ("Assumed fixed hot-knife boundary temperature.", "°C"),
    "input_contact_conductance_W_m2K": ("Assumed blade-to-workpiece contact conductance.", "W/(m²·K)"),
    "input_contact_duration_s": ("Assumed local blade contact duration; distinct from whole-panel line cycle.", "s"),
    "input_ambient_C": ("Assumed surrounding air temperature.", "°C"),
    "input_EVA_total_thickness_mm": ("Assumed total thickness of front and rear EVA layers.", "mm"),
    "input_property_set": ("Named literature table used for thermal material properties.", "identifier"),
    "input_interface_resistance_m2K_W": ("Assumed thermal resistance at each modeled layer interface.", "m²·K/W"),
    "input_timestep_s": ("Numerical integration time step.", "s"),
    "output_peak_EVA_temperature_C": ("Maximum modeled temperature across the two EVA nodes during heating.", "°C"),
    "output_peak_cell_temperature_C": ("Maximum modeled silicon-cell node temperature during heating.", "°C"),
    "output_energy_balance_error_pct": ("Integrated input-minus-loss-minus-stored-energy residual relative to modeled blade input.", "%"),
    "output_peak_EVA_delta_from_finest_dt_C": ("Absolute peak-EVA difference from the finest time step for the same convergence case.", "°C"),
    "input_cooldown_delay_s": ("Time elapsed after the assumed blade contact ends.", "s"),
    "output_glass_temperature_C": ("Modeled glass-node temperature at the cooldown delay.", "°C"),
    "output_EVA_front_temperature_C": ("Modeled front EVA-node temperature at the cooldown delay.", "°C"),
    "output_cell_temperature_C": ("Modeled silicon-cell node temperature at the cooldown delay.", "°C"),
    "output_EVA_rear_temperature_C": ("Modeled rear EVA-node temperature at the cooldown delay.", "°C"),
    "output_backsheet_temperature_C": ("Modeled backsheet-node temperature at the cooldown delay.", "°C"),
    "output_stored_EVA_heat_J_m2": ("Modeled sensible heat above ambient stored in both EVA nodes.", "J/m²"),
    "output_stored_cell_heat_J_m2": ("Modeled sensible heat above ambient stored in the cell node.", "J/m²"),
    "output_total_stack_heat_J_m2": ("Modeled sensible heat above ambient across all five layer nodes.", "J/m²"),
    "input_PSD_D50_mm": ("Assumed median of a mass-weighted lognormal particle-size distribution.", "mm"),
    "input_PSD_GSD": ("Assumed geometric standard deviation of the lognormal particle-size distribution.", "dimensionless"),
    "input_target_fines_fraction": ("Target cumulative mass fraction below the selected screen cut.", "fraction"),
    "output_required_screen_cut_mm": ("Inverse-lognormal screen cut associated with the target fines fraction.", "mm"),
    "input_panel_Ag_scenario_g": ("Assumed total Ag input per panel; all is conditionally assigned to the Stage 4 laminate.", "g/panel"),
    "input_literature_Ag_partition_fraction": ("Source-specific literature Ag fraction applied arithmetically to the scenario feed.", "fraction"),
    "input_fines_mass_yield_assumed_fraction": ("Analyst-selected fines mass fraction used only to calculate a conditional grade.", "fraction"),
    "input_laminate_feed_mass_kg": ("Scenario laminate feed mass passed into the conditional Stage 4 calculation.", "kg/panel"),
    "output_laminate_Ag_feed_grade_scenario_wt_pct": ("Scenario total Ag divided by laminate feed mass; not measured feed assay.", "wt%"),
    "output_Ag_in_fines_scenario_g": ("Scenario Ag mass assigned to fines using the source-specific partition fraction.", "g/panel"),
    "output_fines_mass_kg": ("Assumed fines mass yield multiplied by scenario laminate feed mass.", "kg/panel"),
    "output_fines_Ag_grade_scenario_wt_pct": ("Conditional Ag mass in fines divided by assumed fines mass; not measured product grade.", "wt%"),
}


def clean(value):
    if value is None:
        return ""
    if isinstance(value, (float, np.floating)):
        if not math.isfinite(float(value)):
            return ""
        return f"{float(value):.9g}"
    if isinstance(value, (int, np.integer)):
        return int(value)
    return value


def emit(writer, row_number, experiment_id, procedure_id, **values):
    row = {name: "" for name in FIELDS}
    row.update(record_id=f"F{row_number:07d}", experiment_id=experiment_id,
               procedure_id=procedure_id, **values)
    writer.writerow({key: clean(value) for key, value in row.items()})


def thermal_convergence_rows(writer, start):
    cases = [
        (180, 100, 0.5, 15, 0.90, "Lizcano2024_A1", 0),
        (200, 1000, 2, 25, 0.90, "Lizcano2024_A1", 1e-4),
        (220, 300, 5, 35, 1.16, "Tomsic2025_Table1", 1e-4),
        (250, 3000, 1, 25, 0.90, "Tomsic2025_Table1", 5e-4),
        (300, 1000, 10, 15, 1.16, "Lizcano2024_A1", 0),
        (300, 3000, 10, 35, 1.16, "Tomsic2025_Table1", 5e-4),
        (220, 1000, 0.1, 25, 0.90, "Lizcano2024_A1", 5e-4),
        (200, 300, 0.5, 15, 1.16, "Tomsic2025_Table1", 0),
    ]
    steps = (0.01, 0.005, 0.0025, 0.00125)
    row_number = start
    deltas = []
    for case_no, (tool, hc, duration, ambient, eva_mm, prop, rint) in enumerate(cases, 1):
        thermal_case = {"tool": tool, "hc": hc, "duration": duration, "ambient": ambient,
                        "eva_mm": eva_mm, "property_set": prop, "rint": rint}
        results = []
        for dt in steps:
            out = base.simulate_thermal_batch([thermal_case], dt)
            peak_eva = float(max(out["peak"][0, 1], out["peak"][0, 3]))
            peak_cell = float(out["peak"][0, 2])
            results.append((dt, peak_eva, peak_cell, float(out["energy_error_pct"][0])))
        finest_peak = results[-1][1]
        for dt, peak_eva, peak_cell, error in results:
            delta = abs(peak_eva - finest_peak)
            deltas.append(delta)
            row_number += 1
            emit(writer, row_number, "EXP-S3-04", "PROC-S3-04", stage="3",
                 record_type="thermal_timestep_convergence", evidence_status="NUMERICAL_MODEL_ASSUMPTIONS",
                 scenario_id=f"S3CONV-{case_no:02d}-DT{dt:g}",
                 source_basis="Numerical time-step refinement of the five-node model; convergence check only, not validation against measured temperatures.",
                 input_tool_temperature_C=tool, input_contact_conductance_W_m2K=hc,
                 input_contact_duration_s=duration, input_ambient_C=ambient,
                 input_EVA_total_thickness_mm=eva_mm, input_property_set=prop,
                 input_interface_resistance_m2K_W=rint, input_timestep_s=dt,
                 output_peak_EVA_temperature_C=peak_eva,
                 output_peak_cell_temperature_C=peak_cell,
                 output_energy_balance_error_pct=error,
                 output_peak_EVA_delta_from_finest_dt_C=delta)
    return row_number, {"case_count": len(cases), "time_steps_s": list(steps),
                        "max_abs_peak_EVA_delta_from_finest_dt_C": max(deltas)}


def retained_heat_rows(writer, start):
    row_number = start
    delays = (0, 1, 5, 10, 30, 60, 120, 300)
    for tool, duration in itertools.product((180, 200, 220, 300), (2, 10)):
        case = {"tool": tool, "hc": 1000, "duration": duration, "ambient": 25,
                "eva_mm": 0.90, "property_set": "Lizcano2024_A1", "rint": 1e-4}
        matrices = base.thermal_matrix(case)
        state = (*matrices[:6], matrices[6], 0.0, 0.0)
        peak_eva = np.array(state[6], copy=True)
        peak_cell = float(state[6][2])
        steps = int(round(duration / base.DT_S))
        for _ in range(steps):
            state, _, _ = base.thermal_step(case, state, base.DT_S, blade_on=True)
            peak_eva = np.maximum(peak_eva, state[6])
            peak_cell = max(peak_cell, float(state[6][2]))
        peak_eva_value = float(max(peak_eva[1], peak_eva[3]))
        elapsed = 0.0
        for delay in delays:
            for _ in range(int(round((delay - elapsed) / base.DT_S))):
                state, _, _ = base.thermal_step(case, state, base.DT_S, blade_on=False)
            elapsed = delay
            d, _, capacity, _, _, _, temperatures, _, _ = state
            # Capacity and node temperatures both use the one-square-metre basis.
            eva_heat = float(capacity[1] * (temperatures[1] - case["ambient"])
                             + capacity[3] * (temperatures[3] - case["ambient"]))
            cell_heat = float(capacity[2] * (temperatures[2] - case["ambient"]))
            total_heat = float(np.sum(capacity * (temperatures - case["ambient"])))
            row_number += 1
            emit(writer, row_number, "EXP-S3-05", "PROC-S3-05", stage="3",
                 record_type="modeled_retained_heat_cooldown", evidence_status="NUMERICAL_MODEL_ASSUMPTIONS",
                 scenario_id=f"S3COOL-T{tool}-D{duration}-L{delay}",
                 source_basis="Five-node model after the assumed blade switches off; sensible heat only. No roller, work transfer, reuse, adhesion or degradation response is modeled.",
                 input_tool_temperature_C=tool, input_contact_conductance_W_m2K=case["hc"],
                 input_contact_duration_s=duration, input_ambient_C=case["ambient"],
                 input_EVA_total_thickness_mm=case["eva_mm"], input_property_set=case["property_set"],
                 input_interface_resistance_m2K_W=case["rint"], input_timestep_s=base.DT_S,
                 output_peak_EVA_temperature_C=peak_eva_value,
                 output_peak_cell_temperature_C=peak_cell, input_cooldown_delay_s=delay,
                 output_glass_temperature_C=float(temperatures[0]),
                 output_EVA_front_temperature_C=float(temperatures[1]),
                 output_cell_temperature_C=float(temperatures[2]),
                 output_EVA_rear_temperature_C=float(temperatures[3]),
                 output_backsheet_temperature_C=float(temperatures[4]),
                 output_stored_EVA_heat_J_m2=eva_heat,
                 output_stored_cell_heat_J_m2=cell_heat,
                 output_total_stack_heat_J_m2=total_heat)
    return row_number


def screen_target_rows(writer, start):
    row_number = start
    normal = NormalDist()
    for d50, gsd, target in itertools.product(
        (0.10, 0.25, 0.50, 1, 2, 4, 8), (1.4, 1.8, 2.2, 2.8),
        (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95),
    ):
        cut = d50 * math.exp(math.log(gsd) * normal.inv_cdf(target))
        row_number += 1
        emit(writer, row_number, "EXP-S4-03", "PROC-S4-03", stage="4",
             record_type="inverse_lognormal_screen_target", evidence_status="SCENARIO_ONLY",
             scenario_id=f"S4CUT-D{d50:g}-G{gsd:g}-F{target:g}",
             source_basis="Inverse CDF for an assumed mass-weighted lognormal PSD; cut is a scenario calculation and ignores screen efficiency and material liberation.",
             input_PSD_D50_mm=d50, input_PSD_GSD=gsd,
             input_target_fines_fraction=target, output_required_screen_cut_mm=cut)
    return row_number


def conditional_ag_grade_rows(writer, start):
    row_number = start
    s2 = list(base.stage2_scenarios())
    s3 = list(base.stage3_material_scenarios(s2))
    yields = (0.05, 0.10, 0.20, 0.40, 0.60)
    for feed in s3:
        laminate_kg = feed["stage3_laminate_mass_kg"]
        for ag_g, (partition, method, description), fines_yield in itertools.product(
            (10, 20, 30), base.LITERATURE_PARTITIONS, yields
        ):
            ag_in_fines_g = ag_g * partition
            fines_kg = laminate_kg * fines_yield
            grade_pct = 100 * ag_in_fines_g / (fines_kg * 1000)
            row_number += 1
            emit(writer, row_number, "EXP-S4-04", "PROC-S4-04", stage="4",
                 record_type="conditional_fines_ag_grade_sensitivity",
                 evidence_status="CONDITIONAL_LITERATURE_NORMALIZED_SCENARIO",
                 scenario_id=f"S4GRADE-{feed['scenario_id']}-Ag{ag_g}-{method}-Y{fines_yield:g}",
                 source_basis=(f"Conditional arithmetic only. Assumes {ag_g} g Ag/panel all enters the laminate, applies {partition:.4g} from {method}, and assumes the listed fines mass yield. {description}; no Agastya feed assay or Stage 3 Ag partition is known."),
                 input_panel_Ag_scenario_g=ag_g,
                 input_literature_Ag_partition_fraction=partition,
                 input_fines_mass_yield_assumed_fraction=fines_yield,
                 input_laminate_feed_mass_kg=laminate_kg,
                 output_laminate_Ag_feed_grade_scenario_wt_pct=100 * ag_g / (laminate_kg * 1000),
                 output_Ag_in_fines_scenario_g=ag_in_fines_g,
                 output_fines_mass_kg=fines_kg,
                 output_fines_Ag_grade_scenario_wt_pct=grade_pct)
    return row_number, len(s3)


def capacity_rows(writer, start):
    row_number = start
    seconds_per_shift = 8 * 3600
    for manual_time, operators, cycle in itertools.product((120, 300, 600, 900), (1, 2, 3), (50, 60, 90)):
        stage2_team = operators * seconds_per_shift / manual_time
        stage3_station = seconds_per_shift / cycle
        row_number += 1
        emit(writer, row_number, "EXP-CAP-01", "PROC-CAP-01", stage="CAP",
             record_type="idealized_stage2_stage3_capacity_sensitivity",
             evidence_status="ARITHMETIC_SCENARIO_ONLY",
             scenario_id=f"CAP-S2T{manual_time}-OP{operators}-S3T{cycle}",
             source_basis="Ideal 8-hour arithmetic ceiling: no breaks, transport, setup, defects, shared-resource limits, downtime, safety controls, or measured cycle times.",
             input_stage2_manual_time_s=manual_time, input_stage2_operators=operators,
             input_stage3_cycle_time_s=cycle,
             output_stage2_capacity_panels_8h_team=stage2_team,
             output_stage3_capacity_panels_8h_station=stage3_station,
             output_bottleneck_capacity_panels_8h=min(stage2_team, stage3_station))
    return row_number


def main():
    assert set(FIELD_DOCS) == set(FIELDS), "Follow-up data dictionary must cover every CSV column exactly."
    counts = {}
    row_number = 0
    with FOLLOWUP_CSV.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        row_number = capacity_rows(writer, row_number)
        counts["EXP-CAP-01"] = 36
        row_number, convergence = thermal_convergence_rows(writer, row_number)
        counts["EXP-S3-04"] = 32
        row_number = retained_heat_rows(writer, row_number)
        counts["EXP-S3-05"] = 64
        row_number = screen_target_rows(writer, row_number)
        counts["EXP-S4-03"] = 196
        row_number, s3_count = conditional_ag_grade_rows(writer, row_number)
        counts["EXP-S4-04"] = s3_count * 3 * len(base.LITERATURE_PARTITIONS) * 5

    summary = {
        "generated_on": "2026-10-10",
        "dataset_path": FOLLOWUP_CSV.name,
        "computation_software": {
            "python": f"CPython {platform.python_version()}",
            "numpy": np.__version__,
            "python_standard_library": ["csv", "json", "itertools", "math", "statistics.NormalDist", "importlib.util"],
            "solver": "Custom five-node 1-D thermal resistance/capacitance model with explicit forward Euler for thermal studies; Python standard-library scenario arithmetic for capacity, inverse lognormal cuts and conditional Ag calculations.",
        },
        "total_records": row_number,
        "record_counts_by_experiment": counts,
        "stage3_convergence": convergence,
        "conditional_ag_grade": {
            "base_laminate_scenarios": s3_count,
            "panel_Ag_inputs_g": [10, 20, 30],
            "literature_partition_fractions": [x[0] for x in base.LITERATURE_PARTITIONS],
            "assumed_fines_mass_yields": [0.05, 0.10, 0.20, 0.40, 0.60],
        },
        "all_values_are_virtual_model_or_scenario_calculations": True,
        "physical_sample_count": 0,
        "scenario_rows_are_physical_samples": False,
        "measured_Agastya_trial_rows": 0,
    }
    META_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
