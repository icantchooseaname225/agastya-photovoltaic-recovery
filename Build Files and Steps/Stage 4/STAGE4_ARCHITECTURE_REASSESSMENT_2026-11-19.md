# Stage 4 silver recovery architecture reassessment

**Reviewed:** 19 November 2026  
**Status:** literature-based architecture decision; no AGASTYA feed assay or silver-recovery experiment is documented.

## 1. Actual feed is still an open measurement

AGASTYA has not recorded a physical module, Stage 3 output, particle lot, or assay. The current Stage 3 reference output is glass plus a cell/EVA/backsheet laminate; the foam-roller concept is not yet specified or tested. Stage 4 must not be sized on an assumed composition or particle distribution.

A future Stage 4 feed record must establish, at minimum:

- Module technology and construction, mass and provenance.
- Remaining glass, EVA/backsheet, foam/adhesive residue and other contamination.
- Particle-size distribution, shape, moisture and degree of liberation.
- Whether silver remains thin metallisation attached to silicon-cell pieces, or has been liberated as a separate particle population.
- Ag, Si, Al, Cu, Sn/Pb and other relevant element assays in representative feed and all products/residues.
- Conductivity and density by fraction only when an electrical or density separator is being considered.

Solar-cell silver recovery studies use delaminated and comminuted cell feeds. Their results do not characterize the full module or the unmeasured AGASTYA feed.

## 2. Keep the process terms separate

- **Liberation:** break composite material so the target-bearing phase is exposed or detached from its host.
- **Separation:** partition particles into streams using a physical property such as size, conductivity, density, or surface response.
- **Concentration:** increase silver grade in a product stream; the product still contains other material.
- **Recovery:** fraction of feed silver reporting to the selected product, calculated from feed/product mass and assay.
- **Purification:** remove remaining impurities to meet a stated silver product specification, usually requiring downstream refining and independent assay.

For stream `j`, contained silver is `m_j × a_j`, where `m_j` is dry stream mass and `a_j` is the measured Ag mass fraction. Silver recovery is contained Ag in the selected product divided by contained Ag in the feed. Product grade is contained Ag divided by product mass. A high recovery can have low grade, and a high grade can have low recovery. None of these terms means pure silver by itself.

## 3. Architecture comparison

| Option | Sequence | Evidence and fit | Current decision |
|---|---|---|---|
| **A** | Mechanical liberation → conventional rotating eddy-current separator (ECS) → froth flotation | No located study shows this sequence improves Ag capture on AGASTYA-like silver-coated Si-cell feed. The DOE PV electrodynamic study demonstrates separation of Si/Al and CdTe/Al mixtures at 1–3 mm and says smaller particles approach system limits. This is not proof of silver separation from fine Ag-coated Si. | **Do not use as the default.** Retain an ECS only as a conditional trial if characterization finds a coarse, liberated conductive fraction with a defined value and assay plan. |
| **B1** | Mechanical liberation → one silver-selective rougher flotation operation | Strongest direct silver-focused concentration evidence found: Saffarian et al. used delaminated, ground EoL c-Si cells (P80 about 103 µm). A 1 L rougher test in tap water reported 97.55 ± 0.03% Ag recovery and 32.2 ± 2.3 upgrade. This is a study-specific concentrate, not pure Ag or an AGASTYA forecast. | **Best selective-concentration candidate for a qualified partner-lab study** if feed preparation and the wet-process controls are available. Do not add a cleaner by default. |
| **B2** | Mechanical liberation → one dry size-classification operation | Sim et al. report up to 70% and 80% of feed Ag in the finest fraction for two separate feed categories and >90% polymer in larger fractions. These are literature fraction distributions, not AGASTYA grades or purified product. | **Best low-complexity screening baseline.** Assay every cut and dust stream; treat the finest fraction as an Ag-bearing concentrate candidate for a qualified receiver, not recovered silver. |
| **C** | Stage 3 hot knife + foam roller → adjacent modular mechanical liberation; Stage 4 one selected separator | The IEA PVPS 2025 process description shows hot-knife glass separation followed by laminate shredding/sorting in an industrial line. This supports the material-flow order, not a cost or performance advantage for AGASTYA. A flotation feed still has to meet its demonstrated liberation/size conditions. | **Preferred physical layout to evaluate**, with the liberation module adjacent and bypassable. Formal stage assignment and feed acceptance remain conditional on paired tests. |
| **D** | Alternative dry electrostatic separation, specialized electrodynamic separation, or toll-refinery route | PV electrostatic studies report co-concentration or silicon-focused performance, not a complete Ag mass balance for this feed. Toll refining may avoid AGASTYA installing purification equipment, but acceptance/specification and fees are unverified. | Keep as partner-lab or receiver alternatives after fraction assay. Do not replace the baseline without a silver mass balance and acceptance evidence. |

## 4. Why the current three-step train is not justified

Conventional ECS works best when liberated, sufficiently coarse conductive particles have a useful contrast from the other feed. The DOE PV study's 1–3 mm mixtures concern Si/Al and CdTe/Al, and it notes limits on smaller particles. The available source does not demonstrate that ECS selectively recovers a thin silver print carried on small silicon fragments, nor that it improves subsequent flotation enough to offset particle loss, energy, maintenance and another machine.

The flotation evidence already processes a delaminated and ground cell feed without a conventional ECS step. Therefore the extra ECS stage is unsupported as a default. It could earn a place only if paired feed/product/tailings assays show a complementary coarse conductor product and a net gain in total silver retained at acceptable cost.

Froth flotation has a much closer mechanism-to-target match because the 2026 study specifically tested metallic silver on processed solar-cell feed. Its result remains conditional: the authors used prepared feed, laboratory flotation cells, reagents, controlled water conditions, and analytical assay. AGASTYA has none of the needed measured feed data or verified access yet.

## 5. Recommended experimental sequence

1. Confirm Stage 3 output construction and representative dry mass; preserve a reference aliquot.
2. Characterize untreated feed and any required preparation: image morphology, sieve/PSD, residual polymer/glass, and multielement Ag/Si/Al/Cu/Sn/Pb assay.
3. Run controlled liberation/size classification on matched material and retain every coarse, intermediate, fine, dust, and cleaning-residue stream.
4. Assay all streams and close both total-mass and contained-silver balances with uncertainty.
5. Begin with the dry size-classification baseline. Add ECS only if the measured coarse fraction matches an ECS capability envelope; compare matched with/without ECS arms.
6. If a qualified facility can accept the feed, compare the same characterized feed with a single rougher flotation test. Record water quality, reagent identity/dose, feed size, time, energy, concentrate/tailings mass, assays, repeats and waste route. Do not transfer literature settings without facility approval.
7. Obtain written receiver criteria and a downstream refining route for the concentrate. Assay any final silver product independently.

Predeclare acceptance criteria using actual assay uncertainty and receiver specifications. Do not invent a recovery threshold from the literature.

## 6. Economic and environmental boundary

No verified Indian quotation for a robot, crusher/mill, classifier, ECS, flotation cell, or integrated line was found in this review. No AGASTYA throughput, energy, water use, reagent use, labour duty, maintenance cost, waste cost, or recovery is measured; no profitability or payback is calculable.

The qualitative trade is:

- Removing an unproven ECS would eliminate one machine, feed transfer, power demand and maintenance burden. The savings are real in direction but cannot be assigned a rupee value without matched quotations and a validated process boundary.
- Dry liberation/sieving is the simpler prototype route, but its silver-bearing fines still need a receiver or further treatment.
- Flotation can produce a more selective concentrate under laboratory conditions, but requires controlled water, reagents, fine feed preparation, a flotation cell, tailings management, assays and qualified supervision.
- Integrating liberation after Stage 3 may reduce material handling but can increase dust containment, cleaning, wear, thermal-cell downtime and glass/polymer contamination. Compare whole-line energy and maintenance, not separator-only costs.

For research-prototype, pilot, and industrial scenarios, build a cost model from measured or quoted line items. A consistent cost per accepted panel is:

```text
annualized capital charge / accepted panels per year
+ energy + labour + water + reagents + assay/QC + maintenance + waste/residue handling
```

Use the measured bottleneck throughput of the complete line. Keep external refining and transport visible as separate costs. Do not substitute the silver spot value for realized revenue: a receiver's grade, impurity and fee terms are required.

## 7. Current conclusion

The evidence does not support **mechanical liberation → conventional ECS → froth flotation** as AGASTYA's default. Carry two alternatives into feed characterization:

- **Dry baseline:** mechanical liberation → size classification, with all fractions assayed and a documented concentrate receiver sought.
- **Selective route:** mechanical liberation → one rougher flotation operation at a qualified facility, followed by external refining if the concentrate meets receiver specifications.

Place the liberation unit directly after Stage 3 thermal separation as an adjacent, modular, bypassable cell for the next design iteration. This is a process-layout proposal grounded in published industrial sequence and reduced-transfer logic; better recovery, cost savings, dust control, and quality remain unproven.

## References

- Agraffeil, C. et al. (2025), *Status of PV Module Recycling in IEA PVPS Task 12 Countries*, IEA PVPS T12-31:2025. [DOI](https://doi.org/10.69766/XLFG7020). Industrial hot-knife → laminate shredding/sorting process description.
- Saffarian, H., Galvin, K.P. & Firouzi, M. (2026), “Rethinking silver recovery pathways in end-of-life photovoltaic recycling using froth flotation,” *Minerals Engineering* 242, 110189. [DOI](https://doi.org/10.1016/j.mineng.2026.110189).
- Sim, Y. et al. (2023), “A facile crush-and-sieve treatment for recycling end-of-life photovoltaics,” *Waste Management* 156, 97–106. [DOI](https://doi.org/10.1016/j.wasman.2022.11.023).
- Smith, Y.R., Nagel, J.R. & Rajamani, R.K. (2017), *Comminution and Electrodynamic Eddy Current Separation Studies of End-of-Life Photovoltaic Materials*, U.S. Department of Energy report. [PDF](https://www.energy.gov/sites/prod/files/2017/08/f35/61_Smith_UUtah_PostdocAward.pdf).
