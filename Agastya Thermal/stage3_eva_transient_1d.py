#!/usr/bin/env python3
"""Idealized 1D transient heat diffusion through an EVA layer; not a process model."""
from __future__ import annotations
import csv, json, math, platform
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "stage3_eva_model_outputs"
K_W_MK = 0.34
RHO_KG_M3 = 951.0
CP_J_KG_K = 1400.0
THICKNESS_M = 0.0005
INITIAL_C = 25.0
BOUNDARY_C = 100.0
N_NODES = 51
END_TIME_S = 5.0
SNAPSHOTS_S = [0.0,0.05,0.1,0.25,0.5,1.0,2.0,5.0]


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    alpha=K_W_MK/(RHO_KG_M3*CP_J_KG_K)
    dx=THICKNESS_M/(N_NODES-1)
    dt=0.4*dx*dx/(2.0*alpha)
    nsteps=math.ceil(END_TIME_S/dt)
    dt=END_TIME_S/nsteps
    Fo=alpha*dt/(dx*dx)
    t=[INITIAL_C]*N_NODES
    profile_rows=[]
    energy_rows=[]
    def record(time_s, values):
        for j,temp in enumerate(values):
            profile_rows.append({"time_s":time_s,"depth_from_hot_face_mm":j*dx*1000.0,"temperature_C":temp})
        integral=sum(((values[j]-INITIAL_C)+(values[j+1]-INITIAL_C))*0.5 for j in range(N_NODES-1))*dx
        energy=rho_cp*integral
        energy_rows.append({"time_s":time_s,"mean_temperature_C":sum(values)/N_NODES,"rear_face_temperature_C":values[-1],"sensible_energy_added_J_m2":energy})
    rho_cp=RHO_KG_M3*CP_J_KG_K
    record(0.0,t)
    target_steps={round(x,9):round(x/dt) for x in SNAPSHOTS_S if x>0}
    for step in range(1,nsteps+1):
        old=t
        new=old.copy()
        for j in range(1,N_NODES-1):
            new[j]=old[j]+Fo*(old[j-1]-2.0*old[j]+old[j+1])
        new[0]=BOUNDARY_C
        new[-1]=new[-2]  # insulated reverse face: zero temperature gradient
        t=new
        if step in target_steps.values():
            time_s=step*dt
            record(time_s,t)
    with (OUT/"temperature_profiles.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(profile_rows[0]));w.writeheader();w.writerows(profile_rows)
    with (OUT/"energy_summary.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(energy_rows[0]));w.writeheader();w.writerows(energy_rows)
    summary={"model":"1D explicit finite-difference heat diffusion in a homogeneous EVA slab","property_source":"Tomšič et al. (2025; first published 2024), Advanced Theory and Simulations 8(3), 2401026, DOI 10.1002/adts.202401026, Table 1","python_version":platform.python_version(),"inputs":{"thermal_conductivity_W_mK":K_W_MK,"density_kg_m3":RHO_KG_M3,"specific_heat_J_kgK":CP_J_KG_K,"thickness_m":THICKNESS_M,"initial_temperature_C":INITIAL_C,"hot_face_boundary_temperature_C":BOUNDARY_C,"reverse_face_boundary":"insulated, zero gradient","nodes":N_NODES,"dx_m":dx,"dt_s":dt,"end_time_s":END_TIME_S,"time_steps":nsteps},"derived":{"thermal_diffusivity_m2_s":alpha,"fourier_number":Fo,"characteristic_thickness_diffusion_time_s":THICKNESS_M**2/alpha,"uniform_slab_sensible_energy_to_boundary_temperature_J_m2":rho_cp*THICKNESS_M*(BOUNDARY_C-INITIAL_C)},"snapshots":energy_rows,"limitations":["Idealized constant-property 1D EVA slab only; property values are literature inputs, not measured AGASTYA material values.","Prescribed 100 C hot-face temperature is an ideal boundary condition, not a hot-knife temperature or contact model.","No glass, cells, backsheet, adhesive chemistry, moisture, contact resistance, moving knife, foam roller, peel/fracture, convection, losses, power, throughput, emissions, or separation-quality model.","The calculated energy is sensible heat within the idealized layer and excludes equipment losses and other layers.","No experimental validation; outputs do not establish safe operating conditions or delamination."],"validation_needed":"Measure temperature-dependent properties and boundary/contact histories on approved coupons; compare instrumented profiles and energy with a qualified supervised setup."}
    (OUT/"model_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    # Self-contained SVG: temperature profiles by time, rendered without plotting libraries.
    colors=["#4e79a7","#f28e2b","#e15759","#76b7b2","#59a14f","#edc948","#b07aa1","#ff9da7"]
    width,height=900,560; left,right,top,bottom=90,35,55,75
    plotw,ploth=width-left-right,height-top-bottom
    def X(depth_mm): return left+depth_mm/(THICKNESS_M*1000)*plotw
    def Y(temp): return top+(BOUNDARY_C-temp)/(BOUNDARY_C-INITIAL_C)*ploth
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">','<rect width="100%" height="100%" fill="white"/>','<text x="36" y="32" font-family="Arial" font-size="20" font-weight="bold">Idealized EVA slab temperature profiles</text>']
    for val in [25,40,55,70,85,100]:
        yy=Y(val);parts.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" stroke="#ddd"/>');parts.append(f'<text x="{left-12}" y="{yy+5:.1f}" text-anchor="end" font-family="Arial" font-size="12">{val} C</text>')
    for mm in [0,0.1,0.2,0.3,0.4,0.5]:
        xx=X(mm);parts.append(f'<line x1="{xx:.1f}" y1="{top}" x2="{xx:.1f}" y2="{height-bottom}" stroke="#eee"/>');parts.append(f'<text x="{xx:.1f}" y="{height-bottom+24}" text-anchor="middle" font-family="Arial" font-size="12">{mm:.1f}</text>')
    for i,row in enumerate(energy_rows):
        vals=[r["temperature_C"] for r in profile_rows if r["time_s"]==row["time_s"]]
        pts=" ".join(f'{X(j*dx*1000):.1f},{Y(v):.1f}' for j,v in enumerate(vals))
        parts.append(f'<polyline points="{pts}" fill="none" stroke="{colors[i%len(colors)]}" stroke-width="2.5"/>')
        parts.append(f'<text x="{width-180}" y="{top+20*i}" font-family="Arial" font-size="12" fill="{colors[i%len(colors)]}">{row["time_s"]:.3f} s</text>')
    parts += [f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#333"/>',f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#333"/>',f'<text x="{width/2}" y="{height-20}" text-anchor="middle" font-family="Arial" font-size="14">Depth from ideal hot face (mm)</text>',f'<text x="24" y="{height/2}" transform="rotate(-90 24 {height/2})" text-anchor="middle" font-family="Arial" font-size="14">Temperature (C)</text>','<text x="520" y="520" font-family="Arial" font-size="12" fill="#555">Boundary-condition sensitivity study only; not a delamination or equipment prediction.</text>','</svg>']
    (OUT/"temperature_profiles.svg").write_text("\n".join(parts),encoding="utf-8")
    print(f"python={platform.python_version()} alpha_m2_s={alpha:.9g} dt_s={dt:.9g} steps={nsteps}")
    print(f"outputs={OUT}")
    print(f"5s_rear_face_C={energy_rows[-1]['rear_face_temperature_C']:.3f} 5s_energy_J_m2={energy_rows[-1]['sensible_energy_added_J_m2']:.1f}")

if __name__=="__main__": main()



