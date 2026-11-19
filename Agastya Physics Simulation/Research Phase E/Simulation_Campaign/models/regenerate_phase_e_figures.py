import json
from pathlib import Path
import pandas as pd
import run_phase_e_experiments as model

base = Path(__file__).resolve().parents[1]
processed = base / "processed"
figures = base / "figures"
anova = json.loads((processed / "PE-SIM-001_main_effect_variance.json").read_text(encoding="utf-8"))
mesh = pd.read_csv(processed / "PE-SIM-002_spatial_refinement.csv")
model.write_anova_plot(anova, figures / "PE-SIM-001_main_effect_variance.png")
model.write_mesh_plot(mesh, figures / "PE-SIM-002_spatial_refinement.png")
print("Regenerated actual-data plots from processed results.")
