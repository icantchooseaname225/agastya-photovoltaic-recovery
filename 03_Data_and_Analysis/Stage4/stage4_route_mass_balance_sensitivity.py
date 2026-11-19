#!/usr/bin/env python3
"""Reproduce a published flotation mass-pull calculation and ECS routing sensitivity grid."""
from __future__ import annotations
import csv, json, platform
from pathlib import Path

HERE=Path(__file__).resolve().parent
OUT=HERE/"outputs"
# Paired tap-water rougher result on the prepared cell feed in Saffarian et al. (2026).
LITERATURE_AG_RECOVERY=0.9755
LITERATURE_UPGRADE=32.2
FEED_MASS_KG=1.0  # unit-scaling example only; no AGASTYA feed basis
GRID_STEP=0.05    # mathematical sensitivity grid, not measured ECS performance


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    mass_pull=LITERATURE_AG_RECOVERY/LITERATURE_UPGRADE
    concentrate_mass=FEED_MASS_KG*mass_pull
    tail_mass=FEED_MASS_KG-concentrate_mass
    flotation={"study_feed_mass_scale_kg":FEED_MASS_KG,"silver_recovery_fraction":LITERATURE_AG_RECOVERY,"upgrade_factor":LITERATURE_UPGRADE,"derived_mass_pull_fraction":mass_pull,"derived_concentrate_mass_g_per_1kg_feed":concentrate_mass*1000,"derived_tail_mass_g_per_1kg_feed":tail_mass*1000,"normalized_silver_input_units":1.0,"normalized_silver_to_concentrate_units":LITERATURE_AG_RECOVERY,"normalized_silver_to_tail_units":1.0-LITERATURE_AG_RECOVERY,"check_mass_output_fraction":mass_pull+tail_mass/FEED_MASS_KG,"check_normalized_silver_balance":LITERATURE_AG_RECOVERY+(1.0-LITERATURE_AG_RECOVERY)}
    rows=[]
    n=round(1/GRID_STEP)
    for e_i in range(n+1):
        e=round(e_i*GRID_STEP,10) # accepted silver-bearing ECS product fraction
        for p_i in range(n+1):
            p=round(p_i*GRID_STEP,10) # fraction of input Ag routed to flotation
            if e+p>1.0+1e-9: continue
            if p == 0:
                threshold=None
                route_at_benchmark=e
            else:
                threshold=(LITERATURE_AG_RECOVERY-e)/p
                route_at_benchmark=e+p*LITERATURE_AG_RECOVERY
            rows.append({"ecs_accepted_ag_product_fraction_e_sensitivity_only":e,"ag_fraction_routed_to_flotation_p_sensitivity_only":p,"unused_or_unrecovered_ag_fraction_1_minus_e_minus_p":round(1-e-p,10),"required_conditional_flotation_recovery_to_equal_direct_benchmark":None if threshold is None else round(threshold,8),"route_recovery_if_flotation_matches_published_benchmark":round(route_at_benchmark,8),"mathematically_can_match_direct_benchmark_at_r_f_le_1":bool(threshold is not None and threshold<=1.0)})
    with (OUT/"ecs_flotation_break_even_grid.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    with (OUT/"published_flotation_mass_balance.json").open("w",encoding="utf-8") as f:
        json.dump(flotation,f,indent=2)
    summary={"model":"published benchmark arithmetic plus parameter sensitivity; not an AGASTYA process prediction","python_version":platform.python_version(),"benchmark":{"citation":"Saffarian, Galvin & Firouzi (2026), Minerals Engineering 242, 110189, DOI 10.1016/j.mineng.2026.110189","feed":"delaminated, crushed and ground EoL PV cells prepared for laboratory flotation","tap_water_rougher_silver_recovery_fraction":LITERATURE_AG_RECOVERY,"tap_water_rougher_upgrade_factor":LITERATURE_UPGRADE,"derived_mass_pull_fraction":mass_pull},"scale_example":{"prepared_feed_mass_kg":FEED_MASS_KG,"concentrate_mass_g":concentrate_mass*1000,"tail_mass_g":tail_mass*1000,"silver_mass_balance_normalized_to_1_input_unit":{"feed":1.0,"concentrate":LITERATURE_AG_RECOVERY,"tail":1.0-LITERATURE_AG_RECOVERY}},"sensitivity":{"grid_step":GRID_STEP,"grid_rows":len(rows),"e_definition":"fraction of feed silver ending in a separately accepted ECS silver-bearing product; unknown for AGASTYA","p_definition":"fraction of feed silver routed into the flotation feed after ECS; unknown for AGASTYA","route_recovery_equation":"R_total = e + p * r_f, assuming separate measured products with no double counting","break_even_equation":"r_f_required = (0.9755 - e) / p, for p > 0; this compares algebraically with the direct flotation study benchmark","parameters_are":"mathematical grid only; no values are asserted as likely or measured"},"limitations":["The paper feed was prepared cell material; its recovery and upgrade are literature outcomes, not AGASTYA results or guarantees.","The derived mass pull is R/U from a paired study result and does not supply an AGASTYA feed grade or silver mass.","No direct matched-feed ECS versus flotation experiment, ECS silver partition, product acceptance, size partition, or route cost is available.","The simple sequence equation assumes a single accepted ECS silver-bearing product plus a non-overlapping flotation feed; actual stream definitions and assays are required.","The grid is a deterministic parameter sweep, not a probability distribution, equipment simulation, or forecast."],"validation_needed":"Measure total and silver mass in every classification/ECS/flotation stream on a homogenized representative feed; close mass and Ag balances with assay QA/QC, duplicate splits, residues and uncertainty."}
    (OUT/"model_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    # Threshold chart as an SVG; each curve fixes the hypothetical accepted ECS Ag product fraction e.
    width,height=900,560; left,right,top,bottom=90,45,55,75; pw,ph=width-left-right,height-top-bottom
    def X(p): return left+p*pw
    def Y(r): return top+(1-r)*ph
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">','<rect width="100%" height="100%" fill="white"/>','<text x="32" y="32" font-family="Arial" font-size="20" font-weight="bold">ECS-to-flotation break-even sensitivity</text>','<text x="32" y="51" font-family="Arial" font-size="12" fill="#555">Required conditional flotation recovery to match 97.55% direct flotation benchmark</text>']
    for rv in [0,0.25,0.5,0.75,1.0]:
        yy=Y(rv);parts += [f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" stroke="#ddd"/>',f'<text x="{left-12}" y="{yy+4:.1f}" text-anchor="end" font-family="Arial" font-size="12">{rv:.0%}</text>']
    for pv in [0,0.2,0.4,0.6,0.8,1.0]:
        xx=X(pv);parts += [f'<line x1="{xx:.1f}" y1="{top}" x2="{xx:.1f}" y2="{height-bottom}" stroke="#eee"/>',f'<text x="{xx:.1f}" y="{height-bottom+22}" text-anchor="middle" font-family="Arial" font-size="12">{pv:.0%}</text>']
    colors={0.0:"#4e79a7",0.05:"#f28e2b",0.1:"#59a14f",0.2:"#e15759"}
    for e in colors:
        pts=[]
        for i in range(1,101):
            p=i/100
            if e+p>1: continue
            req=(LITERATURE_AG_RECOVERY-e)/p
            if 0<=req<=1: pts.append(f'{X(p):.1f},{Y(req):.1f}')
        if pts: parts.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{colors[e]}" stroke-width="3"/>')
        parts.append(f'<text x="{width-210}" y="{top+20*list(colors).index(e)}" font-family="Arial" font-size="12" fill="{colors[e]}">e = {e:.0%} accepted ECS Ag</text>')
    parts += [f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#333"/>',f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#333"/>',f'<text x="{width/2}" y="{height-20}" text-anchor="middle" font-family="Arial" font-size="14">Silver fraction routed to flotation after ECS, p</text>',f'<text x="24" y="{height/2}" transform="rotate(-90 24 {height/2})" text-anchor="middle" font-family="Arial" font-size="14">Required flotation recovery</text>','<text x="300" y="520" font-family="Arial" font-size="12" fill="#555">Sensitivity only: e and p are unknown; curves do not establish ECS performance.</text>','</svg>']
    (OUT/"ecs_flotation_break_even.svg").write_text("\n".join(parts),encoding="utf-8")
    print(f"python={platform.python_version()} mass_pull={mass_pull:.8f} concentrate_g_per_kg={concentrate_mass*1000:.3f} grid_rows={len(rows)}")
    print(f"outputs={OUT}")

if __name__=="__main__": main()
