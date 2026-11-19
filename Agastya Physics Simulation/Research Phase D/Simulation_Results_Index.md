# Simulation and calculation results index

| Record | Type | Scope/status | Use and limitation |
|---|---|---|---|
| `Integrated_Process_Model/results/normalized_inventory_results.json` | Phase D executed Python output | Three source-normalized 1 kg Ag inventory cases; measured AGASTYA outputs are null | Reproducible unit arithmetic only; no process efficiency applied |
| `Integrated_Process_Model/agastya_accounting.py --self-check` | Phase D synthetic software check | Formula fixture: mass yield, grade, recovery, and balances | Software verification only; fixture values are not AGASTYA data |
| [Published-data arithmetic v3](../Research%20Phase%20B-C/published_data_validation_v3.csv) | Existing source-qualified arithmetic | Literature/reference calculations | Preserve source basis; not physical outputs |
| [Scenario results v3](../Research%20Phase%20B-C/scenario_results_v3.csv) | Existing normalized reference rows | Literature scenarios | Not a statistical model or project trial |
| [Sensitivity analysis v2](../Research%20Phase%20B-C/sensitivity_analysis_v2.csv) | Existing parameter sensitivity output | Prior assumptions/scenarios | Reuse only with its original model scope and assumptions |
| [Route comparison v2](../Research%20Phase%20B-C/separation_route_comparison_v2.csv) | Existing route comparison | Literature and qualitative route analysis | Not a measured AGASTYA comparison |
| [Phase B accounting run](../Research%20Baseline/phase_b_accounting_run.json) | Existing accounting run | Stage 4 equation/software demonstration | No physical streams or assay values |
| [Legacy physics simulation summary](../Agastya_Physics_Simulation_2026-10-10.md) and associated datasets | Legacy virtual model/time-history outputs; project reports 200,080 rows | Assumption-driven five-node thermal RC and virtual scenarios | Different unit operation and legacy labels; not physical specimens or current Stage 3 outputs |
| [Legacy thermal workbook](../../Build%20Files%20and%20Steps/Stage%203/stage3_thermal_data.xlsx) | Legacy workbook | Assumed EVA heat/throughput calculation; trial log blank | Optional thermal pretreatment assumptions only; no measured energy or throughput |

## Current-stage result status

| Current stage | Numerical physical result available? | What is available |
|---|---|---|
| 1 — disassembly/routing | No | Data schema, audit, and mass-balance equations |
| 2 — liberation/classification | No | Literature context and blank fraction template |
| 3 — electrostatic candidate | No | Governing equation architecture and blank inputs template |
| 4 — sampling/assay/accounting | No | Formula implementation and blank stream template |

There is no AGASTYA recovery, concentrate grade, metal purity, mass throughput, energy consumption, life-cycle impact, or economic result in this index. Literature values remain attributed and separate.
