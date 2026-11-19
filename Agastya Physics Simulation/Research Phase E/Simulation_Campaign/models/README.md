# Phase E model notes

`run_phase_e_experiments.py` imports the historical model from the project-local `Agastya Physics Simulation` directory, reads the master CSV, runs a balanced-grid main-effect decomposition, then runs one-dimensional finite-volume spatial/timestep studies for a hot-knife-like Stage 3 reference. The model does not predict separation quality or silver recovery.

Dependencies recorded from the bundled runtime: Python 3.12.14, NumPy 2.3.5, pandas 3.0.1, Pillow 12.3.0. Re-run it from the campaign folder or provide the same fixed paths. Inputs and equations are described in the Computational Modeling and Simulation Atlas. Outputs are written to `../processed/` and `../figures/`; raw failed explicit outputs are preserved separately.

No Stage 4 silver-removal model is executable: feed properties, route-specific inputs, measured streams and assays remain absent.
