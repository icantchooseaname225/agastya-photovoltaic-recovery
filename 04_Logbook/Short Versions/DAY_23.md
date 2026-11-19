# Day 23 — Multistage virtual model and follow-up calculations

**Date:** 10 October 2026  
**Status:** Historical numerical work only; no physical samples, trials or assays.  
**Full entry:** [PROJECT_LOGBOOK_DAY_23.md](../PROJECT_LOGBOOK_DAY_23.md)

**Objective:** Explore how documented assumptions affect Stage 2 mass accounting, Stage 3 heat transfer and a Stage 4 size-classification hypothesis.

**Work recorded:** The full historical entry reports Python/NumPy scenario calculations and a five-node thermal model, followed by virtual sensitivity and numerical-refinement work. The two CSV datasets contain 200,080 scenario/model rows, not specimens, replicates or measurements.

**Findings:** Thermal energy closure and timestep comparisons check numerical behavior only. The model omits blade movement, delamination/fracture quality, EVA chemistry and emissions. Stage 4 rows model assumed particle-size distributions and literature-normalized arithmetic; they do not model eddy-current separation or Ag recovery.

**Decision / next action:** Keep all outputs labeled virtual. Replace assumptions only with traceable measurements and suitable assays before using them to predict a process.
