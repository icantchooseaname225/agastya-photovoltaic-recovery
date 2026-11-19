# Engineering Feasibility and Next Research Priorities

**Report ID:** AG-R06  
**Version:** 1.0 | **Prepared:** 13 October 2026  
**Assessment:** Current evidence is insufficient for a positive process-feasibility or economic conclusion.

## 1. Decision statement

AGASTYA is a research concept with a coherent four-stage measurement-oriented architecture and relevant literature to motivate testing. It is not yet a demonstrated silver-recovery process. Available evidence supports planning a controlled, feed-specific materials-characterization and separation campaign. It does not support a recovery guarantee, purified-silver output, net environmental benefit, throughput, energy target, or business case.

## 2. Demonstrated capabilities

- Current stages and legacy thermal-model boundary have been reconciled and recorded.
- Source-specific literature metrics are traceable and qualified for access/transfer limitations.
- A guarded accounting implementation preserves unknown process values rather than forcing a result.
- The historical thermal sweep has been reanalyzed; dwell and contact conductance are its strongest main effects for several temperature/energy outputs.
- A refined thermal finite-volume model and timestep study are being used only to examine numerical resolution of optional pretreatment assumptions.
- The 2023 IEA PVPS hot-knife LCA demonstrates that a pilot plant can be assessed with a defined functional unit and inventory, while also identifying data gaps for later laminate and metal processing. Its process-specific inventory is not an AGASTYA estimate.

## 3. Unverified hypotheses and constraints

| Claim or decision | Current evidence | Feasibility status |
|---|---|---|
| Ag can be enriched electrostatically from prepared c-Si material | One direct PV study reports a paper-specific Ag-separation metric; other work shows co-concentration | Worth controlled testing; AGASTYA performance unknown |
| Stage 2 liberates useful Ag-bearing particle classes | No AGASTYA PSD, liberation or assay | Unknown |
| Stage 4 produces silver metal | Stage 4 is sampling/assay/accounting | Unsupported and outside current stage definition |
| Process energy or environmental savings are favorable | No measured power, transport, consumables, waste or avoided-product data | Not assessable |
| Process is economically viable | No equipment, labor, yield, assay, refining, logistics or product-price data | Not assessable |
| Thermal pretreatment improves downstream recovery | No instrumented trial or separation-quality data | Optional, unverified hypothesis |

## 4. Environmental and operational considerations

Potentially relevant burdens include transport, electricity, module damage, containment/dust collection, polymer residues, assay consumables and downstream refining. Thermal routes can generate gaseous products; pyrolysis literature is not enough to estimate emissions from a hot knife. Electrostatic feed handling may create dust and static/spark hazards. These considerations require equipment-specific safety review, local waste rules and measurements; no generic risk score or environmental benefit is assigned here.

Frischknecht et al. used a 1 kg framed c-Si module functional unit and pilot data for hot-knife delamination. Their analysis found transportation and electricity were important contributors in that modeled system and excluded downstream Ag/Cu recovery from the delamination boundary. This is useful for boundary design but not directly transferable to a different plant, geography or feed.

## 5. Advancement gates

**Gate 1 — Feed definition:** traceable c-Si module or homogeneous lot; technology and condition recorded; chain of custody; safe sample plan.

**Gate 2 — Baseline characterization:** calibrated masses; representative split; validated Ag assay and QA/QC; uncertainty/reporting limits; full Stage 1/2 mass and PSD data; dust capture.

**Gate 3 — Separator trial:** measured geometry and operating conditions, documented electrical and dust controls, randomized replicates, feed properties by class, all product/reject/middling/loss masses and assays.

**Gate 4 — Model validation:** parameters fixed from calibration data; model predictions compared against held-out replicates; report errors and residuals; no fitting and validation on the same runs alone.

**Gate 5 — System feasibility:** measured energy, labor, consumables, waste handling and downstream acceptance; system boundary and functional unit defined; compare alternative routes with consistent scope.

## 6. Five highest-priority research tasks

1. **Identify and secure one representative c-Si feed lot.** Record model/year/cell architecture, condition, dimensions, mass and parent-child sample IDs.
2. **Agree the Ag assay and sampling plan with a qualified laboratory.** Establish preparation, QA/QC, reporting limits, retained splits and uncertainty before processing.
3. **Run a contained Stage 1/2 mass and particle-characterization pilot.** Weigh every stream, collect dust, measure PSD and characterize Ag association/liberation.
4. **Dimension and instrument the intended electrostatic separator.** Record electrodes, gap, voltage/polarity, roll/splitter, feed rate, humidity, power and all product streams; then run replicated tests.
5. **Build a stage-wise mass/Ag and energy ledger from measured data.** Use it to decide whether a trajectory model, environmental inventory, and economic analysis are warranted.

## 7. Decision after this phase

Proceed to feed characterization and Stage 1/2 measurement planning. Do not yet select a high-fidelity electrostatic solver, assign probabilistic recovery distributions, claim Ag metal production, or publish an economic/environmental feasibility verdict. Continue the thermal model only if a hot-knife pretreatment remains under consideration and can be instrumented.

## References

- Frischknecht, R., Komoto, K. & Doi, T. (2023). [IEA PVPS hot-knife LCA](https://iea-pvps.org/wp-content/uploads/2023/07/Report_IEA-PVPS_T12-25-2023_LCA-PV-Recycling-Hot-Knife.pdf).
- Yang, X. et al. (2019). [Electrostatic separation of Ag and Si in waste c-Si cells](https://xbzrb.hbu.edu.cn/EN/10.3969/j.issn.1000-1565.2019.03.004).
- AGASTYA Phase D `Research_Gap_Register.csv`, `Validation_Report.md`, and `Next_Research_Plan.md`.
