# AGASTYA multidisciplinary engineering research — Phase D

**Prepared:** 13 October 2026  
**Project:** AGASTYA, end-of-life crystalline-silicon photovoltaic material recovery  
**Evidence class:** workspace audit, literature synthesis, and normalized arithmetic. No physical process or external multiphysics solver was run.

## Executive summary

This phase audited the actual workspace, reconciled current and legacy stage numbering, updated the direct literature review, assessed available simulation software, and implemented a small reproducible accounting model. The authoritative current process map is: **(1) disassembly and component routing, (2) mechanical liberation and classification, (3) candidate electrostatic separation, and (4) representative sampling, assay, and accounting**. Optional thermal delamination is a legacy pretreatment between Stages 1 and 2. Stage 4 is not a silver refining operation.

The literature supports investigating electrostatic separation on characterized crystalline-silicon PV material. A 2019 needle-roll study reports a 94.37% “silver separation efficiency” at its selected settings, but the accessible abstract does not define that metric or provide the full mass balance. A 2023 study reports Ag, Al, and Si co-concentration at 38 kV and 75 rpm; it does not provide a mass-weighted Ag recovery in the accessible abstract. These are study-specific results, not AGASTYA predictions. Mechanical size fractionation studies likewise show Ag partitioning into fine fractions on their own feedstocks, not a universal grade or recovery.

There is no verified AGASTYA panel/coupon/powder lot, measured stream, separator geometry, assay, lab record, or trial. Therefore no defensible numerical prediction can yet be made for Ag recovery, concentrate grade, purity, throughput, energy, environmental benefit, or economics. Unknowns remain blank in the templates and machine-readable output. Normalized literature arithmetic is provided only to illustrate source bases, not to set feed grade.

## Findings from the workspace audit

- The 53,861-row inventory records paths and file metadata before the Phase D folder was populated; it does not claim semantic review of every file. The previous inventory summary was two files lower.
- The current baseline and crosswalk control stage meanings. Older thesis, thermal, and simulation artifacts retain their historical labels; they are not silently remapped or treated as current results.
- The historical 200,080 rows are virtual scenario/time-history output. A five-node explicit-Euler thermal RC model and its workbook describe an assumed optional thermal pretreatment. Neither represents current Stage 3 electrostatic separation or a measured trial.
- The thermal workbook calculates 49.23 panels/day under stated area, energy, solar-hours, and efficiency assumptions; its Trial Log is empty. The calculation is not measured energy or throughput.
- The EYE project is an inspection/record interface. Its image data and model outputs are not Ag assays or separator data.
- The thesis and abstract contain historical claims (including 20 g Ag/module, 90% recovery, $38 value, and thermal throughput) that are not verified by current measurements. They should not be used as current project results.
- Existing Phase B/C arithmetic and software checks remain useful for their specified formulas. The v2 accounting checks passed 28/28; the preserved legacy kernel audit passed 22/25 with three known input-guard gaps. Neither validates the process.

## Process reconstruction and model readiness

| Stage | Current definition | What can be modeled now | Critical evidence gap |
|---|---|---|---|
| 1 | Disassembly and component routing | Data schema and mass/lineage accounting | Identified module, measured component masses, loss capture, and Ag partition |
| 2 | Mechanical liberation and classification | PSD/size-fraction accounting once measured | Actual feed and settings, PSD, liberation/association, dust/losses, and assays |
| 3 | Electrostatic separation candidate | Governing equation architecture and literature comparison | Dimensioned separator, particle/charge distributions, operating conditions, mass and assay data |
| 4 | Representative sampling, assay, and accounting | Equations and fail-closed software implementation | Representative physical streams, validated assays, QA/QC, and uncertainties |

Stage 3 equations and required inputs are documented in `Stage_3_Model/README.md`. They are a model specification, not a numerical field/trajectory solution. `Integrated_Process_Model/agastya_accounting.py` runs only normalized source arithmetic by default; measured AGASTYA mass balance fields are null. A synthetic fixture is used only for formula self-checking and is not project data.

## Silver basis and composition

The 300 ppm value is retained as a review-derived scenario with unresolved source denominator. Dias et al. (2016) publisher abstract reports 600 g/t for its particular feed; a secondary source's 630 g/t wording remains unresolved. For a normalized 1 kg basis only, these correspond to 0.300 g, 0.600 g, and 0.630 g Ag, respectively. They are neither a pooled interval nor an AGASTYA feed assay. No recovery percentage is applied to them.

## Tool disposition

Python's standard library is sufficient for traceable stream accounting; NumPy/pandas/openpyxl are available in the workspace. No OpenFOAM, Cantera, DWSIM, gmsh, or external solver command was found. SimScale, COMSOL, and Ansys access was not authenticated. Recommended next step is measurement-first: use an instrumented benchtop trial and validated assay, then select a solver only if the measured data expose a decision that a model can answer. A particle-trajectory model could later use COMSOL Particle Tracing or a custom field/trajectory coupling; electrostatic charging/contact behavior and model validation remain substantial work.

## Validation and uncertainty

Validation performed in this phase is limited to source/record traceability, arithmetic reproducibility, code-path self-checking with clearly synthetic data, and review of the existing project checks. There is no process validation. The uncertainty report separates source-basis uncertainty, measurement uncertainty, sample heterogeneity, process variability, and model-form uncertainty. Because the physical process inputs are missing, assigning Monte Carlo distributions or reporting probabilistic recovery would create false precision.

## Decisions and next work

1. Preserve the current charter and legacy crosswalk; do not relabel earlier files.
2. Define a representative c-Si feed lot and chain of custody before cutting or comminution.
3. Weigh and characterize every Stage 1 and Stage 2 stream; retain representative splits.
4. Confirm assay method, digestion/sample preparation, QA/QC, reporting limits, and lab scope for the PV matrix.
5. Obtain dimensioned electrostatic separator design and particle-specific properties before choosing simulation software.
6. Run a controlled, replicated Stage 3 trial only after safety review; weigh and assay every output stream.
7. Reconcile mass and Ag closures with uncertainty. Do not claim product purity or refining until an independent downstream route demonstrates it.

See [research gaps](Research_Gap_Register.csv), [next research plan](Next_Research_Plan.md), and [validation report](Validation_Report.md) for acceptance criteria and dependencies.

## Reproduction

Use Python 3.10+ (only standard-library modules are required):

```powershell
python .\Integrated_Process_Model\agastya_accounting.py --input .\Integrated_Process_Model\inputs\reference_inventory.json --output .\Integrated_Process_Model\results\normalized_inventory_results.json
python .\Integrated_Process_Model\agastya_accounting.py --self-check
```

The file inventory is a pre-write snapshot; rerunning the commands changes the output JSON but does not refresh that snapshot. No Git repository was present at `D:\Agastya`.
