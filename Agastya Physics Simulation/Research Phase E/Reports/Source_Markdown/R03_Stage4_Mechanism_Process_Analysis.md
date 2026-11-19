# Stage 4 Mechanism and Process Analysis

**Report ID:** AG-R03  
**Version:** 1.0 | **Prepared:** 13 October 2026  
**Boundary:** Current Stage 4 is representative sampling, assay, and accounting; it does not chemically transform or refine silver.

## Executive finding

The actual Stage 4 mechanism in the governing AGASTYA process model is analytical and evidentiary. It converts collected stream records and representative samples into a defensible material/Ag balance. The operation does not separate Ag from Si, dissolve Ag, precipitate metal, or produce refined silver. The main engineering risk is not an omitted chemical reaction in Stage 4; it is that nonrepresentative samples, missing stream masses, unvalidated sample preparation, and untracked dust can create a false recovery or purity claim.

## 1. Stage interface and workflow

{{FIGURE:stage4}}

Required Stage 4 inputs are the physical feed and every output stream from a defined Stage 1, 2, or 3 run, each linked by IDs and a known parent-child relationship. For each stream, record tare and gross mass, scale resolution/check, collected dust or spill mass, time, operator, equipment settings and sample split. Homogenize or otherwise prepare a representative sample using a qualified procedure; retain a sealed archive split. The laboratory must agree on sample digestion/preparation and an Ag assay appropriate to the composite Si/glass/polymer/metal matrix.

Instrumental methods are not interchangeable with a validated matrix method. EPA SW-846 6010D and 6020B are ICP-OES and ICP-MS analytical methods/guidance, respectively; their existence does not establish recovery from a particular PV powder preparation. Portable XRF can screen elemental content but is not phase identification and does not establish metallic-silver purity. A qualified laboratory should specify blanks, calibration checks, duplicates, matrix spikes or appropriate reference materials, reporting limits, sample mass, uncertainty and preparation recovery.

## 2. Governing accounting

For feed `f`, product stream `p`, and all measured streams `i`:

`m_Ag,f = M_f x_Ag,f`  
`Ag recovery_p = (M_p x_Ag,p) / (M_f x_Ag,f)`  
`Ag grade_p = x_Ag,p`  
`mass yield_p = M_p / M_f`  
`enrichment_p = x_Ag,p / x_Ag,f`

Mass closure and Ag closure are separate:

`r_mass = M_f - Σ_i M_i - M_documented_loss`  
`r_Ag = m_Ag,f - Σ_i(M_i x_Ag,i) - m_Ag,documented_loss`.

Residuals should be reported in absolute units and relative to an explicitly stated denominator. A closure tolerance is set before the run based on scales, sampling and lab uncertainty. Never force closure by adding an unmeasured balancing stream or treating a missing value as zero.

## 3. Silver-bearing stream tracking

The silver-bearing material may be distributed among Ag-bearing cell fragments, Si-rich fractions, Cu-bearing ribbons, glass, polymer residues, fines, airborne dust captured in filters, separator bins, and material remaining on equipment. The fraction of Ag in any one stream is currently unknown for AGASTYA. The Phase D literature review found study-specific reports of Ag partition into fine fractions and study-specific electrostatic outcomes; these are hypotheses for feed-specific measurement, not universal fractions.

The Stage 4 ledger must preserve each stream's status as measured, calculated, literature-derived, or unknown. Assay each output if calculating total recovery. If only selected streams are assayed, report partial Ag accounting and identify the unmeasured contribution; do not call it overall recovery.

## 4. Failure modes and controls

| Failure mode | Direction of bias | Required control |
|---|---|---|
| Feed split is not representative | Feed Ag inventory can be over- or underestimated | Defined sampling protocol; replicate splits; retained feed sample |
| Fine dust is missed | Apparent mass and Ag closure loss; recovery may be biased | Containment, filter capture, equipment cleanout and dust sample |
| Sample preparation does not dissolve/recover Ag | Assay under-reports Ag | Matrix-specific preparation validation, spikes/reference materials |
| Analytical blank or contamination is ignored | Apparent Ag grade can increase | Blank sequence, clean tools, documented limits and uncertainty |
| Product grade is treated as recovery | Confuses concentration with total Ag captured | Report grade, yield, recovery, enrichment separately |
| Incomplete output stream record | Cannot reconcile mass or Ag | Stream IDs, weigh all products/rejects/middlings/losses |
| “Concentrate” is described as pure silver | Overstates product state and value | State chemical form is unresolved; downstream refining is outside scope |

## 5. Current evidence and limits

Phase D's accounting kernel has passed arithmetic and unknown-value propagation checks. It can calculate normalized literature-reference inventories and synthetic fixtures used only for formula self-checking. There are no measured AGASTYA input/output masses, assays, lab QA/QC records, reporting limits, or assay uncertainty values. Accordingly, current feed Ag, recovery, grade, purity, balance residual and uncertainty are all unknown.

## 6. Next assay experiment

The first useful Stage 4 experiment is an assay-validation plan tied to a single traceable c-Si feed lot and retained split. Ask an accredited/qualified laboratory to review the actual composite matrix and recommend preparation, sample mass, dilution, analyte range, QA/QC and detection limits. Submit blind duplicates and matrix spikes where available. Before processing, agree how all feed, concentrate, middlings, rejects, dust and equipment cleanout will be sampled and weighed. The resulting measured balances can then support a Stage 3 test and later a calibrated model.

## References

- U.S. EPA, SW-846 Method 6010D, ICP-OES; and Method 6020B, ICP-MS. These methods require matrix-specific sample preparation and quality controls.
- AGASTYA Phase D: `Stage_4_Model/README.md`, `Research_Gap_Register.csv`, `Validation_Report.md`, and `Four_Stage_Process_Model.md`.
- Yang, X. et al. (2019). [Electrostatic separation study abstract](https://xbzrb.hbu.edu.cn/EN/10.3969/j.issn.1000-1565.2019.03.004). Its reported efficiency is not an AGASTYA recovery value.
