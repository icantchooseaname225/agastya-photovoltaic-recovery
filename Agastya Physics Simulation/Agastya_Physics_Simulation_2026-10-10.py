"""Reproducible, assumption-labelled Agastya process sensitivity simulation.

Historical virtual design-study model, not an experiment or validated machine.
Uses legacy stage numbering; outputs are assumptions/scenarios, not samples.
It creates one consolidated CSV containing Stage 2/3/4 scenario outputs.
"""

from __future__ import annotations

import csv
import itertools
import json
import math
import platform
from collections import defaultdict
from datetime import date
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
DATE_TAG = "2026-10-10"
CSV_PATH = ROOT / f"Agastya_Physics_Simulation_{DATE_TAG}.csv"
REPORT_PATH = ROOT / f"Agastya_Physics_Simulation_{DATE_TAG}.md"
META_PATH = ROOT / f"Agastya_Physics_Simulation_{DATE_TAG}_metadata.json"

SIGMA = 5.670374419e-8
DT_S = 0.005

FIELDS = [
    "record_id", "experiment_id", "procedure_id", "stage", "record_type", "evidence_status", "scenario_id",
    "source_basis", "ambient_C", "panel_mass_kg",
    "stage2_frame_share_pct", "stage2_jbox_cable_share_pct", "stage2_manual_time_s",
    "stage2_frame_mass_kg", "stage2_jbox_cable_mass_kg", "stage2_input_mass_kg",
    "stage2_output_to_stage3_kg", "stage2_mass_closure_pct",
    "stage2_operator_capacity_panels_8h",
    "stage3_glass_share_of_original_pct", "stage3_input_mass_kg",
    "stage3_front_glass_mass_kg", "stage3_laminate_mass_kg", "stage3_mass_closure_pct",
    "stage3_material_property_set", "stage3_blade_setpoint_C",
    "stage3_contact_conductance_W_m2K", "stage3_contact_duration_s",
    "stage3_EVA_total_thickness_mm", "stage3_backsheet_thickness_mm",
    "stage3_interface_resistance_m2K_W", "stage3_time_s",
    "stage3_T_interface_C", "stage3_T_glass_node_C", "stage3_T_EVA_front_node_C",
    "stage3_T_cell_node_C", "stage3_T_EVA_rear_node_C", "stage3_T_backsheet_node_C",
    "stage3_peak_EVA_node_C", "stage3_peak_cell_node_C",
    "stage3_net_contact_energy_J_m2", "stage3_time_above_100C_s",
    "stage3_time_above_140C_s", "stage3_time_above_180C_s",
    "stage3_time_above_220C_s", "stage3_time_above_280C_s",
    "stage3_energy_balance_error_pct",
    "stage4_feed_mass_kg", "stage4_particle_mass_D50_mm",
    "stage4_particle_geometric_SD", "stage4_screen_cut_mm",
    "stage4_fines_mass_fraction_model", "stage4_fines_mass_kg",
    "stage4_coarse_mass_kg", "stage4_mass_closure_pct",
    "stage4_Ag_per_panel_assumed_g", "stage4_Ag_reported_to_fines_fraction",
    "stage4_Ag_in_fines_scenario_g", "stage4_Ag_feed_grade_scenario_wt_pct",
    "stage4_fines_yield_assumed_fraction", "stage4_fines_Ag_grade_scenario_wt_pct",
    "stage4_literature_method",
]


def clean(value):
    if value is None:
        return ""
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.8g}"
    return value


def write_row(writer, record_id, **values):
    row = {name: "" for name in FIELDS}
    row.update(record_id=record_id, **values)
    writer.writerow({key: clean(value) for key, value in row.items()})


def stage2_scenarios():
    panel_masses = [10, 12, 15, 18, 20, 24, 28, 30]
    frame_shares = [0.07, 0.10, 0.13]
    jb_cable_shares = [0.001, 0.0025, 0.005, 0.01]
    manual_times = [120, 300, 600, 900]
    for i, (mass, frame_share, jb_share, seconds) in enumerate(
        itertools.product(panel_masses, frame_shares, jb_cable_shares, manual_times), start=1
    ):
        frame_kg = mass * frame_share
        jb_kg = mass * jb_share
        stage3_feed = mass - frame_kg - jb_kg
        yield {
            "scenario_id": f"S2-{i:04d}",
            "panel_mass_kg": mass,
            "stage2_frame_share_pct": frame_share * 100,
            "stage2_jbox_cable_share_pct": jb_share * 100,
            "stage2_manual_time_s": seconds,
            "stage2_frame_mass_kg": frame_kg,
            "stage2_jbox_cable_mass_kg": jb_kg,
            "stage2_input_mass_kg": mass,
            "stage2_output_to_stage3_kg": stage3_feed,
            "stage2_mass_closure_pct": 100 * (frame_kg + jb_kg + stage3_feed) / mass,
            "stage2_operator_capacity_panels_8h": 8 * 3600 / seconds,
            "source_basis": (
                "Scenario only. Thesis Figure 3.1 gives 10 wt% aluminium frame as a central composition; "
                "7-13 wt% is an analyst sensitivity. Junction-box/external-cable fraction and manual time "
                "are analyst-selected ranges, not measured. Thesis 1 wt% copper includes module wiring, "
                "not just Stage 2 removable cable. Current project Stage 2 is supervised manual hand-off."
            ),
        }


def stage3_material_scenarios(s2_rows):
    for s2 in s2_rows:
        for glass_share in (0.65, 0.70, 0.75):
            glass_kg = s2["panel_mass_kg"] * glass_share
            laminate_kg = s2["stage2_output_to_stage3_kg"] - glass_kg
            if laminate_kg <= 0:
                continue
            yield {
                "scenario_id": f"S3M-{s2['scenario_id'][3:]}-G{int(glass_share*100)}",
                "panel_mass_kg": s2["panel_mass_kg"],
                "stage2_frame_share_pct": s2["stage2_frame_share_pct"],
                "stage2_jbox_cable_share_pct": s2["stage2_jbox_cable_share_pct"],
                "stage2_input_mass_kg": s2["stage2_input_mass_kg"],
                "stage2_output_to_stage3_kg": s2["stage2_output_to_stage3_kg"],
                "stage3_glass_share_of_original_pct": glass_share * 100,
                "stage3_input_mass_kg": s2["stage2_output_to_stage3_kg"],
                "stage3_front_glass_mass_kg": glass_kg,
                "stage3_laminate_mass_kg": laminate_kg,
                "stage3_mass_closure_pct": 100 * (glass_kg + laminate_kg) / s2["stage2_output_to_stage3_kg"],
                "source_basis": (
                    "Scenario only. Thesis Figure 3.1 gives 70 wt% front glass as a central composition; "
                    "65-75 wt% is an analyst sensitivity. Stage 3 mass split is a composition-based "
                    "mass-balance illustration, not a measured delamination yield."
                ),
            }


PROPERTY_SETS = {
    "Lizcano2024_A1": {
        "glass_k": 1.8, "glass_rho": 3000, "glass_cp": 500,
        "eva_k": 0.35, "eva_rho": 960, "eva_cp": 2090,
        "si_k": 148, "si_rho": 2330, "si_cp": 677,
        "bs_k": 0.20, "bs_rho": 1200, "bs_cp": 1250, "bs_mm": 0.10,
    },
    "Tomsic2025_Table1": {
        "glass_k": 1.40, "glass_rho": 2210, "glass_cp": 730,
        "eva_k": 0.34, "eva_rho": 951, "eva_cp": 1400,
        "si_k": 130, "si_rho": 2329, "si_cp": 700,
        "bs_k": 0.19, "bs_rho": 1430, "bs_cp": 1550, "bs_mm": 0.34,
    },
}


def thermal_matrix(case, active=True):
    """One-dimensional five-node thermal RC model, all energies per contact area."""
    pset = PROPERTY_SETS[case["property_set"]]
    eva_total_m = case["eva_mm"] / 1000
    d = np.array([0.0032, eva_total_m / 2, 0.00021, eva_total_m / 2, pset["bs_mm"] / 1000])
    k = np.array([pset["glass_k"], pset["eva_k"], pset["si_k"], pset["eva_k"], pset["bs_k"]])
    rhocp = np.array([
        pset["glass_rho"] * pset["glass_cp"],
        pset["eva_rho"] * pset["eva_cp"],
        pset["si_rho"] * pset["si_cp"],
        pset["eva_rho"] * pset["eva_cp"],
        pset["bs_rho"] * pset["bs_cp"],
    ])
    C = rhocp * d
    g_between = np.empty(4)
    for j in range(4):
        r = d[j] / (2 * k[j]) + d[j + 1] / (2 * k[j + 1]) + case["rint"]
        g_between[j] = 1 / r
    # The blade contacts the glass/EVA interface. Its heat splits into two
    # parallel paths through the half-thickness resistance of glass and EVA.
    r_glass_half = d[0] / (2 * k[0])
    r_eva_half = d[1] / (2 * k[1])
    T = np.full(5, case["ambient"], dtype=float)
    return d, k, C, g_between, r_glass_half, r_eva_half, T


def thermal_step(case, state, dt, blade_on=True):
    d, k, C, g, rgh, reh, T, Ein, Qloss = state
    pset = PROPERTY_SETS[case["property_set"]]
    Tamb = case["ambient"]
    if blade_on:
        h = case["hc"]
        gg = 1 / rgh
        ge = 1 / reh
        Tif = (h * case["tool"] + gg * T[0] + ge * T[1]) / (h + gg + ge)
        q_blade = h * (case["tool"] - Tif)
        q_glass = (Tif - T[0]) * gg
        q_eva = (Tif - T[1]) * ge
    else:
        Tif = T[1]
        q_blade = q_glass = q_eva = 0.0

    q_surface_front = 8.0 * (T[0] - Tamb) + 0.85 * SIGMA * ((T[0] + 273.15) ** 4 - (Tamb + 273.15) ** 4)
    q_surface_back = 8.0 * (T[4] - Tamb) + 0.93 * SIGMA * ((T[4] + 273.15) ** 4 - (Tamb + 273.15) ** 4)
    flows = np.zeros(5)
    flows[0] += q_glass - q_surface_front
    flows[1] += q_eva
    for j in range(4):
        q = g[j] * (T[j + 1] - T[j])
        flows[j] += q
        flows[j + 1] -= q
    flows[4] -= q_surface_back
    Tnew = T + dt * flows / C
    Ein_new = Ein + (q_blade * dt if blade_on else 0.0)
    Qloss_new = Qloss + (q_surface_front + q_surface_back) * dt
    new_state = (d, k, C, g, rgh, reh, Tnew, Ein_new, Qloss_new)
    return new_state, Tif, q_blade


def simulate_thermal_batch(cases, dt=DT_S):
    """Vectorized batch integration for cases with the same contact duration."""
    n = len(cases)
    tools = np.array([c["tool"] for c in cases])
    amb = np.array([c["ambient"] for c in cases])
    hc = np.array([c["hc"] for c in cases])
    eva_mm = np.array([c["eva_mm"] for c in cases])
    prop_names = [c["property_set"] for c in cases]
    duration = cases[0]["duration"]
    assert all(c["duration"] == duration for c in cases)

    d = np.zeros((n, 5)); k = np.zeros((n, 5)); C = np.zeros((n, 5))
    g = np.zeros((n, 4)); rgh = np.zeros(n); reh = np.zeros(n)
    rint = np.array([c["rint"] for c in cases])
    for i, (c, name) in enumerate(zip(cases, prop_names)):
        p = PROPERTY_SETS[name]
        d[i] = [0.0032, eva_mm[i] / 2000, 0.00021, eva_mm[i] / 2000, p["bs_mm"] / 1000]
        k[i] = [p["glass_k"], p["eva_k"], p["si_k"], p["eva_k"], p["bs_k"]]
        cpv = [p["glass_rho"] * p["glass_cp"], p["eva_rho"] * p["eva_cp"],
               p["si_rho"] * p["si_cp"], p["eva_rho"] * p["eva_cp"], p["bs_rho"] * p["bs_cp"]]
        C[i] = d[i] * cpv
        for j in range(4):
            g[i, j] = 1 / (d[i, j] / (2 * k[i, j]) + d[i, j + 1] / (2 * k[i, j + 1]) + rint[i])
        rgh[i] = d[i, 0] / (2 * k[i, 0])
        reh[i] = d[i, 1] / (2 * k[i, 1])

    T = np.repeat(amb[:, None], 5, axis=1).astype(float)
    peak = T.copy()
    Ein = np.zeros(n)
    Qloss = np.zeros(n)
    above = {x: np.zeros(n) for x in (100, 140, 180, 220, 280)}
    max_steps = int(round(duration / dt))
    gglass = 1 / rgh
    geva = 1 / reh
    for _ in range(max_steps):
        Tif = (hc * tools + gglass * T[:, 0] + geva * T[:, 1]) / (hc + gglass + geva)
        q_blade = hc * (tools - Tif)
        q_glass = (Tif - T[:, 0]) * gglass
        q_eva = (Tif - T[:, 1]) * geva
        qfront = 8 * (T[:, 0] - amb) + 0.85 * SIGMA * ((T[:, 0] + 273.15) ** 4 - (amb + 273.15) ** 4)
        qback = 8 * (T[:, 4] - amb) + 0.93 * SIGMA * ((T[:, 4] + 273.15) ** 4 - (amb + 273.15) ** 4)
        f = np.zeros_like(T)
        f[:, 0] += q_glass - qfront
        f[:, 1] += q_eva
        for j in range(4):
            q = g[:, j] * (T[:, j + 1] - T[:, j])
            f[:, j] += q
            f[:, j + 1] -= q
        f[:, 4] -= qback
        T += dt * f / C
        Ein += q_blade * dt
        Qloss += (qfront + qback) * dt
        peak = np.maximum(peak, T)
        eva_peak_now = np.maximum(T[:, 1], T[:, 3])
        for threshold in above:
            above[threshold] += dt * (eva_peak_now >= threshold)

    Tif_final = (hc * tools + gglass * T[:, 0] + geva * T[:, 1]) / (hc + gglass + geva)
    stored = np.sum(C * (T - amb[:, None]), axis=1)
    error = Ein - Qloss - stored
    denom = np.maximum(np.abs(Ein), 1e-9)
    return {
        "T": T, "peak": peak, "Tif": Tif_final, "Ein": Ein,
        "Qloss": Qloss, "energy_error_pct": 100 * error / denom,
        "above": above,
    }


def thermal_cases():
    property_names = list(PROPERTY_SETS)
    keys = ("tool", "hc", "duration", "ambient", "eva_mm", "property_set", "rint")
    products = itertools.product(
        (180, 200, 220, 250, 300),
        (100, 300, 1000, 3000),
        (0.1, 0.25, 0.5, 1, 2, 5, 10),
        (15, 25, 35),
        (0.90, 1.16),
        property_names,
        (0.0, 1e-4, 5e-4),
    )
    grouped = defaultdict(list)
    for idx, values in enumerate(products, start=1):
        grouped[values[2]].append({"scenario_id": f"S3T-{idx:05d}", **dict(zip(keys, values))})
    return grouped


def stage4_size_scenarios(stage3_rows):
    d50_values = (0.10, 0.25, 0.50, 1.0, 2.0, 4.0, 8.0)
    gsd_values = (1.4, 1.8, 2.2, 2.8)
    cuts = (0.25, 0.50, 1.0, 2.0)
    rec = 0
    for base in stage3_rows:
        feed = base["stage3_laminate_mass_kg"]
        for d50, gsd, cut in itertools.product(d50_values, gsd_values, cuts):
            rec += 1
            z = math.log(cut / d50) / math.log(gsd)
            fines_frac = 0.5 * (1 + math.erf(z / math.sqrt(2)))
            fine_kg = feed * fines_frac
            coarse_kg = feed - fine_kg
            yield {
                "scenario_id": f"S4S-{base['scenario_id']}-{int(d50*100):03d}-{int(gsd*10):02d}-{int(cut*100):03d}",
                "panel_mass_kg": base["panel_mass_kg"],
                "stage2_frame_share_pct": base["stage2_frame_share_pct"],
                "stage2_jbox_cable_share_pct": base["stage2_jbox_cable_share_pct"],
                "stage3_glass_share_of_original_pct": base["stage3_glass_share_of_original_pct"],
                "stage3_laminate_mass_kg": feed,
                "stage4_feed_mass_kg": feed,
                "stage4_particle_mass_D50_mm": d50,
                "stage4_particle_geometric_SD": gsd,
                "stage4_screen_cut_mm": cut,
                "stage4_fines_mass_fraction_model": fines_frac,
                "stage4_fines_mass_kg": fine_kg,
                "stage4_coarse_mass_kg": coarse_kg,
                "stage4_mass_closure_pct": 100 * (fine_kg + coarse_kg) / feed,
                "source_basis": (
                    "Scenario only. Assumed mass-weighted lognormal particle-size distribution; D50, "
                    "geometric SD and screen cut are varied as analyst inputs. No Stage 4 comminution or "
                    "Agastya feed PSD has been measured. This predicts size mass split only; no composition, "
                    "Ag grade or Ag recovery is inferred."
                ),
            }


LITERATURE_PARTITIONS = [
    (0.70, "Sim2023_EVAc_category", "Reported Ag distribution to finest cut for EVAc-category study feed"),
    (0.80, "Sim2023_MP_category", "Reported Ag distribution to finest cut for MP-category study feed"),
    (0.9412, "JuyoSalazar2024_lt0.25mm", "Reported Ag distribution in <0.25 mm fraction for study feed"),
]


def stage4_ag_scenarios(stage3_rows):
    rec = 0
    for base in stage3_rows:
        feed = base["stage3_laminate_mass_kg"]
        for ag_g_per_panel, (partition, method, description) in itertools.product(
            (10, 20, 30), LITERATURE_PARTITIONS
        ):
            rec += 1
            ag_to_fines = ag_g_per_panel * partition
            ag_grade = 100 * (ag_g_per_panel / (feed * 1000))
            yield {
                "scenario_id": f"S4Ag-{base['scenario_id']}-Ag{ag_g_per_panel}-{method}",
                "panel_mass_kg": base["panel_mass_kg"],
                "stage2_frame_share_pct": base["stage2_frame_share_pct"],
                "stage2_jbox_cable_share_pct": base["stage2_jbox_cable_share_pct"],
                "stage3_glass_share_of_original_pct": base["stage3_glass_share_of_original_pct"],
                "stage3_laminate_mass_kg": feed,
                "stage4_feed_mass_kg": feed,
                "stage4_Ag_per_panel_assumed_g": ag_g_per_panel,
                "stage4_Ag_reported_to_fines_fraction": partition,
                "stage4_Ag_in_fines_scenario_g": ag_to_fines,
                "stage4_Ag_feed_grade_scenario_wt_pct": ag_grade,
                "stage4_fines_yield_assumed_fraction": "",
                "stage4_fines_Ag_grade_scenario_wt_pct": "",
                "stage4_literature_method": f"{method}: {description}",
                "source_basis": (
                    "Literature-normalized scenario, not Agastya prediction. Ag per panel is assumed at "
                    "10/20/30 g (20 g is the thesis central assumption; outer cases are analyst sensitivities). "
                    "This scenario allocates all assumed panel Ag to the modeled Stage 4 laminate; Stage 3 Ag "
                    "partition is unknown and not simulated. Reported source distributions are applied "
                    "arithmetically; different studies/feed types are kept separate. Product mass yield is not "
                    "reported here, so fines grade is blank."
                ),
            }


def run_trace(case, sample_dt=0.1, cool_s=2.0):
    _, _, _, _, _, _, T0 = thermal_matrix(case)
    state = (*thermal_matrix(case)[:6], T0, 0.0, 0.0)
    # State is advanced at the same small timestep as the parameter sweep.
    total_s = case["duration"] + cool_s
    snapshot_every = int(round(sample_dt / DT_S))
    out = []
    step_count = int(round(total_s / DT_S))
    for step in range(step_count + 1):
        t = step * DT_S
        blade_on = t < case["duration"]
        state, Tif, _ = thermal_step(case, state, DT_S, blade_on=blade_on) if step > 0 else (state, case["ambient"], 0.0)
        if step % snapshot_every == 0:
            T = state[6]
            out.append({
                "time_s": t,
                "Tif": Tif,
                "T": T.copy(),
                "Ein": state[7],
            })
    return out


def run():
    counts = defaultdict(int)
    summary = {}
    max_abs_energy_error = 0.0
    min_peak_eva = float("inf")
    max_peak_eva = float("-inf")
    min_energy = float("inf")
    max_energy = float("-inf")
    max_stage4_fines = float("-inf")
    min_stage4_fines = float("inf")
    max_trace_error = 0.0
    record_counter = 0
    with CSV_PATH.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()

        def emit(**values):
            nonlocal record_counter
            record_counter += 1
            stage = values.pop("stage")
            identifiers = {
                "manual_mass_balance": ("EXP-S2-01", "PROC-S2-01"),
                "material_mass_balance": ("EXP-S3-01", "PROC-S3-01"),
                "thermal_case_summary": ("EXP-S3-02", "PROC-S3-02"),
                "thermal_time_trace": ("EXP-S3-03", "PROC-S3-03"),
                "lognormal_sieve_sensitivity": ("EXP-S4-01", "PROC-S4-01"),
                "literature_Ag_partition_scenario": ("EXP-S4-02", "PROC-S4-02"),
            }
            experiment_id, procedure_id = identifiers[values["record_type"]]
            write_row(writer, f"R{record_counter:07d}", experiment_id=experiment_id,
                      procedure_id=procedure_id, stage=stage, **values)

        s2_rows = list(stage2_scenarios())
        for row in s2_rows:
            emit(stage="2", record_type="manual_mass_balance", evidence_status="SCENARIO_ONLY", **row)
        counts["stage2_manual_mass_balance"] = len(s2_rows)

        s3_rows = list(stage3_material_scenarios(s2_rows))
        for row in s3_rows:
            emit(stage="3", record_type="material_mass_balance", evidence_status="SCENARIO_ONLY", **row)
            counts["stage3_material_mass_balance"] += 1

        grouped = thermal_cases()
        thermal_case_count = 0
        for duration, cases in grouped.items():
            result = simulate_thermal_batch(cases, DT_S)
            for i, case in enumerate(cases):
                pset = PROPERTY_SETS[case["property_set"]]
                peak_eva = max(result["peak"][i, 1], result["peak"][i, 3])
                peak_cell = result["peak"][i, 2]
                min_peak_eva = min(min_peak_eva, peak_eva)
                max_peak_eva = max(max_peak_eva, peak_eva)
                min_energy = min(min_energy, result["Ein"][i])
                max_energy = max(max_energy, result["Ein"][i])
                max_abs_energy_error = max(max_abs_energy_error, abs(result["energy_error_pct"][i]))
                emit(
                    stage="3", record_type="thermal_case_summary",
                    evidence_status="NUMERICAL_MODEL_ASSUMPTIONS",
                    scenario_id=case["scenario_id"], source_basis=(
                        f"Reduced 1-D five-node thermal RC model. Material properties: {case['property_set']} "
                        "literature table; contact conductance, interfacial resistance and contact dwell are "
                        "analyst sensitivities. Blade held at setpoint; no tool mass, heater power, moving-front "
                        "geometry, latent heat, adhesion fracture or EVA degradation chemistry. Energies are per "
                        "m² of assumed blade-contact area, not per panel/electrical kWh."
                    ), ambient_C=case["ambient"], stage3_material_property_set=case["property_set"],
                    stage3_blade_setpoint_C=case["tool"], stage3_contact_conductance_W_m2K=case["hc"],
                    stage3_contact_duration_s=case["duration"], stage3_EVA_total_thickness_mm=case["eva_mm"],
                    stage3_backsheet_thickness_mm=pset["bs_mm"], stage3_interface_resistance_m2K_W=case["rint"],
                    stage3_time_s=case["duration"], stage3_T_interface_C=result["Tif"][i],
                    stage3_T_glass_node_C=result["T"][i, 0], stage3_T_EVA_front_node_C=result["T"][i, 1],
                    stage3_T_cell_node_C=result["T"][i, 2], stage3_T_EVA_rear_node_C=result["T"][i, 3],
                    stage3_T_backsheet_node_C=result["T"][i, 4], stage3_peak_EVA_node_C=peak_eva,
                    stage3_peak_cell_node_C=peak_cell, stage3_net_contact_energy_J_m2=result["Ein"][i],
                    stage3_time_above_100C_s=result["above"][100][i],
                    stage3_time_above_140C_s=result["above"][140][i],
                    stage3_time_above_180C_s=result["above"][180][i],
                    stage3_time_above_220C_s=result["above"][220][i],
                    stage3_time_above_280C_s=result["above"][280][i],
                    stage3_energy_balance_error_pct=result["energy_error_pct"][i],
                )
                thermal_case_count += 1
        counts["stage3_thermal_case_summary"] = thermal_case_count

        trace_count = 0
        for tool, hc, duration in itertools.product((180, 200, 220, 300), (100, 1000, 3000), (2, 10)):
            case = {
                "scenario_id": f"S3TRACE-T{tool}-H{hc}-D{duration}",
                "tool": tool, "hc": hc, "duration": duration, "ambient": 25,
                "eva_mm": 0.90, "property_set": "Lizcano2024_A1", "rint": 1e-4,
            }
            for sample in run_trace(case):
                emit(
                    stage="3", record_type="thermal_time_trace",
                    evidence_status="NUMERICAL_MODEL_ASSUMPTIONS",
                    scenario_id=case["scenario_id"], source_basis=(
                        "Illustrative 1-D five-node thermal RC transient. Heater contact switches off at the "
                        "listed dwell and the model then cools for 2 s. Not a measured panel or validated process."
                    ), ambient_C=case["ambient"], stage3_material_property_set=case["property_set"],
                    stage3_blade_setpoint_C=tool, stage3_contact_conductance_W_m2K=hc,
                    stage3_contact_duration_s=duration, stage3_EVA_total_thickness_mm=case["eva_mm"],
                    stage3_backsheet_thickness_mm=PROPERTY_SETS[case["property_set"]]["bs_mm"],
                    stage3_interface_resistance_m2K_W=case["rint"], stage3_time_s=sample["time_s"],
                    stage3_T_interface_C=sample["Tif"], stage3_T_glass_node_C=sample["T"][0],
                    stage3_T_EVA_front_node_C=sample["T"][1], stage3_T_cell_node_C=sample["T"][2],
                    stage3_T_EVA_rear_node_C=sample["T"][3], stage3_T_backsheet_node_C=sample["T"][4],
                    stage3_peak_EVA_node_C=max(sample["T"][1], sample["T"][3]),
                    stage3_peak_cell_node_C=sample["T"][2], stage3_net_contact_energy_J_m2=sample["Ein"],
                )
                trace_count += 1
        counts["stage3_thermal_time_trace"] = trace_count

        size_count = 0
        for row in stage4_size_scenarios(s3_rows):
            emit(stage="4", record_type="lognormal_sieve_sensitivity",
                 evidence_status="SCENARIO_ONLY", **row)
            counts["stage4_size_sensitivity"] += 1
            max_stage4_fines = max(max_stage4_fines, row["stage4_fines_mass_fraction_model"])
            min_stage4_fines = min(min_stage4_fines, row["stage4_fines_mass_fraction_model"])
            size_count += 1

        ag_count = 0
        for row in stage4_ag_scenarios(s3_rows):
            emit(stage="4", record_type="literature_Ag_partition_scenario",
                 evidence_status="LITERATURE_NORMALIZED_SCENARIO", **row)
            counts["stage4_literature_Ag_scenarios"] += 1
            ag_count += 1

    # Numerical consistency check: halve dt on three representative operating points.
    refinement_cases = [
        {"tool": 180, "hc": 100, "duration": 0.5, "ambient": 25, "eva_mm": 0.90,
         "property_set": "Lizcano2024_A1", "rint": 1e-4},
        {"tool": 220, "hc": 1000, "duration": 5, "ambient": 25, "eva_mm": 0.90,
         "property_set": "Lizcano2024_A1", "rint": 1e-4},
        {"tool": 300, "hc": 3000, "duration": 10, "ambient": 35, "eva_mm": 1.16,
         "property_set": "Tomsic2025_Table1", "rint": 5e-4},
    ]
    differences = []
    for case in refinement_cases:
        coarse = simulate_thermal_batch([case], 0.005)
        fine = simulate_thermal_batch([case], 0.0025)
        coarse_peak = max(coarse["peak"][0, 1], coarse["peak"][0, 3])
        fine_peak = max(fine["peak"][0, 1], fine["peak"][0, 3])
        differences.append(abs(coarse_peak - fine_peak))
    max_dt_refinement_delta = max(differences)

    summary = {
        "generated_on": DATE_TAG,
        "dataset_path": CSV_PATH.name,
        "dataset_schema_version": "2.0",
        "computation_software": {
            "python": f"CPython {platform.python_version()}",
            "numpy": np.__version__,
            "python_standard_library": ["csv", "json", "itertools", "math", "collections", "pathlib"],
            "solver": "Custom five-node 1-D thermal resistance/capacitance model, integrated with explicit forward Euler; scenario/mass-balance and lognormal calculations run in Python.",
        },
        "experiment_register_path": "experiment_register.csv",
        "data_dictionary_path": "data_dictionary.csv",
        "all_rows_reference_documented_experiment_and_procedure": True,
        "total_records": int(sum(counts.values())),
        "record_counts": dict(counts),
        "stage2_stage3_input_mass_range_kg": [
            min(r["stage2_output_to_stage3_kg"] for r in s2_rows),
            max(r["stage2_output_to_stage3_kg"] for r in s2_rows),
        ],
        "stage3_thermal_cases": thermal_case_count,
        "stage3_peak_EVA_node_temperature_range_C": [min_peak_eva, max_peak_eva],
        "stage3_contact_energy_range_J_per_m2_assumed_contact_area": [min_energy, max_energy],
        "stage3_max_abs_energy_balance_error_pct": max_abs_energy_error,
        "stage3_time_step_refinement_max_peak_EVA_difference_C": max_dt_refinement_delta,
        "stage4_log_normal_fines_mass_fraction_range": [min_stage4_fines, max_stage4_fines],
        "stage4_literature_Ag_scenario_count": ag_count,
        "all_values_are_simulated_or_scenario_calculations": True,
        "physical_sample_count": 0,
        "scenario_rows_are_physical_samples": False,
        "measured_Agastya_trial_rows": 0,
    }
    META_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_report(summary)
    print(json.dumps(summary, indent=2))


def write_report(summary):
    counts = summary["record_counts"]
    report = f"""# Agastya physics simulation and sensitivity sweep

**Generated:** 10 October 2026  
**Data file:** `{CSV_PATH.name}`  
**Reproducible model:** `{Path(__file__).name}`

## What was run

This is a first-principles and sensitivity simulation created because the existing Agastya browser walkthrough and Wokwi monitor are conceptual/UI demonstrations, not physics solvers. The run produced **{summary['total_records']:,} rows**. It contains no physical trial observations; measured Agastya trial rows: **0**. The rows are deterministic parameter combinations and time-history outputs, not physical specimens or a Monte Carlo sample size. Every record carries an experiment ID and a procedure ID. See `experiment_register.csv` and `data_dictionary.csv` for the procedure index and column meanings. Follow-up virtual experiments are stored separately in `followup_virtual_experiments.csv` and described in `PROCEDURES_AND_RESULTS.md`.

## Programs and numerical method

The run uses **{summary['computation_software']['python']}** and **NumPy {summary['computation_software']['numpy']}**. Python's built-in `csv` and `json` modules write the datasets and metadata; the standard library also supplies scenario enumeration and mathematical functions. Stage 3 uses a custom one-dimensional, five-node thermal resistance/capacitance model integrated with explicit forward Euler. Python/NumPy vectorize the batch calculation. No commercial finite-element, CFD, or process-simulation package was used. PowerShell was only the launch shell in this run; it did not calculate the physics.

| Block | Rows | What the rows contain |
|---|---:|---|
| Stage 2 manual mass balance | {counts['stage2_manual_mass_balance']:,} | Frame/junction-box hand-off scenarios, Stage 3 feed mass, and idealized one-operator shift ceiling. |
| Stage 3 material balance | {counts['stage3_material_mass_balance']:,} | Glass and laminate output masses from a composition-based scenario sweep. |
| Stage 3 thermal transient summaries | {counts['stage3_thermal_case_summary']:,} | Layer temperatures, heat input per assumed contact area, and time above comparison thresholds. |
| Stage 3 thermal time traces | {counts['stage3_thermal_time_trace']:,} | 0.1 s snapshots for representative heating/cooling cases. |
| Stage 4 size-classification sensitivity | {counts['stage4_size_sensitivity']:,} | Fine/coarse mass split for a mass-weighted lognormal particle-size distribution across D50, spread and cut sizes. |
| Stage 4 literature Ag partition scenarios | {counts['stage4_literature_Ag_scenarios']:,} | Arithmetic scaling of published Ag-to-fines distributions, kept separate by source feed and method. |

## Main model boundaries

### Stage 2

Stage 2 follows the current project plan: a **supervised manual hand-off** after isolation, frame removal and junction-box/external-cable removal. Panel mass (10–30 kg), removable frame share (7–13 wt%), cable/J-box share (0.1–1 wt%) and elapsed manual time (2–15 minutes) are sensitivity inputs, not measured values. The 10 wt% central frame share comes from the thesis's composition graphic; the graphic's 1 wt% copper includes all panel wiring and cannot be treated as a measured junction-box share. The 8-hour capacity is an ideal arithmetic ceiling and excludes breaks, movement, inspection, jams, training and multiple operators.

The mass-balance rows conserve input mass by construction. They do not simulate electrical isolation, tool forces, manual labor variability, or the risks of handling damaged modules.

### Stage 3

The thermal run is a **one-dimensional, five-node transient thermal-resistance/capacitance model**: glass, front EVA, silicon cell, rear EVA and backsheet. It applies a fixed-temperature hot-knife contact at the glass/EVA interface, then calculates conduction through the layers plus natural convection and radiation at the two outer surfaces. It sweeps knife temperatures 180/200/220/250/300 °C; contact conductance 100/300/1,000/3,000 W m⁻² K⁻¹; assumed local dwell 0.1–10 s; ambient 15/25/35 °C; two total EVA thicknesses (0.90/1.16 mm); two literature property sets; and assumed interface thermal resistances 0/1×10⁻⁴/5×10⁻⁴ m² K W⁻¹. The 0.90 mm total uses the thesis's 2×0.45 mm; 1.16 mm interprets the literature table's 580 μm EVA (×2) as 0.58 mm per layer. Outer convection is fixed at an assumed 8 W m⁻² K⁻¹; emissivities are 0.85 (glass) and 0.93 (backsheet).

The materials-property sets follow tables from [Lizcano et al. (2024)](https://doi.org/10.1002/pip.3813) and [Tomšič et al. (2025)](https://doi.org/10.1002/adts.202401026). Project references for the hot-knife process and its limits are in [Stage 3 thermal development](../Build%20Files%20and%20Steps/Stage%203/STAGE3_THERMAL_DEVELOPMENT.md). Time above 100/140 °C is a comparison statistic, not a modeled peel result; EVA adhesion, viscoelastic fracture, and actual material-specific delamination strength are not modeled. The 280 °C time flag is only a comparison with reported TGA behavior for tested EVA ([Saitta et al. (2026)](https://doi.org/10.3390/green1010002)), not an operating limit or safety approval.

Thermal model outputs are **per square metre of assumed blade-contact area**. They are not electrical heater kWh per panel. The model excludes the heater/blade mass and control cycle, moving contact geometry, blade feed speed, full-panel heat distribution, latent heat, cross-linked EVA chemistry, damage, fumes, and quality scoring. Whole-panel hot-knife literature cycle times (about 50–60 s/module) do not define local contact dwell; the two quantities are kept separate.

### Stage 4

The Stage 4 mainline follows the latest project research decision: **contained comminution and dry size classification**, with ECS conditional on a characterized eligible feed. The size model assumes an overall *mass-weighted lognormal* particle-size distribution and computes the mass below each screen cut from its CDF. It sweeps assumed D50 values of 0.10–8 mm, geometric standard deviations of 1.4–2.8, and screen cuts of 0.25–2 mm. No Agastya crusher, feed particle-size distribution, component-specific liberation or sieve efficiency has been measured. Those rows predict only size mass partition, not Ag grade or recovery.

The separate Ag rows scale 70%, 80% and 94.12% source-reported Ag distributions to 10/20/30 g/panel scenario inputs. The reported distribution values come from different study feeds ([Sim et al. (2022)](https://doi.org/10.1016/j.wasman.2022.11.023); [Juyo Salazar et al. (2024)](https://doi.org/10.1016/j.susmat.2024.e01047)) and are **not a prediction of Agastya performance**. The 20 g/panel central input is from the thesis; 10 and 30 g are analyst sensitivity bounds. This arithmetic scenario allocates all assumed panel Ag to the modeled Stage 4 laminate; Stage 3 Ag partition is unknown and not simulated. Since product mass yield is unavailable, fine-fraction Ag grade is deliberately left blank. The conventional eddy-current mechanism is not numerically predicted: current feed is not demonstrated to be liberated conductive particles, and the project record does not provide the particle geometry, conductivity, magnetic-field map, rotor speed or splitter dimensions needed for a defensible trajectory model.

## Results range

- Stage 2 scenario Stage 3 feed mass: **{summary['stage2_stage3_input_mass_range_kg'][0]:.3f}–{summary['stage2_stage3_input_mass_range_kg'][1]:.3f} kg/module**.
- Stage 3 peak modeled EVA-node temperature: **{summary['stage3_peak_EVA_node_temperature_range_C'][0]:.2f}–{summary['stage3_peak_EVA_node_temperature_range_C'][1]:.2f} °C** across the swept interface conditions.
- Stage 3 net interface heat: **{summary['stage3_contact_energy_range_J_per_m2_assumed_contact_area'][0]:.1f}–{summary['stage3_contact_energy_range_J_per_m2_assumed_contact_area'][1]:.1f} J/m²** of assumed contact area.
- Stage 3 maximum absolute integrated energy-balance residual: **{summary['stage3_max_abs_energy_balance_error_pct']:.4g}%**. Halving the 5 ms integration step changed peak EVA temperature by at most **{summary['stage3_time_step_refinement_max_peak_EVA_difference_C']:.4g} °C** on three representative checks.
- Stage 4 modeled fines mass fraction: **{summary['stage4_log_normal_fines_mass_fraction_range'][0]:.4f}–{summary['stage4_log_normal_fines_mass_fraction_range'][1]:.4f}** across assumed PSD/cut combinations. This large spread mainly shows the sensitivity to unknown post-comminution PSD; it is not an equipment performance interval.

The ranges describe parameter sweeps, not confidence intervals, likely operating windows, safe settings, or expected results. Do not use them as design approvals, safety limits, energy claims, or recovery forecasts. A parameter-combination count is not a physical sample size.

## Provisional conclusions about the process approaches

- **Stage 2:** retain supervised manual hand-off as the current baseline until panel/output weights and task time are measured. The 32–576 panels/shift range is an ideal arithmetic capacity ceiling, not a throughput estimate or automation case.
- **Stage 3:** use hot-knife front-glass separation as the instrumented coupon reference because it matches the current glass-plus-laminate process objective. The reduced model only maps assumed heat transfer; it cannot establish peel quality, select a setpoint, or verify EVA-free cells. The heated roller and heat reuse remain unverified.
- **Stage 4:** continue with contained comminution and dry classification as the measured-feed research path. The 0–1 fines range reflects the unknown PSD. Keep ECS conditional until the feed is characterized; no ECS performance was simulated.
- **Silver:** neither literature-normalized partition rows nor conditional grade arithmetic establishes Agastya grade or recovery. Measure Stage 3 silver partition, feed assay, fraction masses and product assays before making a recovery claim.

These are provisional development directions, not a validated process ranking or safety/design decision. See `PROCEDURES_AND_RESULTS.md` for the full scenario counts, physical sample-size statement and procedure-by-procedure conclusions.

## Reproduce

Run from the main Agastya folder with Python 3 and NumPy:

```powershell
python ".\\Agastya Physics Simulation\\{Path(__file__).name}"
```

The script regenerates the consolidated CSV and this report. A machine-readable run summary is in `{META_PATH.name}`.

## Most useful real measurements to collect next

1. Stage 2: weigh one identified panel, removed frame, junction box/cables and Stage 3 hand-off; record actual supervised task time.
2. Stage 3: on supervisor-approved coupons, log blade temperature, interface temperature, contact geometry/feed speed, energy meter trace, force and output-quality scores. These measurements are needed to replace contact and loss assumptions.
3. Stage 4: obtain supervised/contained access, characterize the actual laminate feed PSD and dryness, retain and weigh every fraction, and assay representative feed/products. Do not add ECS unless the measured feed meets an accepted device envelope.

## Source notes

- Agastya Stage 2 manual and Stage 3 process boundaries: `../Build Files and Steps/Stage 3/STAGE3_BUILD_PLAN.md`, `../Build Files and Steps/Stage 3/STAGE3_THERMAL_DEVELOPMENT.md`, and `../04_Logbook/PROJECT_LOGBOOK_DAY_3_4.md`.
- Stage 3 material properties: [Lizcano et al., 2024](https://doi.org/10.1002/pip.3813), Table A1; [Tomšič et al., 2025](https://doi.org/10.1002/adts.202401026), Table 1.
- Stage 4 literature distribution values and interpretation: `../Build Files and Steps/Stage 4/STAGE4_METHOD_COMPARISON_AND_CALCULATIONS.md` and `../Build Files and Steps/Stage 4/STAGE4_RESEARCH_COMPLETION_BRIEF_2026-10-08.md`.
- The published 70/80 and 94.12% values are normalized distributions into the finest fraction, not product grade or purity. All Agastya-specific feed masses and material shares in this file remain unverified scenarios.
"""
    REPORT_PATH.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    run()

