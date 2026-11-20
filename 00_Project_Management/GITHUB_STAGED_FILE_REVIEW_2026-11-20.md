# GitHub staged-file review â€” 20 November 2026

## Repository and gate

- Local branch: `main`; remote name: `origin`; URL: `https://github.com/icantchooseaname225/agastya-photovoltaic-recovery.git`.
- Remote checkpoint: public repository; the initial reviewed tree was published on `main` by a regular push. See the repository-preparation record for the first verified revision.
- The current reviewed source tree is consolidated on local `main`; any follow-up changes should use regular non-force pushes.
- This manifest reflects the current tracked source tree after the initial sync; it records exact paths and working-tree sizes for review.

## Reviewed project set summary

- Reviewed tracked-file count, including this manifest: **425**.
- Aggregate working-tree file bytes, including this review: **2,945,479 bytes**.
- Largest individual file: less than 10 MiB; this is the sum of individual file sizes, not the compressed Git object-store size.
- The manifest is included in the committed local project set. Its size is shown in the final table row.

## Privacy and content review

- Screened candidate text/code files for email-address patterns, owner-profile paths, credential assignments, GitHub token patterns, bearer tokens, and private-key headers. No email or credential matches remain in the candidate set; all owner-profile paths found in project-facing records were replaced by `%USERPROFILE%` or removed from reproduction commands.
- The `secrets.example.h` template contains only obvious placeholders (`YOUR_WIFI_PASSWORD`, `REPLACE_WITH_A_RANDOM_TOKEN...`) and a private-network example address. The actual `secrets.h` file is Git-ignored.
- Two phone-pattern matches were false positives: a tender URL identifier in a Day 29 source link and a prefix of a SHA-256 hash in the EYE dataset source record.
- Excluded by `.gitignore`: private correspondence and the six enquiry drafts; outreach contact/tracker files and the public-contact lead CSV; raw image corpora, dataset group manifest, archives and model weights; local path inventories; generated QA contact sheets and inspection exports; the IRIS/submission and NCSC final packages; archive snapshots; presentation/printable binaries; and unreviewed PDF/Word/PowerPoint/Excel files.
- Third-party original photographs are excluded. The tracked project set keeps the asset register/credits and editable vector source files.

## Complete tracked path and size list

| Path | Bytes |
|---|---:|
| `.gitignore` | 2,894 |
| `00_Project_Management/build_workspace_registers.py` | 43,947 |
| `00_Project_Management/CHANGELOG.md` | 177 |
| `00_Project_Management/DECISION_LOG.md` | 186 |
| `00_Project_Management/DECISIONS_LOG.md` | 3,919 |
| `00_Project_Management/DUPLICATE_AND_CLEANUP_REPORT.md` | 3,964 |
| `00_Project_Management/FILE_CATALOG.csv` | 50,499 |
| `00_Project_Management/file_inventory_summary.md` | 1,673 |
| `00_Project_Management/FILE_MIGRATION_LOG.csv` | 23,925 |
| `00_Project_Management/FINAL_CONSISTENCY_AUDIT_2026-10-11.md` | 8,831 |
| `00_Project_Management/generate_file_inventory.py` | 2,145 |
| `00_Project_Management/GITHUB_REPOSITORY_PREPARATION_2026-11-19.md` | 5,867 |
| `00_Project_Management/GITHUB_STAGED_FILE_REVIEW_2026-11-19.md` | 31,555 |
| `00_Project_Management/link_check_results.csv` | 44,652 |
| `00_Project_Management/MASTER_TASK_LIST.md` | 11,344 |
| `00_Project_Management/MIGRATION_PLAN_2026-10-11.md` | 3,273 |
| `00_Project_Management/MILESTONES.md` | 299 |
| `00_Project_Management/OPEN_QUESTIONS.md` | 4,503 |
| `00_Project_Management/PROJECT_STATUS.md` | 181 |
| `00_Project_Management/PROJECT_UNDERSTANDING_AUDIT.md` | 7,111 |
| `00_Project_Management/README.md` | 655 |
| `00_Project_Management/REPAIR_LOG.md` | 8,252 |
| `00_Project_Management/TASK_TRACKER.csv` | 340 |
| `00_Project_Management/TOOLS_AND_SOFTWARE_AUDIT.md` | 5,625 |
| `00_Project_Management/validate_links.py` | 1,485 |
| `01_Research/03_Source_Evidence/SOURCE_EVIDENCE_REGISTER.csv` | 29,811 |
| `01_Research/Evidence_Database/README.md` | 312 |
| `01_Research/INDIA_SOLAR_PV_MARKET_REGULATORY_SNAPSHOT_2026-11-19.md` | 5,644 |
| `01_Research/Institutional_Collaboration/INSTITUTIONAL_VALIDATION_PROGRAMME_2026-11-19.md` | 5,319 |
| `01_Research/Institutional_Collaboration/RETIRED_CSI_PANEL_CHARACTERIZATION_AND_CHAIN_OF_CUSTODY_PLAN_2026-11-19.md` | 5,810 |
| `01_Research/Literature_Review/AGASTYA_EVIDENCE_REVIEW_2026-10-11.md` | 788 |
| `01_Research/Material_Composition/README.md` | 432 |
| `01_Research/Published_Experiments/README.md` | 260 |
| `01_Research/RESEARCH_OVERVIEW.md` | 9,323 |
| `01_Research/Scientific_References/README.md` | 191 |
| `01_Research/Separation_Methods/README.md` | 307 |
| `01_Research/Stage_4_Flotation_Reagent_Investigation/AGASTYA_FROTH_FLOTATION_REAGENT_FEASIBILITY_REPORT.md` | 10,949 |
| `02_Engineering/ENGINEERING_OVERVIEW.md` | 4,333 |
| `02_Engineering/README.md` | 458 |
| `02_Engineering/Stage_2_Robotic_Disassembly/generate_workcell_plan_dxf.py` | 4,187 |
| `02_Engineering/Stage_2_Robotic_Disassembly/README.md` | 819 |
| `02_Engineering/Stage_2_Robotic_Disassembly/robot_workcell_reach_model.py` | 13,245 |
| `02_Engineering/Stage_2_Robotic_Disassembly/simulation_outputs/concept_workcell_plan.dxf` | 6,497 |
| `02_Engineering/Stage_2_Robotic_Disassembly/simulation_outputs/concept_workcell_plan_notes.md` | 1,061 |
| `02_Engineering/Stage_2_Robotic_Disassembly/simulation_outputs/model_report.md` | 2,931 |
| `02_Engineering/Stage_2_Robotic_Disassembly/simulation_outputs/perimeter_task_points.csv` | 5,234 |
| `02_Engineering/Stage_2_Robotic_Disassembly/simulation_outputs/reach_envelope.svg` | 9,687 |
| `02_Engineering/Stage_2_Robotic_Disassembly/simulation_outputs/reach_screen_summary.json` | 2,811 |
| `02_Engineering/Stage_2_Robotic_Disassembly/STAGE2_ROBOTIC_DISASSEMBLY_FEASIBILITY_2026-11-19.md` | 7,900 |
| `03_Data_and_Analysis/DATA_AND_ANALYSIS_GUIDE.md` | 4,468 |
| `03_Data_and_Analysis/README.md` | 387 |
| `03_Data_and_Analysis/Sensitivity_Analysis/README.md` | 516 |
| `03_Data_and_Analysis/Stage4/outputs/ecs_flotation_break_even.svg` | 3,463 |
| `03_Data_and_Analysis/Stage4/outputs/ecs_flotation_break_even_grid.csv` | 8,619 |
| `03_Data_and_Analysis/Stage4/outputs/model_summary.json` | 2,475 |
| `03_Data_and_Analysis/Stage4/outputs/published_flotation_mass_balance.json` | 518 |
| `03_Data_and_Analysis/Stage4/README.md` | 1,705 |
| `03_Data_and_Analysis/Stage4/ROUTE_COMPARISON_MODEL_NOTE.md` | 2,202 |
| `03_Data_and_Analysis/Stage4/stage4_route_mass_balance_sensitivity.py` | 7,933 |
| `03_Data_and_Analysis/Validation/README.md` | 264 |
| `04_Logbook/Day_01_to_05/DAY_01_SHORT_ENTRY.md` | 728 |
| `04_Logbook/Day_01_to_05/DAY_02_SHORT_ENTRY.md` | 686 |
| `04_Logbook/Day_01_to_05/DAY_03_SHORT_ENTRY.md` | 1,027 |
| `04_Logbook/Day_01_to_05/DAY_04_SHORT_ENTRY.md` | 1,058 |
| `04_Logbook/Day_01_to_05/DAY_05_SHORT_ENTRY.md` | 1,201 |
| `04_Logbook/Logbook_Index.md` | 10,109 |
| `04_Logbook/Originals_Before_Concise_Edit_2026-10-13/PROJECT_LOGBOOK_DAY_24.md` | 3,786 |
| `04_Logbook/Originals_Before_Concise_Edit_2026-10-13/PROJECT_LOGBOOK_DAY_25.md` | 2,272 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_10.md` | 2,858 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_11.md` | 2,498 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_12.md` | 3,519 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_13.md` | 3,185 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_15.md` | 2,520 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_16.md` | 2,480 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_17.md` | 2,668 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_18.md` | 2,954 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_19.md` | 2,719 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_20.md` | 2,249 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_21.md` | 2,360 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_23.md` | 10,991 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_24.md` | 3,786 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_25.md` | 2,272 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_26.md` | 2,668 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_27.md` | 4,905 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_28.md` | 14,156 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_29.md` | 18,336 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_3_4.md` | 4,532 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_30.md` | 14,728 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_34.md` | 6,894 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_35.md` | 6,529 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_36.md` | 4,479 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_37.md` | 2,391 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_38.md` | 4,129 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_39.md` | 7,341 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_40.md` | 4,447 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_5_8.md` | 5,355 |
| `04_Logbook/PROJECT_LOGBOOK_DAY_9.md` | 2,434 |
| `04_Logbook/Short Versions/DAY_06.md` | 475 |
| `04_Logbook/Short Versions/DAY_07.md` | 454 |
| `04_Logbook/Short Versions/DAY_08.md` | 452 |
| `04_Logbook/Short Versions/DAY_09.md` | 457 |
| `04_Logbook/Short Versions/DAY_10.md` | 446 |
| `04_Logbook/Short Versions/DAY_11.md` | 465 |
| `04_Logbook/Short Versions/DAY_12.md` | 474 |
| `04_Logbook/Short Versions/DAY_13.md` | 392 |
| `04_Logbook/Short Versions/DAY_15.md` | 450 |
| `04_Logbook/Short Versions/DAY_16.md` | 421 |
| `04_Logbook/Short Versions/DAY_17.md` | 438 |
| `04_Logbook/Short Versions/DAY_18.md` | 484 |
| `04_Logbook/Short Versions/DAY_19.md` | 478 |
| `04_Logbook/Short Versions/DAY_20.md` | 470 |
| `04_Logbook/Short Versions/DAY_21.md` | 1,214 |
| `04_Logbook/Short Versions/DAY_22.md` | 803 |
| `04_Logbook/Short Versions/DAY_23.md` | 1,201 |
| `04_Logbook/Short Versions/DAY_24_SHORT_ENTRY.md` | 1,258 |
| `04_Logbook/Short Versions/DAY_25_SHORT_ENTRY.md` | 1,372 |
| `04_Logbook/Short Versions/DAY_26_SHORT_ENTRY.md` | 1,188 |
| `04_Logbook/Short Versions/DAY_27_SHORT_ENTRY.md` | 1,205 |
| `04_Logbook/Short Versions/DAY_28_SHORT_ENTRY.md` | 1,931 |
| `04_Logbook/Short Versions/DAY_29_SHORT_ENTRY.md` | 2,398 |
| `04_Logbook/Short Versions/DAY_30_SHORT_ENTRY.md` | 1,608 |
| `04_Logbook/Short Versions/DAY_34_SHORT_ENTRY.md` | 1,991 |
| `04_Logbook/Short Versions/DAY_35_SHORT_ENTRY.md` | 2,158 |
| `04_Logbook/Short Versions/DAY_36_SHORT_ENTRY.md` | 1,811 |
| `04_Logbook/Short Versions/DAY_37_SHORT_ENTRY.md` | 1,240 |
| `04_Logbook/Short Versions/DAY_38_SHORT_ENTRY.md` | 1,470 |
| `04_Logbook/Short Versions/DAY_39_SHORT_ENTRY.md` | 2,014 |
| `04_Logbook/Short Versions/DAY_40_SHORT_ENTRY.md` | 2,226 |
| `04_Logbook/Short Versions/DAY31-32-33 COMBINED.txt` | 8,952 |
| `04_Logbook/Short Versions/README.md` | 1,737 |
| `05_Presentation/Final_Presentation/AGASTYA_SLIDE_EVIDENCE_REGISTER.csv` | 8,560 |
| `05_Presentation/Final_Presentation/AGASTYA_SLIDE_EVIDENCE_REGISTER_2026-10-20.csv` | 11,040 |
| `05_Presentation/Final_Presentation/AGASTYA_VISUAL_ASSET_REGISTER.csv` | 5,588 |
| `05_Presentation/Final_Presentation/AGASTYA_VISUAL_ASSET_REGISTER_2026-10-20.csv` | 5,307 |
| `05_Presentation/Final_Presentation/README.md` | 1,516 |
| `05_Presentation/PRESENTATION_GUIDE.md` | 2,792 |
| `05_Presentation/Presentation_Script/AGASTYA_PRESENTATION_SPEAKER_NOTES.md` | 8,216 |
| `05_Presentation/Presentation_Script/AGASTYA_PRESENTATION_SPEAKER_NOTES_2026-10-20.md` | 12,364 |
| `05_Presentation/Presentation_Script/README.md` | 329 |
| `05_Presentation/Working_Drafts/build_agastya_presentations.js` | 36,609 |
| `05_Presentation/Working_Drafts/Build_Utilities/.build_agastya_enhanced.js` | 48,500 |
| `05_Presentation/Working_Drafts/Build_Utilities/.inspect_agastya_temp.py` | 1,878 |
| `05_Presentation/Working_Drafts/Build_Utilities/.render_agastya_temp.ps1` | 628 |
| `05_Presentation/Working_Drafts/README.md` | 387 |
| `06_NCSC_Display/DISPLAY_IDEAS_AND_DEMONSTRATIONS.md` | 300 |
| `06_NCSC_Display/NCSC_PREPARATION_GUIDE.md` | 9,255 |
| `06_NCSC_Display/Official_Requirements/NCSC_COMPLIANCE_CHECKLIST.md` | 2,900 |
| `06_NCSC_Display/Posters/build_printables.js` | 34,005 |
| `06_NCSC_Display/Posters/poster_generator.py` | 15,467 |
| `06_NCSC_Display/Posters/README.md` | 328 |
| `06_NCSC_Display/Presentation_QA/AGASTYA_JUDGE_QUESTIONS.md` | 5,853 |
| `06_NCSC_Display/PRINT_AND_BUILD_REGISTER.csv` | 8,615 |
| `06_NCSC_Display/PRINTED_MATERIALS_AND_DISPLAY_PLAN.md` | 313 |
| `06_NCSC_Display/validate_print_outputs.js` | 3,061 |
| `06_NCSC_Display/validate_print_outputs.py` | 2,655 |
| `07_Visual_Assets/ASSET_CATALOGUE.md` | 1,872 |
| `07_Visual_Assets/Asset_Licences_and_Credits/README.md` | 333 |
| `07_Visual_Assets/Conceptual_Illustrations/Agastya_3D_Cardboard_Model.svg` | 9,121 |
| `07_Visual_Assets/Conceptual_Illustrations/Agastya_Cardboard_Prototype_3D.svg` | 12,683 |
| `07_Visual_Assets/Conceptual_Illustrations/Agastya_Concept_Model_Diagram.svg` | 11,280 |
| `07_Visual_Assets/Conceptual_Illustrations/Agastya_Cutaway_3D_Concept.svg` | 15,188 |
| `07_Visual_Assets/Conceptual_Illustrations/Agastya_Structural_Model_Diagram.svg` | 10,245 |
| `07_Visual_Assets/Conceptual_Illustrations/Agastya_Structure_Simple_Guide.svg` | 9,357 |
| `07_Visual_Assets/Original_Photographs/README.md` | 256 |
| `07_Visual_Assets/Research_Figures/README.md` | 198 |
| `07_Visual_Assets/VISUAL_ASSET_REGISTER.csv` | 878 |
| `09_Software_and_Environment/ENVIRONMENT_INVESTIGATION_2026-10-26.md` | 3,220 |
| `09_Software_and_Environment/ENVIRONMENT_SETUP.md` | 1,262 |
| `09_Software_and_Environment/FINAL_QA_REPORT_2026-10-26.md` | 3,489 |
| `09_Software_and_Environment/PROGRAMS_USED_AND_SIMULATION_SCOPE.md` | 2,157 |
| `09_Software_and_Environment/README.md` | 463 |
| `09_Software_and_Environment/REPRODUCIBILITY_GUIDE.md` | 1,918 |
| `09_Software_and_Environment/SOFTWARE_INVENTORY.md` | 2,648 |
| `09_Software_and_Environment/SOFTWARE_REPAIR_REPORT_2026-10-26.md` | 3,623 |
| `Agastya Physics Simulation/Agastya_Physics_Simulation_2026-10-10.md` | 11,889 |
| `Agastya Physics Simulation/Agastya_Physics_Simulation_2026-10-10.py` | 41,055 |
| `Agastya Physics Simulation/Agastya_Physics_Simulation_2026-10-10_metadata.json` | 1,826 |
| `Agastya Physics Simulation/build_dataset_docs.py` | 27,532 |
| `Agastya Physics Simulation/data_dictionary.csv` | 30,084 |
| `Agastya Physics Simulation/dataset_checks_and_summary.json` | 2,604 |
| `Agastya Physics Simulation/experiment_register.csv` | 12,352 |
| `Agastya Physics Simulation/followup_virtual_experiments.py` | 20,226 |
| `Agastya Physics Simulation/followup_virtual_experiments_metadata.json` | 1,489 |
| `Agastya Physics Simulation/followup_virtual_experiments_summary.json` | 1,489 |
| `Agastya Physics Simulation/PROCEDURES_AND_RESULTS.md` | 16,742 |
| `Agastya Physics Simulation/README.md` | 3,618 |
| `Agastya Physics Simulation/Research Baseline/agastya_four_stage_process_flow.svg` | 6,037 |
| `Agastya Physics Simulation/Research Baseline/AGASTYA_PHASE_A_BASELINE_2026-10-10.md` | 32,288 |
| `Agastya Physics Simulation/Research Baseline/ARCHITECTURE_CROSSWALK_2026-10-10.md` | 1,181 |
| `Agastya Physics Simulation/Research Baseline/missing_specifications.csv` | 5,071 |
| `Agastya Physics Simulation/Research Baseline/PHASE_B_ACCOUNTING_MODEL.md` | 3,453 |
| `Agastya Physics Simulation/Research Baseline/phase_b_accounting_run.json` | 1,072 |
| `Agastya Physics Simulation/Research Baseline/preliminary_material_inventory.csv` | 4,675 |
| `Agastya Physics Simulation/Research Baseline/README.md` | 2,033 |
| `Agastya Physics Simulation/Research Baseline/reference_inventory_arithmetic.csv` | 802 |
| `Agastya Physics Simulation/Research Baseline/software_access_matrix.csv` | 5,271 |
| `Agastya Physics Simulation/Research Baseline/source_evidence_register.csv` | 8,304 |
| `Agastya Physics Simulation/Research Baseline/stage_balance_input_template.csv` | 590 |
| `Agastya Physics Simulation/Research Baseline/stage4_accounting_kernel.py` | 4,941 |
| `Agastya Physics Simulation/Research Phase B-C/accounting_unit_tests_v2.py` | 4,406 |
| `Agastya Physics Simulation/Research Phase B-C/accounting_validation_report_v2.md` | 1,368 |
| `Agastya Physics Simulation/Research Phase B-C/accounting_validation_results_v2.csv` | 2,401 |
| `Agastya Physics Simulation/Research Phase B-C/AGASTYA_PHASE_BC_REPORT.md` | 2,649 |
| `Agastya Physics Simulation/Research Phase B-C/agastya_scenario_model_v2.py` | 10,866 |
| `Agastya Physics Simulation/Research Phase B-C/agastya_scenario_model_v3.py` | 5,010 |
| `Agastya Physics Simulation/Research Phase B-C/agastya_validation_plan_v2.md` | 1,697 |
| `Agastya Physics Simulation/Research Phase B-C/build_evidence_database_v2.py` | 62,725 |
| `Agastya Physics Simulation/Research Phase B-C/electrostatic_stage_feasibility_v2.md` | 1,513 |
| `Agastya Physics Simulation/Research Phase B-C/evidence_database_v2.csv` | 29,460 |
| `Agastya Physics Simulation/Research Phase B-C/NCSC_GUIDELINE_CHECKLIST_v2.md` | 1,820 |
| `Agastya Physics Simulation/Research Phase B-C/NCSC_RESEARCH_PROPOSAL_v2.md` | 2,979 |
| `Agastya Physics Simulation/Research Phase B-C/published_data_reproduction_v2.py` | 2,389 |
| `Agastya Physics Simulation/Research Phase B-C/published_data_reproduction_v3.py` | 3,424 |
| `Agastya Physics Simulation/Research Phase B-C/published_data_validation_v2.csv` | 1,540 |
| `Agastya Physics Simulation/Research Phase B-C/published_data_validation_v2.md` | 2,117 |
| `Agastya Physics Simulation/Research Phase B-C/published_data_validation_v3.csv` | 1,928 |
| `Agastya Physics Simulation/Research Phase B-C/README.md` | 1,224 |
| `Agastya Physics Simulation/Research Phase B-C/scenario_model_run_v2.json` | 504 |
| `Agastya Physics Simulation/Research Phase B-C/scenario_model_run_v3.json` | 1,067 |
| `Agastya Physics Simulation/Research Phase B-C/scenario_results_v2.csv` | 1,378 |
| `Agastya Physics Simulation/Research Phase B-C/scenario_results_v3.csv` | 2,019 |
| `Agastya Physics Simulation/Research Phase B-C/sensitivity_analysis_v2.csv` | 2,845 |
| `Agastya Physics Simulation/Research Phase B-C/sensitivity_analysis_v2.md` | 1,075 |
| `Agastya Physics Simulation/Research Phase B-C/separation_route_analysis_v2.md` | 2,573 |
| `Agastya Physics Simulation/Research Phase B-C/separation_route_comparison_v2.csv` | 4,833 |
| `Agastya Physics Simulation/Research Phase B-C/software_access_matrix_v2.csv` | 6,012 |
| `Agastya Physics Simulation/Research Phase B-C/software_execution_audit_v2.md` | 1,088 |
| `Agastya Physics Simulation/Research Phase B-C/validate_accounting_kernel_v2.py` | 11,457 |
| `Agastya Physics Simulation/Research Phase D/Evidence_Register.csv` | 13,509 |
| `Agastya Physics Simulation/Research Phase D/Four_Stage_Process_Model.md` | 7,644 |
| `Agastya Physics Simulation/Research Phase D/Integrated_Process_Model/agastya_accounting.py` | 8,497 |
| `Agastya Physics Simulation/Research Phase D/Integrated_Process_Model/inputs/reference_inventory.json` | 1,334 |
| `Agastya Physics Simulation/Research Phase D/Integrated_Process_Model/README.md` | 1,667 |
| `Agastya Physics Simulation/Research Phase D/Integrated_Process_Model/results/normalized_inventory_results.json` | 2,128 |
| `Agastya Physics Simulation/Research Phase D/Literature_Review.md` | 8,020 |
| `Agastya Physics Simulation/Research Phase D/Next_Research_Plan.md` | 3,881 |
| `Agastya Physics Simulation/Research Phase D/Project_File_Audit.md` | 8,579 |
| `Agastya Physics Simulation/Research Phase D/README.md` | 1,903 |
| `Agastya Physics Simulation/Research Phase D/Research_Gap_Register.csv` | 3,822 |
| `Agastya Physics Simulation/Research Phase D/Research_Log.md` | 2,128 |
| `Agastya Physics Simulation/Research Phase D/Research_Master_Report.md` | 8,023 |
| `Agastya Physics Simulation/Research Phase D/Sensitivity_and_Uncertainty_Report.md` | 4,851 |
| `Agastya Physics Simulation/Research Phase D/Simulation_Results_Index.md` | 2,890 |
| `Agastya Physics Simulation/Research Phase D/Simulation_Tool_Assessment.md` | 6,961 |
| `Agastya Physics Simulation/Research Phase D/Stage_1_Model/component_routing_template.csv` | 322 |
| `Agastya Physics Simulation/Research Phase D/Stage_1_Model/README.md` | 1,432 |
| `Agastya Physics Simulation/Research Phase D/Stage_2_Model/README.md` | 1,599 |
| `Agastya Physics Simulation/Research Phase D/Stage_2_Model/size_fraction_measurement_template.csv` | 293 |
| `Agastya Physics Simulation/Research Phase D/Stage_3_Model/electrostatic_model_inputs_template.csv` | 599 |
| `Agastya Physics Simulation/Research Phase D/Stage_3_Model/README.md` | 3,133 |
| `Agastya Physics Simulation/Research Phase D/Stage_4_Model/assay_stream_template.csv` | 402 |
| `Agastya Physics Simulation/Research Phase D/Stage_4_Model/README.md` | 2,125 |
| `Agastya Physics Simulation/Research Phase D/Validation_Report.md` | 3,723 |
| `Agastya Physics Simulation/Research Phase E/Logbook/README.md` | 575 |
| `Agastya Physics Simulation/Research Phase E/maintain_phase_e_records.py` | 32,454 |
| `Agastya Physics Simulation/Research Phase E/README.md` | 3,306 |
| `Agastya Physics Simulation/Research Phase E/Reports/Appendices/Appendix_B_Full_Main_Effects.csv` | 4,201 |
| `Agastya Physics Simulation/Research Phase E/Reports/Appendices/Appendix_Main_Effect_Results.md` | 4,158 |
| `Agastya Physics Simulation/Research Phase E/Reports/Appendices/Appendix_Model_Inputs.md` | 4,492 |
| `Agastya Physics Simulation/Research Phase E/Reports/Appendices/Appendix_README.md` | 1,146 |
| `Agastya Physics Simulation/Research Phase E/Reports/build_appendices.py` | 3,997 |
| `Agastya Physics Simulation/Research Phase E/Reports/PDF_QA_REPORT.csv` | 2,155 |
| `Agastya Physics Simulation/Research Phase E/Reports/README.md` | 832 |
| `Agastya Physics Simulation/Research Phase E/Reports/render_reports.py` | 30,577 |
| `Agastya Physics Simulation/Research Phase E/Reports/REPORT_INDEX.md` | 3,671 |
| `Agastya Physics Simulation/Research Phase E/Reports/Source_Markdown/R01_Technical_Research_Dossier.md` | 9,781 |
| `Agastya Physics Simulation/Research Phase E/Reports/Source_Markdown/R02_Thermal_Physics_Chemical_Transformations.md` | 9,315 |
| `Agastya Physics Simulation/Research Phase E/Reports/Source_Markdown/R03_Stage4_Mechanism_Process_Analysis.md` | 6,265 |
| `Agastya Physics Simulation/Research Phase E/Reports/Source_Markdown/R04_Computational_Modeling_Simulation_Atlas.md` | 7,922 |
| `Agastya Physics Simulation/Research Phase E/Reports/Source_Markdown/R05_Materials_Mass_Balance_Recovery_Analysis.md` | 5,913 |
| `Agastya Physics Simulation/Research Phase E/Reports/Source_Markdown/R06_Engineering_Feasibility_Next_Priorities.md` | 6,334 |
| `Agastya Physics Simulation/Research Phase E/Reports/Source_Markdown/R07_Research_Progress_Development_Record.md` | 4,768 |
| `Agastya Physics Simulation/Research Phase E/Research_Log.md` | 2,688 |
| `Agastya Physics Simulation/Research Phase E/Research_Progress_Register.csv` | 6,775 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Campaign/figures/diagrams/four_stage_process_map.svg` | 3,181 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Campaign/figures/diagrams/stage4_assay_workflow.svg` | 2,167 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Campaign/figures/diagrams/unquantified_material_flow.svg` | 2,559 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Campaign/models/inspect_legacy_csv.py` | 1,451 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Campaign/models/README.md` | 897 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Campaign/models/regenerate_phase_e_figures.py` | 585 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Campaign/models/run_phase_e_experiments.py` | 26,255 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Campaign/processed/PE-SIM-001_main_effect_variance.json` | 10,049 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Campaign/processed/PE-SIM-002_N1_coarse_model_verification.json` | 3,546 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Campaign/processed/PE-SIM-002_spatial_refinement.csv` | 5,527 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Campaign/processed/PE-SIM-003_timestep_refinement.csv` | 1,429 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Campaign/processed/phase_e_experiment_summary.json` | 8,787 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Campaign/raw/PE-SIM-002_failed_explicit_dt0p5ms.csv` | 4,149 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Campaign/raw/PE-SIM-002_failed_explicit_dt0p5ms_N1_comparison.json` | 3,326 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Campaign/raw/PE-SIM-002_failed_explicit_dt0p5ms_summary.json` | 7,713 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Campaign/README.md` | 959 |
| `Agastya Physics Simulation/Research Phase E/Simulation_Register.csv` | 6,564 |
| `Agastya Simulation/index.html` | 10,393 |
| `Agastya Simulation/machine.css` | 5,821 |
| `Agastya Simulation/machine.html` | 3,727 |
| `Agastya Simulation/machine.js` | 13,105 |
| `Agastya Simulation/README.md` | 2,322 |
| `Agastya Simulation/simulation.js` | 3,955 |
| `Agastya Simulation/styles.css` | 7,017 |
| `Agastya Simulation/Wokwi/diagram.json` | 1,496 |
| `Agastya Simulation/Wokwi/sketch.ino` | 2,890 |
| `Agastya Thermal/AgastyaThermalMonitor/AgastyaThermalMonitor.ino` | 9,615 |
| `Agastya Thermal/AgastyaThermalMonitor/README.md` | 4,304 |
| `Agastya Thermal/README.md` | 6,644 |
| `Agastya Thermal/stage3_eva_model_outputs/energy_summary.csv` | 607 |
| `Agastya Thermal/stage3_eva_model_outputs/model_summary.json` | 3,500 |
| `Agastya Thermal/stage3_eva_model_outputs/temperature_profiles.csv` | 17,982 |
| `Agastya Thermal/stage3_eva_model_outputs/temperature_profiles.svg` | 8,599 |
| `Agastya Thermal/stage3_eva_transient_1d.py` | 6,860 |
| `Agastya Thermal/STAGE3_EVA_TRANSIENT_MODEL_README.md` | 1,710 |
| `AGASTYA_ARCHITECTURE.md` | 8,111 |
| `AGASTYA_PROJECT_INDEX.md` | 6,203 |
| `Agastya-EYE/.gitignore` | 401 |
| `Agastya-EYE/app.py` | 55,731 |
| `Agastya-EYE/datasets/import_reports/github_solarpanel_inspection.json` | 14,740 |
| `Agastya-EYE/datasets/import_reports/raptormaps_thermal_v1.json` | 2,253 |
| `Agastya-EYE/datasets/licenses/RaptorMaps-MIT-LICENSE.txt` | 1,074 |
| `Agastya-EYE/datasets/source_manifest.csv` | 5,537 |
| `Agastya-EYE/datasets/SOURCES.md` | 16,497 |
| `Agastya-EYE/demos/servo_gate/agastya_eye_servo_gate_demo.ino` | 2,206 |
| `Agastya-EYE/demos/servo_gate/README.md` | 1,497 |
| `Agastya-EYE/docs/ARDUINO_SERVO_GATE.md` | 8,193 |
| `Agastya-EYE/docs/STAGE_INTEROP.md` | 7,928 |
| `Agastya-EYE/docs/STAGE_SOFTWARE_ROADMAP.md` | 7,547 |
| `Agastya-EYE/docs/STAGE1_READINESS.md` | 13,812 |
| `Agastya-EYE/docs/STAGE1_SORTER_BUILD.md` | 15,993 |
| `Agastya-EYE/docs/STAGE1_VALIDATION_RUN_2026-11-19.md` | 2,082 |
| `Agastya-EYE/docs/STAGE1_VALIDATION_RUN_2026-11-20.md` | 1,853 |
| `Agastya-EYE/docs/SYSTEM_REPAIR_AUDIT_2026-11-19.md` | 10,436 |
| `Agastya-EYE/docs/THERMAL_MODEL_CARD.md` | 5,621 |
| `Agastya-EYE/docs/VISIBLE_CROP_MODEL_CARD.md` | 3,279 |
| `Agastya-EYE/firmware/agastya_eye/agastya_eye.ino` | 12,304 |
| `Agastya-EYE/firmware/agastya_eye/secrets.example.h` | 333 |
| `Agastya-EYE/firmware/agastya_eye/sensor_adapter.h` | 1,759 |
| `Agastya-EYE/firmware/servo_gate/README.md` | 2,268 |
| `Agastya-EYE/firmware/servo_gate/servo_gate.ino` | 3,674 |
| `Agastya-EYE/hardware/__init__.py` | 55 |
| `Agastya-EYE/hardware/approval.py` | 17,753 |
| `Agastya-EYE/hardware/arduino_config.py` | 3,233 |
| `Agastya-EYE/hardware/arduino_controller.py` | 11,193 |
| `Agastya-EYE/inference/__init__.py` | 55 |
| `Agastya-EYE/inference/classifier.py` | 6,594 |
| `Agastya-EYE/inference/device.py` | 3,723 |
| `Agastya-EYE/inference/estimation.py` | 6,882 |
| `Agastya-EYE/inference/ledger.py` | 36,099 |
| `Agastya-EYE/inference/material_ledger.py` | 27,810 |
| `Agastya-EYE/inference/preprocessing.py` | 463 |
| `Agastya-EYE/inference/thermal_classifier.py` | 7,762 |
| `Agastya-EYE/inference/thermal_surface_classifier.py` | 290 |
| `Agastya-EYE/inference/triage.py` | 7,465 |
| `Agastya-EYE/inference/visible_crop_classifier.py` | 9,299 |
| `Agastya-EYE/models/pv_bw_power_loss_ridge_research.json` | 736 |
| `Agastya-EYE/models/pv_el_power_loss_ridge_research.json` | 736 |
| `Agastya-EYE/models/pv_hdr_power_loss_ridge_research.json` | 738 |
| `Agastya-EYE/models/solar_mobilenet_v2_baseline_2026-09-25.json` | 1,590 |
| `Agastya-EYE/models/solar_mobilenet_v2_candidate.json` | 1,695 |
| `Agastya-EYE/models/solar_rgb_surface_defects_mobilenet_v2.json` | 6,129 |
| `Agastya-EYE/README.md` | 35,389 |
| `Agastya-EYE/requirements.txt` | 73 |
| `Agastya-EYE/Start-EYE.bat` | 109 |
| `Agastya-EYE/Start-EYE.ps1` | 9,121 |
| `Agastya-EYE/Stop-EYE.ps1` | 2,036 |
| `Agastya-EYE/tests/__init__.py` | 0 |
| `Agastya-EYE/tests/test_arduino_controller.py` | 7,532 |
| `Agastya-EYE/tests/test_hardware_approval.py` | 8,426 |
| `Agastya-EYE/tests/test_inference_device.py` | 2,788 |
| `Agastya-EYE/tests/test_inference_preprocessing.py` | 819 |
| `Agastya-EYE/tests/test_inspection_estimates.py` | 4,717 |
| `Agastya-EYE/tests/test_material_ledger.py` | 7,155 |
| `Agastya-EYE/tests/test_pv_degradation.py` | 6,697 |
| `Agastya-EYE/tests/test_pv_surface_defects.py` | 4,847 |
| `Agastya-EYE/tests/test_raptormaps_thermal.py` | 4,215 |
| `Agastya-EYE/tests/test_sort_destination.py` | 2,217 |
| `Agastya-EYE/tests/test_surface_defect_inference.py` | 1,919 |
| `Agastya-EYE/tests/test_system_health.py` | 1,465 |
| `Agastya-EYE/tools/simulate_esp32.py` | 39,784 |
| `Agastya-EYE/training/export_reviewed.py` | 6,611 |
| `Agastya-EYE/training/import_github_inspection.py` | 10,388 |
| `Agastya-EYE/training/import_pv_degradation.py` | 6,246 |
| `Agastya-EYE/training/import_pv_multi_defect.py` | 11,237 |
| `Agastya-EYE/training/import_raptormaps_thermal.py` | 13,805 |
| `Agastya-EYE/training/prepare_dataset.py` | 10,682 |
| `Agastya-EYE/training/pv_degradation.py` | 8,171 |
| `Agastya-EYE/training/pv_surface_defects.py` | 7,610 |
| `Agastya-EYE/training/raptormaps_thermal.py` | 3,823 |
| `Agastya-EYE/training/train_classifier.py` | 11,306 |
| `Agastya-EYE/training/train_pv_severity.py` | 11,258 |
| `Agastya-EYE/training/train_surface_defect_classifier.py` | 11,914 |
| `Agastya-EYE/training/train_thermal_classifier.py` | 11,590 |
| `Agastya-EYE/web/app.js` | 47,169 |
| `Agastya-EYE/web/index.html` | 43,773 |
| `Agastya-EYE/web/materials.js` | 10,500 |
| `Agastya-EYE/web/process.js` | 5,719 |
| `Agastya-EYE/web/styles.css` | 25,371 |
| `Build Files and Steps/Stage 3/STAGE3_BUILD_PLAN.md` | 11,800 |
| `Build Files and Steps/Stage 3/STAGE3_ROLLER_AND_LIBERATION_PLACEMENT_REASSESSMENT_2026-11-19.md` | 5,449 |
| `Build Files and Steps/Stage 3/STAGE3_THERMAL_DEVELOPMENT.md` | 14,704 |
| `Build Files and Steps/Stage 4/README.md` | 2,061 |
| `Build Files and Steps/Stage 4/STAGE4_ARCHITECTURE_AND_ROUTE_DECISION_2026-10-16.md` | 4,373 |
| `Build Files and Steps/Stage 4/STAGE4_ARCHITECTURE_REASSESSMENT_2026-11-19.md` | 11,429 |
| `Build Files and Steps/Stage 4/STAGE4_DEVELOPMENT_ROADMAP.md` | 12,606 |
| `Build Files and Steps/Stage 4/STAGE4_EQUIPMENT_INVENTORY_TEMPLATE.csv` | 803 |
| `Build Files and Steps/Stage 4/STAGE4_FEASIBILITY_REVIEW.md` | 20,125 |
| `Build Files and Steps/Stage 4/STAGE4_FEED_GAP_REPAIR_RESEARCH.md` | 19,723 |
| `Build Files and Steps/Stage 4/STAGE4_FEED_REQUIREMENTS.md` | 8,239 |
| `Build Files and Steps/Stage 4/STAGE4_LITERATURE_REVIEW.md` | 27,658 |
| `Build Files and Steps/Stage 4/STAGE4_METHOD_COMPARISON_AND_CALCULATIONS.md` | 22,113 |
| `Build Files and Steps/Stage 4/STAGE4_MODEL_CRITIQUE_AND_ALTERNATIVES.md` | 16,100 |
| `Build Files and Steps/Stage 4/STAGE4_READINESS_AUDIT_2026-10-06.md` | 5,611 |
| `Build Files and Steps/Stage 4/STAGE4_RESEARCH_COMPLETION_BRIEF_2026-10-08.md` | 16,349 |
| `Build Files and Steps/Stage 4/STAGE4_SOFTWARE_AND_MODEL_RESEARCH.md` | 11,847 |
| `Build Files and Steps/Stage 4/STAGE4_TRIAL_LOG_TEMPLATE.csv` | 625 |
| `CHANGELOG.md` | 21,706 |
| `PROJECT_STATUS.md` | 7,727 |
| `PROJECT_UNDERSTANDING_AUDIT.md` | 268 |
| `README.md` | 1,855 |
| `SESSION_HANDOFF.md` | 13,502 |
| `Stage 3 Prototype Development/ARCHITECTURE_RECONCILIATION.md` | 3,601 |
| `Stage 3 Prototype Development/Figures/Stage_3_Architecture_Decision.svg` | 3,012 |
| `Stage 3 Prototype Development/README.md` | 2,960 |
| `Stage 3 Prototype Development/Source/build_documents.js` | 22,295 |
| `Stage 3 Prototype Development/Source/build_workbooks.py` | 18,219 |
| `Stage 3 Prototype Development/Stage_3_Decision_Report.md` | 6,933 |
| `STAGE3_STAGE4_INTERFACE.md` | 5,904 |
| `START_HERE.md` | 3,372 |
| `00_Project_Management/GITHUB_STAGED_FILE_REVIEW_2026-11-20.md` | 32,723 |

## Synchronization status

This complete path/size manifest describes the current reviewed local `main` source tree. The initial set was published with a regular push; see the repository-preparation record for synchronization history. Keep using regular non-force pushes.
