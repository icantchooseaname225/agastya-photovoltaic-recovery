# Validation report

**Validation scope:** file and source traceability, formula implementation, and existing software evidence. No physical AGASTYA process validation occurred.

## Phase D checks performed

| Check | Result | Meaning / limit |
|---|---|---|
| Current architecture against baseline and crosswalk | Passed | Stage definitions and legacy mappings match the controlling project record; this is document consistency, not process validation. |
| Source-to-claim review | Passed with explicit limits | Claims in the literature review identify source type and study-specific limitations; abstract-only sources are not represented as full-text audits. |
| Reference unit conversions | Passed in code self-check and generated output | 300 mg/kg → 0.300 g/kg; 600 g/t → 0.600 g/kg; 630 g/t → 0.630 g/kg. These are arithmetic reference cases. |
| Synthetic accounting formula self-check | Passed | A clearly synthetic fixture gives 20% mass yield, 0.4 wt% target grade, 80% Ag recovery, and zero residuals. It tests formula code only and is not project data. |
| Unknown-value propagation | Passed | Empty measured-process input produces null metrics rather than zero. |
| CSV structure | Passed | Evidence register: 24 records × 10 columns; gap register: 17 × 8; stage templates parse with consistent widths (Stage 1: 16, Stage 2: 15, Stage 3: 28, Stage 4: 22). |
| Markdown local links | Passed | Checked 21 Phase D and project navigation files; no broken local links were found. |
| Project recursive inventory | Recorded | 53,861 file rows before Phase D deliverables; the snapshot inventories metadata and did not semantically inspect every file. |
| Existing accounting tests | Existing project result: 28/28 v2 checks passed | Historical project software check; no implication of process performance. |
| Legacy kernel audit | Existing project result: 22/25 passed; 3 known input-guard failures | Recovery above 100%, grade above 100%, and NaN guard failures remain known; this phase did not rewrite the legacy kernel. |
| External solver execution | Not run | No solver installation/account was available or authenticated in the checked environment. |
| Physical trial or assay | Not performed / no result found | No recovery, grade, purity, throughput, energy, or environmental claim can be validated. |

## Acceptance checks for the next physical/model phase

1. Feed technology, sample identity, condition, and chain of custody are recorded.
2. Calibrated masses account for all input, output, and collected-loss streams within a predeclared tolerance; no balancing plug is used.
3. Assay method and sample preparation are agreed with a qualified lab for the PV matrix; QA/QC, reporting limits, replicate results, and uncertainty are retained.
4. Stage 2 PSD and Ag association are measured by feed lot and size class.
5. Stage 3 geometry, settings, environment, feed rate, and bin masses are recorded for each replicate; all bins and losses are assayed.
6. Model parameters are fixed from calibration data, then predictions are compared with withheld replicate runs. Report errors and residuals, not only fitted plots.
7. Stage-specific and overall balances distinguish mass yield, Ag grade, recovery, enrichment, and product purity.
8. Any claim about metal product/refining is validated by the receiving/refining route and lies outside current AGASTYA Stage 4.

## Limitations

This report validates reproducibility of simple conversions and code logic only. It does not validate the model form of an electrostatic separator, the accuracy of any literature metric as an AGASTYA predictor, or any physical performance. Model credibility requires empirical inputs and independent comparison data.
