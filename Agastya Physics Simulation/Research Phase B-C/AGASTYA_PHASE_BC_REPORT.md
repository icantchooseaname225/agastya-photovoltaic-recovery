# AGASTYA Phase B/C research report

> **Source correction, 2026-10-11:** The historical v2 output below used 630 g/t as its Dias reference. The publisher abstract states 600 g/t; 630 g/t appears in secondary conclusion excerpts and is not reconciled. The v3 source-qualified run in this folder preserves 630 only as an unresolved discrepancy and does not treat it as verified. The 300 ppm review composition scenario also has unresolved source basis. Neither is an AGASTYA measurement.

Prepared 2026-10-11. Research stage: evidence and model validation; no physical AGASTYA trials.

## Summary

Phase B/C contains 14 evidence records, seven software/tool records and five route comparisons. It regenerates two normalized reference scenarios and nine sensitivity rows; runs 28 v2 accounting unit tests; and probes the preserved Phase A kernel with 25 cases. Three legacy input-guard gaps remain visible.

Dry size classification has a useful lower-complexity comparator. Electrostatic PV research reports Ag co-concentration but no accessible mass-based Ag recovery. Silver-focused flotation has direct laboratory evidence on prepared cell feed, not whole modules or AGASTYA feed. Chemical studies report study-specific extraction with specialist reagent and waste burdens.

## Actual work

CPython 3.14.4 generated the CSV outputs. Separate normalized arithmetic gives 300 ppm → 0.300 g Ag/kg and 630 g/t → 0.630 g Ag/kg. Unknown process recoveries, product mass/grade and balance residuals remain blank or symbolic. Published rounded flotation-table values were recalculated as a diagnostic. The v2 unit tests pass 28/28; legacy probes pass 22/25 and flag three missing guards in preserved Phase A code.

## Defensible conclusion

AGASTYA establishes a structured accounting framework and literature comparison, not recovered silver, a validated separator, measured sample, assay or solver result. The most useful next investigation is a supervised, sample-defined size-partition study with weighed streams and qualified Ag assays. It can show whether Stage 2 alone creates a useful Ag-bearing fraction before Stage 3 complexity is added.

## Limits

Studies use different feeds, preparations, endpoints and assays. No local panel source, physical sample, solver model, assay or competition-level details are documented. These limits prevent a process-performance ranking and a submission-readiness claim.

Start with evidence_database_v2.csv, separation_route_comparison_v2.csv, scenario_results_v2.csv, sensitivity_analysis_v2.csv and published_data_validation_v2.csv. Companion analyses are in the named markdown reports in this folder.

