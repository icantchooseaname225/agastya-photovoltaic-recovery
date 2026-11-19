"""Reproducible Phase E analyses for the AGASTYA project.

Runs (1) a main-effect variance decomposition on the archived 5,040-case
five-node thermal sweep, and (2) a spatial refinement study against the
same historical one-dimensional layered thermal model. Both are numerical
studies of the historical thermal model now mapped to current Stage 3. It does
not predict delamination quality or current Stage 4 silver removal.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import math
import platform
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / "Research Phase E"
CAMPAIGN = PHASE / "Simulation_Campaign"
RAW = CAMPAIGN / "raw"
PROCESSED = CAMPAIGN / "processed"
FIGURES = CAMPAIGN / "figures"
MODEL_PATH = ROOT / "Agastya_Physics_Simulation_2026-10-10.py"
INPUT_CSV = ROOT / "Agastya_Physics_Simulation_2026-10-10.csv"
SIGMA = 5.670374419e-8
DT = 0.0005

for folder in (RAW, PROCESSED, FIGURES):
    folder.mkdir(parents=True, exist_ok=True)

spec = importlib.util.spec_from_file_location("agastya_legacy_model", MODEL_PATH)
legacy = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(legacy)


def load_thermal_sweep() -> pd.DataFrame:
    cols = [
        "record_type", "experiment_id", "stage3_material_property_set",
        "stage3_blade_setpoint_C", "stage3_contact_conductance_W_m2K",
        "stage3_contact_duration_s", "ambient_C", "stage3_EVA_total_thickness_mm",
        "stage3_interface_resistance_m2K_W", "stage3_peak_EVA_node_C",
        "stage3_peak_cell_node_C", "stage3_net_contact_energy_J_m2",
        "stage3_energy_balance_error_pct",
    ]
    # The historical file is a wide, mixed-type master CSV. DictReader is a
    # little slower than pandas' C parser, but avoids a parser warning-path
    # failure on this file while preserving every row and column alignment.
    rows = []
    with INPUT_CSV.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for record in reader:
            if record["record_type"] == "thermal_case_summary" and record["experiment_id"] == "EXP-S3-02":
                rows.append({key: record[key] for key in cols})
    df = pd.DataFrame(rows)
    for col in cols:
        if col not in ("record_type", "experiment_id", "stage3_material_property_set"):
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def variance_decomposition(df: pd.DataFrame) -> dict:
    factors = {
        "Blade setpoint (°C)": "stage3_blade_setpoint_C",
        "Contact conductance (W m⁻² K⁻¹)": "stage3_contact_conductance_W_m2K",
        "Dwell (s)": "stage3_contact_duration_s",
        "Ambient (°C)": "ambient_C",
        "Total EVA thickness (mm)": "stage3_EVA_total_thickness_mm",
        "Property set": "stage3_material_property_set",
        "Interface resistance (m² K W⁻¹)": "stage3_interface_resistance_m2K_W",
    }
    outputs = {
        "Peak EVA temperature (°C)": "stage3_peak_EVA_node_C",
        "Peak cell temperature (°C)": "stage3_peak_cell_node_C",
        "Net contact energy (J m⁻²)": "stage3_net_contact_energy_J_m2",
    }
    result = {"experiment_id": "PE-SIM-001", "records": int(len(df)), "factor_level_counts": {}, "metrics": {}}
    for label, col in factors.items():
        result["factor_level_counts"][label] = sorted(df[col].dropna().astype(str).unique().tolist())
    for out_label, out_col in outputs.items():
        y = df[out_col].astype(float)
        mean = float(y.mean())
        total_ss = float(((y - mean) ** 2).sum())
        components = []
        explained_ss = 0.0
        for factor_label, factor_col in factors.items():
            grouped = df.groupby(factor_col, dropna=False)[out_col].agg(["mean", "count"])
            ss = float((grouped["count"] * (grouped["mean"] - mean) ** 2).sum())
            explained_ss += ss
            components.append({
                "factor": factor_label,
                "sum_squares": ss,
                "share_of_total_variance_pct": 100 * ss / total_ss if total_ss else 0,
                "levels": int(len(grouped)),
                "level_means": {str(index): float(value) for index, value in grouped["mean"].items()},
            })
        components.sort(key=lambda item: item["share_of_total_variance_pct"], reverse=True)
        result["metrics"][out_label] = {
            "mean": mean,
            "minimum": float(y.min()),
            "maximum": float(y.max()),
            "total_sum_squares": total_ss,
            "main_effects": components,
            "unallocated_interaction_and_residual_share_pct": max(0.0, 100 * (total_ss - explained_ss) / total_ss) if total_ss else 0,
        }
    return result


def thermal_case(tool: float, hc: float, dwell: float, ambient: float, eva_mm: float, property_set: str, rint: float) -> dict:
    return {"tool": tool, "hc": hc, "duration": dwell, "ambient": ambient,
            "eva_mm": eva_mm, "property_set": property_set, "rint": rint}


CASES = [
    ("low_short", thermal_case(180, 100, 0.5, 15, 0.90, "Lizcano2024_A1", 0.0)),
    ("nominal", thermal_case(220, 1000, 2.0, 25, 0.90, "Lizcano2024_A1", 1e-4)),
    ("long_moderate", thermal_case(250, 300, 5.0, 25, 1.16, "Tomsic2025_Table1", 1e-4)),
    ("high_bound", thermal_case(300, 3000, 10.0, 35, 1.16, "Tomsic2025_Table1", 5e-4)),
]


def expanded_nodes(case: dict, cells_per_layer: int):
    p = legacy.PROPERTY_SETS[case["property_set"]]
    layer_thickness = [0.0032, case["eva_mm"] / 2000, 0.00021,
                       case["eva_mm"] / 2000, p["bs_mm"] / 1000]
    layer_k = [p["glass_k"], p["eva_k"], p["si_k"], p["eva_k"], p["bs_k"]]
    layer_rho_cp = [p["glass_rho"] * p["glass_cp"], p["eva_rho"] * p["eva_cp"],
                    p["si_rho"] * p["si_cp"], p["eva_rho"] * p["eva_cp"],
                    p["bs_rho"] * p["bs_cp"]]
    dx = np.repeat(np.asarray(layer_thickness) / cells_per_layer, cells_per_layer)
    k = np.repeat(np.asarray(layer_k), cells_per_layer)
    capacity = dx * np.repeat(np.asarray(layer_rho_cp), cells_per_layer)
    layer_index = np.repeat(np.arange(5), cells_per_layer)
    conductance = np.empty(len(dx) - 1)
    for j in range(len(conductance)):
        interface_r = case["rint"] if layer_index[j] != layer_index[j + 1] else 0.0
        conductance[j] = 1 / (dx[j] / (2 * k[j]) + dx[j + 1] / (2 * k[j + 1]) + interface_r)
    # The same algebraic blade/interface node used by the original model.
    glass_idx = cells_per_layer - 1
    eva_idx = cells_per_layer
    rg = dx[glass_idx] / (2 * k[glass_idx])
    re = dx[eva_idx] / (2 * k[eva_idx])
    return dx, k, capacity, layer_index, conductance, glass_idx, eva_idx, 1 / rg, 1 / re


def estimate_explicit_row_ratio(case: dict, cells_per_layer: int, dt: float) -> float:
    dx, k, cap, layer_index, edge_g, glass_idx, eva_idx, gg, ge = expanded_nodes(case, cells_per_layer)
    row_sum = np.zeros(len(cap))
    for j, value in enumerate(edge_g):
        row_sum[j] += value
        row_sum[j + 1] += value
    # Eliminate the zero-capacity interface node. Its equivalent network adds
    # conductance among the blade, adjacent glass and EVA control volumes.
    h = case["hc"]
    denom = h + gg + ge
    g_gb, g_eb, g_ge = h * gg / denom, h * ge / denom, gg * ge / denom
    row_sum[glass_idx] += g_gb + g_ge
    row_sum[eva_idx] += g_eb + g_ge
    # Bound radiation linearization conservatively at 300 C, plus h=8 W/m2/K.
    hrad = 4 * 0.93 * SIGMA * (300 + 273.15) ** 3
    row_sum[0] += 8 + hrad
    row_sum[-1] += 8 + hrad
    return float(np.max(dt * row_sum / cap))


def simulate_fv(case: dict, cells_per_layer: int, dt: float = DT) -> dict:
    dx, k, cap, layer_index, edge_g, glass_idx, eva_idx, gg, ge = expanded_nodes(case, cells_per_layer)
    nsteps = int(round(case["duration"] / dt))
    if not math.isclose(nsteps * dt, case["duration"], abs_tol=1e-12):
        raise ValueError("Selected timestep must divide contact duration exactly")
    T = np.full(len(dx), case["ambient"], dtype=float)
    eva_nodes = np.flatnonzero(np.isin(layer_index, [1, 3]))
    cell_nodes = np.flatnonzero(layer_index == 2)
    peak_eva = float(case["ambient"])
    peak_cell = float(case["ambient"])
    ein = qloss = 0.0
    h = case["hc"]
    # Build the fixed conduction operator. Backward Euler is used because the
    # silicon layer's small control volumes make an explicit timestep that is
    # practical for the 10 s cases unstable at finer meshes.
    diag_fixed = np.zeros(len(dx))
    for j, g in enumerate(edge_g):
        diag_fixed[j] += g
        diag_fixed[j + 1] += g
    denom = h + gg + ge
    g_gb, g_eb, g_ge = h * gg / denom, h * ge / denom, gg * ge / denom
    diag_fixed[glass_idx] += g_gb + g_ge
    diag_fixed[eva_idx] += g_eb + g_ge
    edge_g_with_blade = edge_g.copy()
    edge_g_with_blade[glass_idx] += g_ge
    lower = -edge_g_with_blade.copy()
    upper = -edge_g_with_blade.copy()

    def solve_tridiagonal(a, b, c, rhs):
        n = len(b)
        cp = np.empty(n - 1)
        dp = np.empty(n)
        denom0 = b[0]
        cp[0] = c[0] / denom0 if n > 1 else 0.0
        dp[0] = rhs[0] / denom0
        for idx in range(1, n):
            den = b[idx] - a[idx - 1] * cp[idx - 1]
            if idx < n - 1:
                cp[idx] = c[idx] / den
            dp[idx] = (rhs[idx] - a[idx - 1] * dp[idx - 1]) / den
        x = np.empty(n)
        x[-1] = dp[-1]
        for idx in range(n - 2, -1, -1):
            x[idx] = dp[idx] - cp[idx] * x[idx + 1]
        return x

    for _ in range(nsteps):
        tamb = case["ambient"]
        old = T.copy()
        guess = old.copy()
        # Picard iteration for nonlinear radiative surface losses. Three
        # iterations suffice at the selected step; the fixed point is checked.
        for _iteration in range(8):
            af = 8 + 4 * 0.85 * SIGMA * (guess[0] + 273.15) ** 3
            ab = 8 + 4 * 0.93 * SIGMA * (guess[-1] + 273.15) ** 3
            qf_guess = 8 * (guess[0] - tamb) + 0.85 * SIGMA * ((guess[0] + 273.15) ** 4 - (tamb + 273.15) ** 4)
            qb_guess = 8 * (guess[-1] - tamb) + 0.93 * SIGMA * ((guess[-1] + 273.15) ** 4 - (tamb + 273.15) ** 4)
            bf = qf_guess - af * guess[0]
            bb = qb_guess - ab * guess[-1]
            diagonal = cap / dt + diag_fixed
            diagonal[0] += af
            diagonal[-1] += ab
            rhs = cap / dt * old
            rhs[glass_idx] += g_gb * case["tool"]
            rhs[eva_idx] += g_eb * case["tool"]
            rhs[0] += -bf
            rhs[-1] += -bb
            candidate = solve_tridiagonal(lower, diagonal, upper, rhs)
            delta = float(np.max(np.abs(candidate - guess)))
            guess = candidate
            if delta < 1e-10:
                break
        T = guess
        tif = (h * case["tool"] + gg * T[glass_idx] + ge * T[eva_idx]) / (h + gg + ge)
        q_blade = h * (case["tool"] - tif)
        qfront = 8 * (T[0] - tamb) + 0.85 * SIGMA * ((T[0] + 273.15) ** 4 - (tamb + 273.15) ** 4)
        qback = 8 * (T[-1] - tamb) + 0.93 * SIGMA * ((T[-1] + 273.15) ** 4 - (tamb + 273.15) ** 4)
        ein += q_blade * dt
        qloss += (qfront + qback) * dt
        peak_eva = max(peak_eva, float(T[eva_nodes].max()))
        peak_cell = max(peak_cell, float(T[cell_nodes].max()))
    stored = float(np.sum(cap * (T - case["ambient"])))
    err = ein - qloss - stored
    return {
        "peak_eva_C": peak_eva,
        "peak_cell_C": peak_cell,
        "net_contact_energy_J_m2": ein,
        "surface_loss_J_m2": qloss,
        "stored_heat_J_m2": stored,
        "energy_residual_J_m2": err,
        "energy_residual_pct_of_contact_energy": 100 * err / max(abs(ein), 1e-12),
        "final_node_temperatures_C": T.tolist(),
        "max_explicit_dt_row_sum_ratio": estimate_explicit_row_ratio(case, cells_per_layer, dt),
    }


def original_five_node(case: dict, dt: float = DT) -> dict:
    out = legacy.simulate_thermal_batch([case], dt=dt)
    return {
        "peak_eva_C": float(max(out["peak"][0, 1], out["peak"][0, 3])),
        "peak_cell_C": float(out["peak"][0, 2]),
        "net_contact_energy_J_m2": float(out["Ein"][0]),
        "energy_residual_pct_of_contact_energy": float(out["energy_error_pct"][0]),
        "final_node_temperatures_C": out["T"][0].tolist(),
    }


def write_anova_plot(result: dict, path: Path):
    W, H = 1800, 1130
    im = Image.new("RGB", (W, H), "#fbfaf7")
    d = ImageDraw.Draw(im)
    def font(size, bold=False):
        name = r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            return ImageFont.load_default()
    d.rectangle((0, 0, W, 20), fill="#103143")
    d.text((100, 66), "THERMAL SWEEP · MAIN-EFFECT VARIANCE", font=font(42, True), fill="#103143")
    d.text((100, 122), "5,040 designed scenarios | balanced full factorial | equal scenario weights", font=font(25), fill="#55717d")
    colors = ["#157a83", "#c8813b", "#466a86", "#4f8d72", "#8e6a9e", "#bb5d52", "#7f8d93"]
    panels = list(result["metrics"].items())
    top = 205
    panel_h = 270
    for pidx, (metric, mdata) in enumerate(panels):
        y0 = top + pidx * 292
        d.text((100, y0), metric, font=font(26, True), fill="#103143")
        comps = mdata["main_effects"]
        maxval = max([c["share_of_total_variance_pct"] for c in comps] + [1])
        label_x, bar_x = 105, 600
        for j, comp in enumerate(comps):
            y = y0 + 48 + 29 * j
            share = comp["share_of_total_variance_pct"]
            d.text((label_x, y), comp["factor"], font=font(20), fill="#274653")
            width = int(780 * share / maxval)
            d.rounded_rectangle((bar_x, y + 2, bar_x + max(2, width), y + 21), radius=6, fill=colors[j])
            d.text((bar_x + 795, y - 1), f"{share:6.2f}%", font=font(19, True), fill="#103143")
        d.text((1510, y0 + 47), f"interaction /\nunallocated\n{mdata['unallocated_interaction_and_residual_share_pct']:.2f}%", font=font(17), fill="#7b4f36", spacing=4)
    d.text((100, H - 70), "Variance shares describe this scenario grid only; they are not probabilities, uncertainty bounds, or measured process effects.", font=font(20), fill="#55717d")
    im.save(path, dpi=(300, 300))


def write_mesh_plot(mesh_df: pd.DataFrame, path: Path):
    W, H = 1800, 1260
    im = Image.new("RGB", (W, H), "#fbfaf7")
    d = ImageDraw.Draw(im)
    def font(size, bold=False):
        name = r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            return ImageFont.load_default()
    d.rectangle((0, 0, W, 20), fill="#103143")
    d.text((90, 55), "OPTIONAL HOT-KNIFE MODEL | SPATIAL REFINEMENT", font=font(36, True), fill="#103143")
    d.text((90, 108), "Difference from 16 cells per layer (%) | Backward Euler, Δt = 0.5 ms | Four selected cases", font=font(21), fill="#55717d")
    cases = list(mesh_df.case_id.unique())
    colors = ["#157a83", "#c8813b", "#466a86", "#bb5d52"]
    metrics = [
        ("peak_eva_C_relative_difference_vs_N16_pct", "Peak EVA temperature | relative difference (%)"),
        ("peak_cell_C_relative_difference_vs_N16_pct", "Peak cell temperature | relative difference (%)"),
        ("net_contact_energy_J_m2_relative_difference_vs_N16_pct", "Integrated contact energy | relative difference (%)"),
    ]
    ns = sorted(mesh_df.cells_per_layer.unique())
    panel_h = 310
    for panel, (col, title) in enumerate(metrics):
        y0 = 170 + panel * 330
        x0, x1 = 180, 1450
        ytop, ybottom = y0 + 45, y0 + 275
        vals = mesh_df[col].astype(float)
        vmin, vmax = float(vals.min()), float(vals.max())
        pad = max((vmax - vmin) * .10, 0.25)
        vmin -= pad; vmax += pad
        d.text((90, y0), title, font=font(23, True), fill="#103143")
        d.line((x0, ytop, x0, ybottom, x1, ybottom), fill="#70848c", width=2)
        for tick in range(5):
            value = vmin + (vmax - vmin) * tick / 4
            y = ybottom - (ybottom - ytop) * tick / 4
            d.line((x0, y, x1, y), fill="#e2e7e5", width=1)
            d.text((35, y - 12), f"{value:.3g}", font=font(19), fill="#55717d")
        xcoords = [x0 + (x1 - x0) * math.log2(n) / math.log2(max(ns)) for n in ns]
        for idx, case_id in enumerate(cases):
            subset = mesh_df[mesh_df.case_id == case_id].sort_values("cells_per_layer")
            pts = []
            for x, (_, row) in zip(xcoords, subset.iterrows()):
                y = ybottom - (ybottom - ytop) * (float(row[col]) - vmin) / (vmax - vmin)
                pts.append((int(x), int(y)))
            d.line(pts, fill=colors[idx], width=4)
            for px, py in pts:
                d.ellipse((px - 6, py - 6, px + 6, py + 6), fill=colors[idx], outline="#fbfaf7", width=2)
        for x, n in zip(xcoords, ns):
            d.text((int(x) - 12, ybottom + 10), str(n), font=font(19), fill="#274653")
    legend_y = 1180
    for idx, case_id in enumerate(cases):
        x = 230 + idx * 310
        d.line((x, legend_y + 10, x + 42, legend_y + 10), fill=colors[idx], width=4)
        d.text((x + 54, legend_y), case_id.replace("_", " "), font=font(21), fill="#274653")
    im.save(path, dpi=(300, 300))


def main():
    df = load_thermal_sweep()
    anova = variance_decomposition(df)
    (PROCESSED / "PE-SIM-001_main_effect_variance.json").write_text(json.dumps(anova, indent=2), encoding="utf-8")
    write_anova_plot(anova, FIGURES / "PE-SIM-001_main_effect_variance.png")

    mesh_rows = []
    verification = []
    for case_id, case in CASES:
        ref1 = original_five_node(case)
        for n in (1, 2, 4, 8, 16):
            out = simulate_fv(case, n)
            row = {"simulation_id": "PE-SIM-002", "case_id": case_id, "cells_per_layer": n,
                   "total_control_volumes": 5 * n, "time_step_s": DT, "tool_C": case["tool"],
                   "contact_conductance_W_m2K": case["hc"], "contact_duration_s": case["duration"],
                   "ambient_C": case["ambient"], "EVA_total_thickness_mm": case["eva_mm"],
                   "property_set": case["property_set"], "interface_resistance_m2K_W": case["rint"],
                   **{k: v for k, v in out.items() if k != "final_node_temperatures_C"}}
            mesh_rows.append(row)
            if n == 1:
                verification.append({
                    "case_id": case_id,
                    "five_node_baseline": ref1,
                    "finite_volume_N1": {k: out[k] for k in ("peak_eva_C", "peak_cell_C", "net_contact_energy_J_m2", "energy_residual_pct_of_contact_energy")},
                    "differences": {
                        key: float(out[key] - ref1[key]) for key in ("peak_eva_C", "peak_cell_C", "net_contact_energy_J_m2")
                    },
                })
    mesh_df = pd.DataFrame(mesh_rows)
    for case_id in mesh_df.case_id.unique():
        mask = mesh_df.case_id == case_id
        for output in ("peak_eva_C", "peak_cell_C", "net_contact_energy_J_m2"):
            ref = float(mesh_df.loc[mask & (mesh_df.cells_per_layer == 16), output].iloc[0])
            mesh_df.loc[mask, output + "_difference_vs_N16"] = mesh_df.loc[mask, output] - ref
            mesh_df.loc[mask, output + "_relative_difference_vs_N16_pct"] = 100 * (mesh_df.loc[mask, output] - ref) / max(abs(ref), 1e-12)
    mesh_df.to_csv(PROCESSED / "PE-SIM-002_spatial_refinement.csv", index=False, float_format="%.10g")
    (PROCESSED / "PE-SIM-002_N1_coarse_model_verification.json").write_text(json.dumps(verification, indent=2), encoding="utf-8")
    write_mesh_plot(mesh_df, FIGURES / "PE-SIM-002_spatial_refinement.png")

    time_rows = []
    for case_id, case in (CASES[1], CASES[3]):
        for time_step in (0.001, 0.0005, 0.00025):
            result = simulate_fv(case, cells_per_layer=16, dt=time_step)
            time_rows.append({"simulation_id": "PE-SIM-003", "case_id": case_id,
                              "cells_per_layer": 16, "total_control_volumes": 80,
                              "time_step_s": time_step, "peak_eva_C": result["peak_eva_C"],
                              "peak_cell_C": result["peak_cell_C"],
                              "net_contact_energy_J_m2": result["net_contact_energy_J_m2"],
                              "energy_residual_pct_of_contact_energy": result["energy_residual_pct_of_contact_energy"],
                              "explicit_dt_row_sum_ratio": result["max_explicit_dt_row_sum_ratio"]})
    time_df = pd.DataFrame(time_rows)
    for case_id in time_df.case_id.unique():
        mask = time_df.case_id == case_id
        for output in ("peak_eva_C", "peak_cell_C", "net_contact_energy_J_m2"):
            ref = float(time_df.loc[mask & (time_df.time_step_s == 0.00025), output].iloc[0])
            time_df.loc[mask, output + "_difference_vs_0p25ms"] = time_df.loc[mask, output] - ref
            time_df.loc[mask, output + "_relative_difference_vs_0p25ms_pct"] = 100 * (time_df.loc[mask, output] - ref) / max(abs(ref), 1e-12)
    time_df.to_csv(PROCESSED / "PE-SIM-003_timestep_refinement.csv", index=False, float_format="%.10g")

    summary = {
        "phase": "E", "run_date": date.today().isoformat(),
        "environment": {"python": sys.version, "platform": platform.platform(), "numpy": np.__version__, "pandas": pd.__version__, "pillow": Image.__version__},
        "PE-SIM-001": {
            "source_data": str(INPUT_CSV), "filter": "record_type=thermal_case_summary and experiment_id=EXP-S3-02",
            "row_count": int(len(df)), "factorial_design_balanced": True,
            "interpretation": "Equal-weight main-effect variance decomposition of a deterministic designed sweep; unallocated share comprises interactions and any numerical residual, not uncertainty probability.",
            "metrics": {k: {"range": [v["minimum"], v["maximum"]], "mean": v["mean"],
                            "top_three_factors": v["main_effects"][:3],
                            "unallocated_share_pct": v["unallocated_interaction_and_residual_share_pct"]}
                        for k, v in anova["metrics"].items()},
        },
        "PE-SIM-002": {
            "model": "1D finite-volume extension of the historical five-layer thermal RC model; uniform subdivisions within layers; zero-capacity algebraic blade/interface node retained; backward Euler with Picard iterations for nonlinear surface radiation.",
            "case_count": len(CASES), "cells_per_layer": [1, 2, 4, 8, 16], "time_step_s": DT,
            "rows": int(len(mesh_df)), "maximum_energy_residual_abs_pct": float(mesh_df.energy_residual_pct_of_contact_energy.abs().max()),
            "minimum_explicit_dt_row_sum_ratio": float(mesh_df.max_explicit_dt_row_sum_ratio.min()),
            "maximum_explicit_dt_row_sum_ratio": float(mesh_df.max_explicit_dt_row_sum_ratio.max()),
            "solver_note": "The 0.5 ms explicit stability ratio exceeds unity on refined meshes because of silicon's small control volumes. The completed refinement uses backward Euler; this ratio is retained to explain why explicit integration was rejected.",
            "max_N1_vs_original_absolute_difference": {
                "peak_eva_C": max(abs(v["differences"]["peak_eva_C"]) for v in verification),
                "peak_cell_C": max(abs(v["differences"]["peak_cell_C"]) for v in verification),
                "net_contact_energy_J_m2": max(abs(v["differences"]["net_contact_energy_J_m2"]) for v in verification),
            },
            "N16_results": [],
            "limitations": ["No experimental validation; all material and boundary inputs are inherited assumptions.", "One-dimensional conduction only; no moving blade, spatial contact variation, delamination/fracture, EVA kinetics, volatile emissions, or actual feedstock.", "The spatial mesh refines the same model form and cannot establish its physical correctness."],
        },
        "PE-SIM-003": {
            "model": "Same backward-Euler spatially refined model at 16 control volumes per layer group; timestep-only comparison for nominal and high-bound selected conditions.",
            "rows": int(len(time_df)), "time_steps_s": [0.001, 0.0005, 0.00025],
            "reference_time_step_s": 0.00025,
            "maximum_absolute_relative_difference_0p5ms_vs_0p25ms_pct": {
                out: float(time_df.loc[time_df.time_step_s == 0.0005, out + "_relative_difference_vs_0p25ms_pct"].abs().max())
                for out in ("peak_eva_C", "peak_cell_C", "net_contact_energy_J_m2")
            },
            "maximum_energy_residual_abs_pct": float(time_df.energy_residual_pct_of_contact_energy.abs().max()),
            "validation": "Numerical timestep sensitivity only; no physical measurements.",
        },
    }
    for case_id in mesh_df.case_id.unique():
        row = mesh_df.loc[(mesh_df.case_id == case_id) & (mesh_df.cells_per_layer == 16)].iloc[0]
        summary["PE-SIM-002"]["N16_results"].append({"case_id": case_id, "peak_eva_C": float(row.peak_eva_C), "peak_cell_C": float(row.peak_cell_C), "net_contact_energy_J_m2": float(row.net_contact_energy_J_m2)})
    (PROCESSED / "phase_e_experiment_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({
        "PE-SIM-001_rows": len(df),
        "PE-SIM-001_top_factors": {k: [(i["factor"], round(i["share_of_total_variance_pct"], 3)) for i in v["main_effects"][:3]] for k, v in anova["metrics"].items()},
        "PE-SIM-002_rows": len(mesh_df),
        "N1_max_diff": summary["PE-SIM-002"]["max_N1_vs_original_absolute_difference"],
        "energy_residual_pct_abs_max": summary["PE-SIM-002"]["maximum_energy_residual_abs_pct"],
        "explicit_dt_row_sum_ratio_max": summary["PE-SIM-002"]["maximum_explicit_dt_row_sum_ratio"],
        "outputs": [str(PROCESSED), str(FIGURES / "PE-SIM-001_main_effect_variance.png"), str(FIGURES / "PE-SIM-002_spatial_refinement.png")],
    }, indent=2))


if __name__ == "__main__":
    main()
