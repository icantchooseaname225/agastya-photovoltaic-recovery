# Phase E simulation campaign

The campaign contains raw preserved failures, processed calculations and figures generated from documented models. Read `../../Simulation_Register.csv` for status and limitations.

- `models/run_phase_e_experiments.py` runs PE-SIM-001/002/003.
- `raw/` preserves the first unstable explicit-Euler spatial-refinement outputs; do not use them as results.
- `processed/` contains sensitivity JSON, spatial and timestep CSVs, coarse-model comparison and the experiment summary.
- `figures/` contains 300 dpi plots.

Run from the project environment with Python, NumPy, pandas and Pillow installed:

```powershell
python .\models\run_phase_e_experiments.py
```

All experiments are deterministic model calculations for a historical thermal model that now maps to current Stage 3. They do not predict delamination quality or Stage 4 silver removal. There are no physical inputs or independent validation measurements.
