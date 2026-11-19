# AGASTYA software inventory and execution scope

## Tools actually used

| Program/library | Use recorded in this workspace | What it does not establish |
|---|---|---|
| CPython 3.14.4 | Evidence CSV generation, deterministic scenario arithmetic, accounting tests and validation | No physical measurement by itself |
| Python standard library | CSV/JSON processing, balances, checks and manifests | No multiphysics solve |
| NumPy 2.5.3 | Earlier thermal-model/sensitivity workflow | A numerical output is not experimental validation |
| PowerShell 7.6.5 | File orchestration and command launch | Not a physics engine |
| Node.js 24.19.0 + PptxGenJS | Generate current PowerPoint decks | Not a research or simulation engine |
| python-pptx 1.0.2 | Structural/text inspection of PPTX files | Does not prove slide appearance in PowerPoint |
| ReportLab 4.4.9 | Generate A1/A4 poster PDFs | Export success does not prove event compliance |
| pypdf 6.10.0 | Verify PDF page count, page boxes and extract claim text | Does not detect all visual/layout defects by itself |
| Poppler (`pdfinfo`, `pdftoppm`) | Check page sizes and render poster PDFs for visual preview | Does not determine print-policy compliance |

## Models and run records

The legacy simulation records contain **200,080 virtual rows**: scenario calculations and time histories, including a five-node lumped thermal resistance/capacitance model integrated by explicit forward Euler and assumed particle-size/screen-cut scenarios. The model outputs carry assumed inputs and run metadata. They are not physical observations, random sample replicates or measured performance.

The Phase B/C scripts produce literature-normalized inventory arithmetic, sensitivity rows, source extraction and accounting checks. No process recovery is imputed. See [data and analysis guide](../03_Data_and_Analysis/DATA_AND_ANALYSIS_GUIDE.md).

## Not run

No Ansys Maxwell, Rocky, COMSOL, MOOSE, FEM, DEM, CFD, electrostatic field/particle solver, process chemistry engine, leaching simulator, assay instrument or lab method was run. No paid application, remote service or connected facility was used. Browser demos and EYE vision software are not silver-recovery physics engines.

## Software-access status

The bundled runtime paths are local to the current Windows account and may not exist on another computer. Do not install replacements just to reproduce the current arithmetic: use the installed Python/Node runtime and record `python --version` or `node --version`. A physics solver should only be selected after its input data, validation target, license/access and study question are defined.
