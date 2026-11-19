# AGASTYA PROJECT LOGBOOK — DAY 30

**Digital work date:** 23 October 2026  
**Type/status:** AI-assisted Stage 4 literature research and computational-engineering draft; owner review pending.  
**Physical work:** None. No module, sample, lab visit, process trial, assay, purchase, booking or external contact occurred.  
**Short counterpart:** [Day 30 short entry](Short%20Versions/DAY_30_SHORT_ENTRY.md)

## Objective and project baseline

Investigate the proposed Stage 4A mechanical liberation/classification, Stage 4B copper/aluminium removal, Stage 4C silver concentration and downstream route from concentrate to verified silver. Execute the ten requested computational families, identify Indian analytical/process facilities, and prepare a supervised physical-test plan.

The verified project root is C:/Agastya. Current architecture remains Stage 1 inspection/routing → Stage 2 manual frame/JB/cable preparation → Stage 3 guarded hot-knife front-glass separation/thermal treatment → Stage 4 silver removal/recovery. Stage 3 output is a cell/EVA/backsheet laminate, or a rear-glass laminate for glass/glass construction. The Stage 4 route is still open. No project-level physical Ag assay, recovery measurement, laboratory acceptance or feedstock record was located. The thesis contains an older conflicting four-stage/ECS description; it was not edited. Neither the thesis nor canonical architecture was changed.

## Findings: Stage 4A and Stage 4B

Compared three mechanical routes: controlled low-speed size reduction and sieving after current Stage 3; guarded thermal/mechanical delamination followed by sizing; and an industrial shred/sort train. Front-glass removal is not full separation of encapsulant, cells, backsheet or ribbons. Comminution may liberate mixed cell-bearing particles but can smear ductile Ag and transfer valuable material to fines/dust. Recommended first physical gate is a small, supervised, mass-balanced size-classification test with every stream and dust collected and assayed.

Gajare et al. (2025) report roughly 5% mass below 150 µm and 0.85 wt% Ag for the metal-rich fines in their specific processed c-Si feed. At an assumed 500 ppm raw-feed grade, this implies 85% Ag partition to that fines fraction by mass balance; 85% is derived scenario arithmetic, not the paper’s measured recovery and not an Agastya result. Sim et al. report high Ag partition to fine fractions for different feed categories; their fractions are not assumed to match Agastya.

ECS is not selective for copper versus aluminium or silver. It separates liberated conductive particles from nonconductors with size/shape/field-dependent behavior. Published UHF equipment information reports nonferrous items down to about 2–3 mm; the cited Ag-rich fines are below 150 µm. Silver metallization remains bonded to silicon unless physically liberated. Recommendation: omit ECS from the base route. Consider only on a measured coarse, dry, liberated conductor stream, paired against no-ECS control and with Ag assays on both products. Manual removal/screening of liberated ribbons is a simpler first comparator. Dry electrostatic separation remains an alternative because the cited PV study co-concentrated Si, Ag and Al but does not give a transferable mass-weighted Ag recovery/grade.

Break-even model: if an ECS reject loses fraction p of feed Ag, downstream relative recovery needs to exceed 1/(1−p)−1 to restore final Ag mass. Model thresholds are 5% Ag loss → >5.26% relative gain; 10% → >11.11%; 20% → >25%. These are equations, not measured separator performance.

## Findings: Stage 4C and downstream silver

The strongest direct flotation benchmark located is Saffarian, Galvin and Firouzi (2026). They used delaminated c-Si cells, crushed and ground to about P80 103 µm, in small mechanical flotation cells. The paper reports rougher flotation in tap water at 97.55 ± 0.03% Ag recovery and 32.2 ± 2.3 upgrade. A cleaner result reports 86.5 ± 2.8% recovery and 62.6 ± 2.0 upgrade, around 47 wt% Ag concentrate. The protocols/water baselines differ and must not be multiplied as a single sequence. Concentrate is not refined silver. At an illustrative 0.75 wt% feed assay, the code derives 24.15 wt% rougher grade and 3.03% mass yield; cleaner 46.95 wt% grade and 1.38% mass yield. These are model arithmetic at that feed grade, not new measurements.

The flotation paper describes metallic Ag metallization associated with silicon after grinding. Likely unquantified impurities include Si/cell fragments, copper, aluminium, Sn/Pb-bearing solder/ribbons, polymer/glass and other metals. Published 2026 PV-cell literature reports 99.7% Ag recovery and 99.6% purity for its organic-acid route; that cell-feed result is not validated on an Agastya flotation concentrate. A 2024 hydro/electrochemical study reports 98.7 ± 1.4% recovery, not a purity result. Recommended downstream path is concentrate homogenization and multielement assay, then qualified toll-refiner acceptance review. If no refiner accepts it, a specialist lab can assess selective dissolution/release, impurity separation, silver recovery, washing/drying and residues. Professional electrorefining can be considered if required. Final product needs independent assay; ISO 15096:2020 covers high-purity Ag ≥999‰ by ICP-OES difference and ASTM B413-26 specifies refined-silver grades at 999.0, 999.5 and 999.9 fineness. Recovery, concentrate grade and purity remain distinct.

## Executed simulations and numerical checks

Ten computational families were executed from a new source package with seed 20261023 and 100,000 draws for stochastic cases: (1) Stage 4A material/Ag stream balance; (2) lognormal size-cut sweep; (3) ECS coarse-size screen; (4) ECS silver-loss break-even; (5) flotation grade/recovery/mass yield; (6) route comparison; (7) staged downstream Ag recovery; (8) integrated Ag recovery and stream losses; (9) Spearman sensitivity; and (10) experiment-priority ranking.

- S1 used an illustrative 1 kg component composition, not an Agastya module bill of materials. Median target mass yield was 14.3%; median Ag retention 77.4% (p05–p95 62.0–89.5%). Coarse, polymer/glass and fines/dust rejects were tracked. Maximum mass-closure error was below 5×10⁻¹⁶ and Ag-closure error below 6×10⁻¹⁷ g due to floating-point rounding.
- S2 was calibrated to 5% mass below 150 µm and derived 85% Ag partition at the same cut. Its base curve gives at 100 µm: 1.16% mass, 61.8% Ag and 2.65 wt% scenario grade. The 150 µm anchors are literature-calibrated; intermediate cuts are unvalidated model interpolation.
- S3 estimated median modeled mass ≥2 mm of about 0.96%. Ag share is negligible under the assumed fine-Ag PSD. This is not an ECS trajectory model; particle shape, liberation, field map, rotor/belt geometry and conductivity distribution are absent.
- S4 produced break-even gains above. S5 rejected impossible concentrate grades over 100 wt% and checked grade = feed grade × upgrade and yield = recovery / upgrade.
- S8 integrated the assumed 4A Ag-capture, flotation and downstream recovery ranges. Median overall Ag recovery after optional finishing was 64.3% (p05–p95 54.6–74.4%), or 0.322 g Ag from a 1 kg feed assumed to contain 0.5 g Ag. This is an assumption envelope, not a forecast; it does not predict final purity.
- S9 rank correlations were flotation recovery ρ≈0.70, Stage 4A Ag capture ρ≈0.64, release ρ≈0.19, solution capture ρ≈0.10 and optional finishing ρ≈0.04. This order reflects analyst-selected ranges.
- S10 prioritizes feed and 4A stream masses/Ag-Cu-Al assay; then PSD and size-fraction assays; conditional paired ECS/no-ECS; flotation replication; and refiner acceptance/downstream review.

Runtime was Python 3.12.14 with NumPy 2.5.2, SciPy 1.18.1, pandas 3.0.6 and Matplotlib 3.11.2. Torch/CUDA and RTX 4050 were available but not needed. No usable CFD, FEM, electromagnetic or flotation bubble solver was found or used. No field, particle trajectory or bubble-attachment model is claimed. Five pytest checks passed: mass and Ag closure, PSD calibration, flotation identity, invalid-grade rejection and ECS break-even. Tests verify arithmetic only, not model assumptions or physical performance.

## India laboratories, instruments and feedstock

Delhi NCR priority: IIT Delhi CRF for approved solid ICP-MS assay (published external academic student/faculty rate ₹1,000 + GST; method page recommends 100–500 mg solids for digestion-based samples, operator approval required); CSIR-NPL NPLONE for microscopy, qualitative XRF and PSD (published tentative rates: FESEM ₹1,500 + GST, EDS ₹1,000 + GST, qualitative XRF ₹1,100 + GST, micron PSD ₹500/sample); NISE Gurugram for intact PV module characterization, not Ag assay or recycling.

Process leads: JNARDDC Nagpur lists a lab flotation machine, crushing/milling/sieving, ICP-OES/MS, XRF and microscopy; Ag/PV feed acceptance and price are unknown. CSIR-IMMT has flotation-column amenability and pilot-testing capabilities but no PV silver service/access quote was found. CSIR-CMERI documents solar PV recycling and process-plant development. IIT Hyderabad is a research collaboration lead, not a public testing offer. CSIR-CGCRI SAIF and IIT Bombay CSIF are external analytical alternatives with sample/access/fee confirmation needed. No facility was contacted.

Inventory covers guarded glass-separation interface, frame/JB tools, low-speed shear/shredder, sealed crusher/mill, sieves/PSD, balance and splitter, microscopy/SEM-EDS, XRF, ICP-OES/MS, conditional ECS, electrostatic separator, lab flotation cell and calibrated support equipment, dust capture, filtration/drying and specialist-only chemical/refining infrastructure. Recommendation: access process machinery through a supervised institution; do not buy before the first assay-balanced test.

Indicative assay cost illustration: 15 IIT Delhi solid ICP-MS slots at ₹1,000 + 18% GST = ₹17,700, plus two NPL PSD samples at ₹500 + GST each = ₹18,880 if 18% GST applies. This excludes sample preparation/digestion, matrix work, QC, extra repeats, logistics, current fee confirmation and any process-trial charges; it is not a quote. NISE’s official form lists ₹5,200 + GST for field-module STC testing; fee validity requires confirmation.

Lowest-cost credible feedstock path is to request one traceable intact retired c-Si module from an owner, campus facility or maintenance channel through an approved supervised facility. Delhi’s vendor portal does not promise an EOL module. CPCB covers solar PV panels/cells/modules under E-Waste Rules. No seller/recycler was contacted; no price/offer verified. Shattered cells do not test front-glass removal.

## Proposed supervised physical test sequence

1. Approve source, c-Si construction, module identity, custody, receiving facility and safe end-of-test route.
2. Establish baseline dry mass, photos, frame/JB status and representative assay/sampling plan.
3. Run controlled Stage 4A size reduction/sieving on an approved coupon; retain all coarse, intermediate, fine, polymer/glass and dust streams.
4. Record masses, sieve apertures, time, energy if available, images, PSD/liberation and Ag/Cu/Al/Si/Sn/Pb assays with duplicates and uncertainty.
5. Only if a coarse liberated conductor fraction exists, compare paired no-ECS/ECS products and assay both.
6. Compare fines and flotation (and later electrostatic concentration) using feed, concentrate and tailings mass/assays, repeatability, water/reagent record and facility waste plan.
7. Obtain concentrate acceptance and downstream proposal from qualified refiner/laboratory; assay final product to appropriate method.

Do not set numeric go/no-go limits until measurement uncertainty, repeatability, actual feed grade and refiner requirements are known. No home chemical refining, high-temperature salt processing or waste treatment is planned.

## Deliverable and project-state record

The editable report is `C:/Users/jay91/Documents/Codex/2026-10-23/files-pasted-by-the-user-agastya/outputs/Agastya_Stage4_Investigation_2026-10-23/Agastya_Stage4_Labs_Equipment_and_Physical_Testing_Plan.docx`. Machine-readable laboratory, equipment, route and simulation CSVs and the complete source/config/output/figure/test package are in the same investigation folder. Word export was visually reviewed page-by-page; LibreOffice was unavailable, so the installed Microsoft Word renderer and bundled Poppler were used. The Stage 4 investigation output is a research draft pending owner review.

Modified project navigation: full/short logbook index, short-version README, project index latest-entry pointer and OPEN_QUESTIONS latest-entry summary. Pre-edit SHA-256-verified copies are in `C:/Agastya/99_Archive/Logbook_Phase5_Before_Update_2026-10-23/`. No thesis, architecture, historic simulation output, evidence register or decisions log was edited.

Sources include: [current architecture](../AGASTYA_ARCHITECTURE.md); flotation [Saffarian et al.](https://doi.org/10.1016/j.mineng.2026.110189); fines [Gajare et al.](https://doi.org/10.1016/j.solmat.2024.113259); size partition [Sim et al.](https://doi.org/10.1016/j.wasman.2022.11.023); electrostatic study [de Souza & Veit](https://doi.org/10.1016/j.cec.2023.100027); ECS [Eriez](https://www.eriez.com/Products/Metals-Recycling/Nonferrous-Recovery/Eddy-Current-Separators); PV hydrometallurgy [Luo et al.](https://doi.org/10.1016/j.jece.2026.122096) and [Russo et al.](https://doi.org/10.1016/j.eti.2024.103803); ASTM [B413-26](https://store.astm.org/b0413-26.html); ISO [15096:2020](https://www.iso.org/standard/75283.html); BIS [IS 2113:2014](https://standards.bis.gov.in/); NPL [NPLONE](https://www.nplindia.org/index.php/commercial-services/characterized-your-sample-at-npl/); IIT Delhi [external-user process](https://crf.iitd.ac.in/Booking-System/External-Users.html), [ICP-MS sample guidance](https://crf.iitd.ac.in/All-Facilities-/ICP-MS.html), [charges](https://crf.iitd.ac.in/files/CRF_Charges_List.pdf); NISE [testing](https://nise.res.in/departments/pv-module-systems-bos-testing); JNARDDC [testing](https://www.jnarddc.gov.in/en/services/testing.aspx); IMMT [flotation](https://www.immt.res.in/flotation-column); CMERI [waste-processing CoE](https://www.cmeri.res.in/department/coe-centre-excellence-waste-processing-segregation-technologies); CPCB [FAQ](https://cpcb.nic.in/uploads/Projects/E-Waste/FAQ_ewaste_23012024.pdf) and [portal](https://www.eprewaste.cpcb.gov.in/); Delhi Solar Portal [vendors](https://solar.delhi.gov.in/page/empaneled-vendors).
