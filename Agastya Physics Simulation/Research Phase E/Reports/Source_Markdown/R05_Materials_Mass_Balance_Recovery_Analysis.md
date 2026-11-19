# Materials, Mass Balance and Recovery Analysis

**Report ID:** AG-R05  
**Version:** 1.0 | **Prepared:** 13 October 2026  
**Status:** Stream framework and source-specific reference arithmetic; no measured AGASTYA assay or recovery.

## 1. Purpose and boundary

This report defines how mass and Ag should be followed through current Stage 1 disassembly, Stage 2 liberation/classification, Stage 3 electrostatic separation, and Stage 4 sampling/assay/accounting. The boundary ends at a characterized Ag-bearing product or other measured stream. Stage 4 does not refine silver. Any downstream chemical or metallurgical route requires its own process boundary, material ledger, safety review and assay.

## 2. Feed composition and silver inventory

c-Si module construction commonly includes front glass, encapsulants, cells, conductive ribbons/solder, a backsheet, frame, junction box and cable. The exact bill of materials depends on module design, age, cell architecture, and manufacturer. Printed cell contacts and interconnect geometry also evolve. A review of technology-specific consumption estimates reports 2020 cell-level and module-level values differing substantially among PERC, TOPCon and SHJ designs ([Hallam et al., 2023](https://doi.org/10.1002/pip.3661)). Those are manufacturing-use estimates, not measured Ag concentration in a specific aged panel, and they do not give recoverable Ag after service and processing.

Phase D records three isolated reference bases:

| Source basis | Normalized 1 kg Ag inventory | Evidence meaning |
|---|---:|---|
| Review-derived 300 ppm | 0.300 g | Denominator/source provenance unresolved |
| Dias et al. study-specific 600 g/t | 0.600 g | Specific study feed; not AGASTYA assay |
| Secondary 630 g/t wording | 0.630 g | Relationship to 600 g/t unresolved |

They must not be combined into a statistical interval or used as a single “typical panel” grade. Actual recoverable inventory requires representative sampling of the identified feed and a matrix-valid assay.

## 3. Stream ledger

{{FIGURE:massflow}}

| Process point | Required stream records | Ag accounting requirement |
|---|---|---|
| Feed | Parent ID, manufacturer/model/year if known, technology, mass, condition, sample split | Baseline Ag assay with preparation/QA/QC and uncertainty |
| Stage 1 | Frame, box/cables, glass, cell-bearing laminate, debris, dust and unexplained loss | Assay all streams if Ag partition is claimed; otherwise report partition as unknown |
| Stage 2 | Each size class, each collected residue, dust and equipment cleanout | Measure mass by class and assay representative splits; size is not liberation |
| Stage 3 | Concentrate, middlings, rejects, dust/filter, equipment residue | Weigh and assay every output; include replicate run IDs |
| Stage 4 | Sample IDs, aliquot masses, assay results, blanks, duplicates, standards/spikes and reporting limits | Calculate grade, recovery, enrichment and uncertainty separately |

## 4. Balance equations and uncertainty

For a stream of total mass `M_i` and Ag mass fraction `x_i`, its Ag inventory is `A_i = M_i x_i`. A stage's total mass closure residual is `r_M = M_feed − Σ_i M_i − M_documented loss`; its Ag residual is `r_A = A_feed − Σ_i A_i − A_documented loss`. Recovery, grade and yield are:

`R_Ag = A_product/A_feed`  
`G_Ag = A_product/M_product`  
`Y_mass = M_product/M_feed`.

If input quantities are measured with uncertainty, first-order propagation can be used for planning. For independent feed/product mass and grade terms, `u_R/R ≈ sqrt[(u_Mp/Mp)^2+(u_xp/xp)^2+(u_Mf/Mf)^2+(u_xf/xf)^2]`. Covariance from shared sampling or laboratory calibration requires covariance terms. With no replicate feed data or analytical uncertainty, no numeric interval is justified.

## 5. Current computed balances

There is no actual integrated balance. The historical virtual datasets contain scenario mass partitions and calculations, not weighed outputs. Phase D's normalized one-kilogram arithmetic demonstrates unit conversions only. The current calculation kernel intentionally propagates unknown process inputs to null outputs. No recovery, grade, product purity, process loss, consumable use, or Ag closure is reported for AGASTYA.

The optional thermal model's contact energy per area is not a process energy balance. It omits actual heated area, tool and machine warm-up, drive energy, cycle utilization, exhaust treatment and panel variation. Energy requirements for the current electrostatic stage are also unknown because no hardware or power measurements were provided.

## 6. Critical measurement gaps and priority

The most consequential missing measurement is a representative, traceable feed lot with baseline Ag assay. The next are calibrated Stage 1/2 mass partitions, dust capture and size-class assays, and a defined Stage 3 separator with all bins weighed and assayed. A small reported Ag fraction can be dominated by sample heterogeneity or missed fines; therefore sample lineage and QA/QC are part of the material balance, not administrative extras.

IEA PVPS's hot-knife LCA used 2018 pilot data for a defined delamination functional unit and recommended more primary information on laminate and metal-recovery operations. Its boundary cannot provide AGASTYA's Ag recovery or complete end-of-life energy account ([Frischknecht et al., 2023](https://iea-pvps.org/wp-content/uploads/2023/07/Report_IEA-PVPS_T12-25-2023_LCA-PV-Recycling-Hot-Knife.pdf)).

## References

- Hallam, B. et al. (2023). [Silver learning curve for photovoltaics](https://doi.org/10.1002/pip.3661).
- Frischknecht, R., Komoto, K. & Doi, T. (2023). [IEA PVPS hot-knife LCA](https://iea-pvps.org/wp-content/uploads/2023/07/Report_IEA-PVPS_T12-25-2023_LCA-PV-Recycling-Hot-Knife.pdf).
- AGASTYA Phase D `Integrated_Process_Model/results/normalized_inventory_results.json` and `Four_Stage_Process_Model.md`.
