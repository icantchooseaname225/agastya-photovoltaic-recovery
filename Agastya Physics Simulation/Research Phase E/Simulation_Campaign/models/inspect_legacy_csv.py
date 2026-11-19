import csv
import sys
from collections import Counter

p = r"D:\Agastya\Agastya Physics Simulation\Agastya_Physics_Simulation_2026-10-10.csv"
counts = Counter()
examples = []
with open(p, encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        if row["experiment_id"].startswith("EXP-S3"):
            counts[(row["experiment_id"], row["record_type"])] += 1
            if len(examples) < 12:
                examples.append((row["experiment_id"], row["record_type"], row["scenario_id"]))
print(counts)
print(examples)

import importlib.util
sys_path = r"D:\Agastya\Agastya Physics Simulation\Research Phase E\Simulation_Campaign\models\run_phase_e_experiments.py"
spec = importlib.util.spec_from_file_location("phase_e", sys_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for case_id, case in mod.CASES[:1]:
    for n in (1, 2, 4, 8, 16):
        dx, k, cap, li, edge, gi, ei, gg, ge = mod.expanded_nodes(case, n)
        row = [0.0] * len(cap)
        for j, g in enumerate(edge):
            row[j] += g; row[j+1] += g
        h=case["hc"]; den=h+gg+ge; row[gi]+=h*gg/den+gg*ge/den; row[ei]+=h*ge/den+gg*ge/den
        row[0]+=20; row[-1]+=20
        rates=[row[j]/cap[j] for j in range(len(cap))]
        ix=max(range(len(cap)),key=rates.__getitem__)
        print("stability",n,"node",ix,"layer",li[ix],"dx",dx[ix],"cap",cap[ix],"rate",rates[ix],"dtmax",2/rates[ix],"ratio",rates[ix]*mod.DT)
