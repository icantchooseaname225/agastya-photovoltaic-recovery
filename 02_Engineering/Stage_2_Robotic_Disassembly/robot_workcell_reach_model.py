#!/usr/bin/env python3
"""Top-view reach screening for a PV-module perimeter-disassembly workcell.

This deterministic geometric screen is deliberately not an inverse-kinematics,
collision, payload, torque, or safety simulation.  It identifies whether a
candidate nominal radial reach can cover sampled perimeter task points from a
chosen base location.  All dimensions are user-editable assumptions.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import sys
from collections import defaultdict
from pathlib import Path

DEFAULT_LENGTH_MM = 2278.0
DEFAULT_WIDTH_MM = 1134.0
DEFAULT_STANDOFF_MM = 300.0
DEFAULT_SPACING_MM = 100.0
DEFAULT_REACHES_MM = (1200.0, 1500.0, 1800.0, 2000.0)
OUTPUT_DIR = Path(__file__).resolve().parent / "simulation_outputs"


def edge_points(length_mm: float, width_mm: float, spacing_mm: float):
    half_l, half_w = length_mm / 2.0, width_mm / 2.0
    edges = (
        ("near_long", (-half_l, -half_w), (half_l, -half_w)),
        ("far_short", (half_l, -half_w), (half_l, half_w)),
        ("far_long", (half_l, half_w), (-half_l, half_w)),
        ("near_short", (-half_l, half_w), (-half_l, -half_w)),
    )
    points = []
    for edge_name, start, end in edges:
        span = math.dist(start, end)
        intervals = max(1, math.ceil(span / spacing_mm))
        for i in range(intervals):
            t = i / intervals
            x = start[0] + (end[0] - start[0]) * t
            y = start[1] + (end[1] - start[1]) * t
            points.append((edge_name, x, y))
    # Add the final point once so every corner is included exactly once.
    points.append(("near_short", -half_l, -half_w))
    return points


def svg_diagram(length_mm, width_mm, base_x_mm, base_y_mm, reach_list, points, path):
    width_px, height_px = 1120, 840
    cx, cy, scale = 560.0, 405.0, 150.0 / 1000.0
    px = lambda x: cx + x * scale
    py = lambda y: cy - y * scale
    panel_x = cx - (length_mm / 2.0) * scale
    panel_y = cy - (width_mm / 2.0) * scale
    panel_w, panel_h = length_mm * scale, width_mm * scale
    base_px, base_py = px(base_x_mm), py(base_y_mm)
    colors = {1200.0: "#4e79a7", 1500.0: "#f28e2b", 1800.0: "#59a14f", 2000.0: "#b07aa1"}
    chunks = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width_px}" height="{height_px}" viewBox="0 0 {width_px} {height_px}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="32" y="38" font-family="Arial,sans-serif" font-size="24" font-weight="700">Stage 2 perimeter reach screen (top view)</text>',
        '<text x="32" y="64" font-family="Arial,sans-serif" font-size="14" fill="#444">Illustrative panel and base assumptions; dashed circles show nominal radial reach only</text>',
    ]
    for reach in reach_list:
        color = colors.get(reach, "#777777")
        radius = reach * scale
        chunks.append(f'<circle cx="{base_px:.1f}" cy="{base_py:.1f}" r="{radius:.1f}" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="8 7" opacity="0.85"/>')
    chunks.append(f'<rect x="{panel_x:.1f}" y="{panel_y:.1f}" width="{panel_w:.1f}" height="{panel_h:.1f}" rx="5" fill="#f4f7fa" fill-opacity="0.94" stroke="#223344" stroke-width="3"/>')
    chunks.append(f'<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" font-family="Arial,sans-serif" font-size="15">PV module plan</text>')
    for i, (edge, x, y) in enumerate(points):
        chunks.append(f'<circle cx="{px(x):.1f}" cy="{py(y):.1f}" r="2.1" fill="#253746"><title>{edge} task point {i+1}</title></circle>')
    chunks.append(f'<circle cx="{base_px:.1f}" cy="{base_py:.1f}" r="8" fill="#d62728" stroke="#ffffff" stroke-width="2"/>')
    chunks.append(f'<text x="{base_px+13:.1f}" y="{base_py+5:.1f}" font-family="Arial,sans-serif" font-size="14" fill="#8c1d18">arm base</text>')
    legend_y = 735
    chunks.append('<text x="32" y="708" font-family="Arial,sans-serif" font-size="14" font-weight="700">Nominal reach circles</text>')
    for i, reach in enumerate(reach_list):
        color = colors.get(reach, "#777777")
        x = 32 + i * 250
        chunks.append(f'<line x1="{x}" y1="{legend_y}" x2="{x+48}" y2="{legend_y}" stroke="{color}" stroke-width="3" stroke-dasharray="8 7"/>')
        chunks.append(f'<text x="{x+58}" y="{legend_y+5}" font-family="Arial,sans-serif" font-size="14">{reach/1000:.1f} m</text>')
    chunks.append('<text x="32" y="785" font-family="Arial,sans-serif" font-size="13" fill="#444">Reach circles ignore height, link orientation, singularities, collisions, tool approach, force, payload, and safety limits.</text>')
    chunks.append('</svg>')
    path.write_text("\n".join(chunks), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--length-mm", type=float, default=DEFAULT_LENGTH_MM)
    parser.add_argument("--width-mm", type=float, default=DEFAULT_WIDTH_MM)
    parser.add_argument("--base-standoff-mm", type=float, default=DEFAULT_STANDOFF_MM,
                        help="distance from arm base to the nearest long panel edge")
    parser.add_argument("--spacing-mm", type=float, default=DEFAULT_SPACING_MM)
    args = parser.parse_args()
    if min(args.length_mm, args.width_mm, args.spacing_mm) <= 0 or args.base_standoff_mm < 0:
        parser.error("length, width and spacing must be positive; standoff cannot be negative")

    length, width, spacing = args.length_mm, args.width_mm, args.spacing_mm
    base_x, base_y = 0.0, -(width / 2.0 + args.base_standoff_mm)
    reaches = DEFAULT_REACHES_MM
    points = edge_points(length, width, spacing)
    rows = []
    by_edge = defaultdict(list)
    distances = []
    for i, (edge, x, y) in enumerate(points, start=1):
        distance = math.hypot(x - base_x, y - base_y)
        distances.append(distance)
        by_edge[edge].append(distance)
        row = {
            "task_point_id": f"P{i:03d}", "edge": edge,
            "x_mm": round(x, 3), "y_mm": round(y, 3),
            "arm_base_x_mm": round(base_x, 3), "arm_base_y_mm": round(base_y, 3),
            "base_to_point_radius_mm": round(distance, 3),
        }
        for reach in reaches:
            row[f"within_{int(reach)}mm_nominal_reach"] = distance <= reach
        rows.append(row)

    sorted_d = sorted(distances)
    p95 = sorted_d[max(0, math.ceil(0.95 * len(sorted_d)) - 1)]
    reach_summary = []
    edge_summary = {}
    for edge, edge_d in sorted(by_edge.items()):
        edge_summary[edge] = {"sampled_points": len(edge_d), "max_radius_mm": round(max(edge_d), 3)}
    for reach in reaches:
        within = sum(d <= reach for d in distances)
        reach_summary.append({
            "nominal_reach_mm": int(reach),
            "sampled_points_reachable": within,
            "sampled_points_total": len(distances),
            "sampled_perimeter_coverage_percent": round(100.0 * within / len(distances), 2),
        })

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / "perimeter_task_points.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "run_id": "S2-REACH-20261119-01",
        "model_type": "2D top-view radial reach screen",
        "created_by": Path(__file__).name,
        "python_version": platform.python_version(),
        "geometry_assumptions": {
            "panel_length_mm": length, "panel_width_mm": width,
            "panel_aspect_orientation": "length on x axis; centered at origin",
            "robot_base_x_mm": base_x, "robot_base_y_mm": base_y,
            "base_standoff_from_near_long_edge_mm": args.base_standoff_mm,
            "perimeter_sampling_spacing_mm": spacing,
            "reach_values_mm": list(reaches),
        },
        "results": {
            "sampled_perimeter_points": len(points),
            "maximum_sampled_base_radius_mm": round(max(distances), 3),
            "minimum_nominal_radial_reach_for_all_sampled_points_mm": round(max(distances), 3),
            "95th_percentile_sampled_radius_mm_nearest_rank": round(p95, 3),
            "coverage_by_reach": reach_summary,
            "edge_summary": edge_summary,
        },
        "limitations": [
            "Reachability means only planar base-to-point radius is within a scalar reach value.",
            "No robot link geometry, joint limits, inverse kinematics, tool orientation, singularity, or collision checks.",
            "No vertical dimension, end-effector design, payload, torque, force, speed, repeatability, cycle-time, or safety model.",
            "Sampled point coverage is geometric point coverage, not process success probability or production performance.",
            "Panel dimensions and base standoff are illustrative assumptions pending a measured AGASTYA feed and workcell layout.",
        ],
        "interpretation": "Screening evidence for choosing between a fixed base, panel indexer, or linear robot rail. It is not a robot selection or validated motion plan.",
    }
    json_path = OUTPUT_DIR / "reach_screen_summary.json"
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    svg_path = OUTPUT_DIR / "reach_envelope.svg"
    svg_diagram(length, width, base_x, base_y, reaches, points, svg_path)

    lines = [
        "# Stage 2 robotic workcell reach screen",
        "",
        f"**Run ID:** {summary['run_id']}  ",
        f"**Execution:** Python {platform.python_version()} standard library  ",
        "**Status:** executed geometric screen; not validated robot motion.",
        "",
        "## Question",
        "Can one stationary arm base geometrically reach sampled perimeter task points on an illustrative module from one long-side work position, and how much reach is needed?",
        "",
        "## Model and assumptions",
        "",
        f"- Rectangular panel: {length:.0f} × {width:.0f} mm, centered at (0, 0); these are scenario dimensions, not an AGASTYA-measured panel.",
        f"- Arm base projection: (0, {base_y:.0f}) mm; {args.base_standoff_mm:.0f} mm beyond the near long edge.",
        f"- Perimeter task points: {len(points)} sampled at no more than {spacing:.0f} mm spacing, including all four corners.",
        "- Reachability rule: planar Euclidean distance from base projection ≤ scalar nominal reach.",
        "- No kinematic, payload, force, collision, speed, cycle-time, sensor, or safety assumptions are encoded.",
        "",
        "## Results",
        "",
        f"- Maximum sampled base-to-perimeter radius: **{max(distances):.1f} mm**.",
        f"- Reach required to include all sampled points under this planar rule: **{max(distances):.1f} mm**.",
        f"- 95th-percentile sampled radius (nearest-rank): **{p95:.1f} mm**.",
        "",
        "| Nominal radial reach | Sampled points within radius |",
        "|---:|---:|",
    ]
    for row in reach_summary:
        lines.append(f"| {row['nominal_reach_mm']} mm | {row['sampled_points_reachable']}/{row['sampled_points_total']} ({row['sampled_perimeter_coverage_percent']:.2f}%) |")
    lines += [
        "",
        "![Top-view reach circles and sampled panel perimeter](reach_envelope.svg)",
        "",
        "## Engineering interpretation",
        "",
        "The screen shows whether a nominal radial reach is plainly too short for a single fixed-base perimeter tool path in this illustrative layout. If the required reach is impractical for payload, cost, stiffness, or guarding, a panel indexer or robot linear rail can reduce the required arm reach. That trade cannot be quantified until the actual module dimensions, station layout, tool approach directions, and fixture are measured.",
        "",
        "Use the arm to position and control task-specific tools while the module remains supported by a fixture. The arm should not be assumed to lift the complete module. Frame release and junction-box/cable removal likely need different tools and access orientations; a quick tool changer or separate dedicated actuator must be compared against one tool doing both. No actuator, robot model, joint configuration, or payload rating is selected here.",
        "",
        "## Limits and next input",
        "",
        "This is a reproducible 2D reach screen. It does not prove inverse-kinematic reachability, tool orientation, collision clearance, structural rigidity, repeatability, frame release forces, cycle time, or safety. Replace the scenario dimensions with measured target-module dimensions, then build a 3D CAD/workcell model and evaluate manufacturer robot data before choosing an arm. Measure frame-release and junction-box removal forces on approved representative material before actuator sizing.",
        "",
        "Outputs: `perimeter_task_points.csv`, `reach_screen_summary.json`, and `reach_envelope.svg`.",
    ]
    report_path = OUTPUT_DIR / "model_report.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"summary": summary["results"], "outputs": [str(csv_path), str(json_path), str(svg_path), str(report_path)]}, indent=2))


if __name__ == "__main__":
    main()
