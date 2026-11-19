# AGASTYA Phase E — report collection index

**Collection ID:** AG-PE-REPORTS  
**Version:** 1.0 | **Prepared:** 13 October 2026  
**Project boundary:** c-Si module material recovery research; no AGASTYA physical recovery result has been established.

> **Historical snapshot:** This collection was prepared 13 October 2026. Its stage map was corrected by the project owner on 16 October. Current architecture is in the root `AGASTYA_ARCHITECTURE.md`; historical labels in these reports do not control current design.

## Reading order

| No. | Report | Purpose | PDF |
|---|---|---|---|
| 01 | AGASTYA Technical Research Dossier | Integrated project status, four-stage architecture, evidence boundary, principal findings and decisions | `01_AGASTYA_Technical_Research_Dossier.pdf` |
| 02 | Thermal Physics and Chemical Transformations | Optional hot-knife pretreatment model, sensitivity, mesh/timestep checks, chemistry limits | `02_Thermal_Physics_and_Chemical_Transformations.pdf` |
| 03 | Stage 4 Mechanism and Process Analysis | Representative sampling, assay, stream accounting and failure modes | `03_Stage4_Mechanism_and_Process_Analysis.pdf` |
| 04 | Computational Modeling and Simulation Atlas | Historical and new simulation methods, results, numerical checks and reproduction | `04_Computational_Modeling_and_Simulation_Atlas.pdf` |
| 05 | Materials, Mass Balance and Recovery Analysis | Feed composition, silver inventory, stream tracking and recovery equations | `05_Materials_Mass_Balance_and_Recovery_Analysis.pdf` |
| 06 | Engineering Feasibility and Next Research Priorities | Evidence-based readiness, advancement gates and highest-value work | `06_Engineering_Feasibility_and_Next_Research_Priorities.pdf` |
| 07 | Research Progress and Development Record | Chronological separation of prior work and Phase E updates | `07_Research_Progress_and_Development_Record.pdf` |

The supplementary [Appendix A PDF](PDFs/08_Appendix_Thermal_Model_Inputs.pdf) contains inherited thermal properties, boundary inputs, equations, selected scenarios and numerical-check notes. [Appendix B PDF](PDFs/09_Appendix_Main_Effect_Results.pdf) presents the full factor-by-response sensitivity results in print form. Full-precision factor effects are retained in the [CSV](Appendices/Appendix_B_Full_Main_Effects.csv) and source JSON; row-level simulation outputs remain under `Simulation_Campaign/processed/`.

## Evidence and print notes

The PDF collection is formatted for A4 portrait printing with a consistent visual system, document identifiers, dates, page headers/footers, tables of contents and traceable references. Reports are companion records, not seven independent proof claims. A claim labeled as literature-derived, scenario-calculated or simulated retains that evidence type in the text.

The historical virtual dataset contains 200,080 scenario/time-history records. It does not contain physical AGASTYA samples. No assay, separator performance, product purity, process recovery, throughput, energy demand, economic feasibility or environmental benefit has been validated for AGASTYA.

## Appendices and reproducibility

See [appendix index](Appendices/Appendix_README.md) for the inherited thermal parameters, full factor effects, spatial/timestep data, environment summary and preserved failed explicit run. Report sources are in `Source_Markdown/`; report generation is reproducible with `render_reports.py`.

Editable sources are in `Source_Markdown/`. Figures and report-generation code are under `../Simulation_Campaign/` and `render_reports.py`. The PDFs should be reviewed in the target print workflow before physical printing or presentation.
