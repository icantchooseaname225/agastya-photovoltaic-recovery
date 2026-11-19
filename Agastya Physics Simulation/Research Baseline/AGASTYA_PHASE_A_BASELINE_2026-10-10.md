# AGASTYA Integrated Solar-Panel Silver Recovery System
## Phase A research baseline and execution gate

**Prepared:** 10 October 2026  
**Scope:** Research and input definition before new integrated solver runs  
**Status:** Baseline documented; sample and software access remain unverified

## Executive summary

The latest project charter defines four stages: (1) panel disassembly and component separation, (2) mechanical liberation of silver-bearing material, (3) electrostatic separation and concentration, and (4) recovery verification, material accounting, and purity assessment. This sequence is the controlling architecture for new work.

The existing Agastya simulation documents use different stage numbers: Stage 3 is a hot-knife thermal calculation and Stage 4 is comminution and size classification. Those legacy files remain valid records of their earlier assumptions, but their stage numbers do not match the new charter. A crosswalk is included in this folder. New work must use the charter's stage names and IDs to prevent mixing unlike processes.

Crystalline-silicon cells do contain silver-bearing printed contacts, but the silver is a small fraction of the module and is attached to a structured cell/interconnect feed. Published module-level silver values span approximately 300–630 mg/kg in the sources reviewed here; this is a difference between particular study feeds and accounting bases, not a universal composition range or statistical confidence interval. A measured feed assay is required before an Agastya silver balance can be reported.

Published evidence supports mechanical pretreatment and size classification as feed preparation, but it does not establish that size alone recovers silver. A 2023 electrostatic-separation study reports a silicon-rich output, not an Ag product. A 2026 bench flotation study reports silver recovery and upgrade from delaminated, crushed cells and is a useful comparator if electrostatic separation performs poorly. Neither result predicts Agastya performance.

No physical panel, coupon, particle lot, instrument access, assay, or external solver run is verified in the workspace. The project has local Python and NumPy. Candidate browser and student tools have been researched but not authenticated or installed. The next credible step is to identify the actual panel/cell type and source, measure or obtain a component inventory, then decide whether a partner or student license enables the required model.

## 1. Architecture and material interfaces

The flow below follows the latest charter. Stream names are planned identifiers; they do not imply that a physical stream exists yet. See the [four-stage process-flow diagram](agastya_four_stage_process_flow.svg).

S0 identified c-Si module → Stage 1 disassembly → S1a glass; S1b frame/junction box/cables; S1c laminate/cell-bearing feed → Stage 2 mechanical liberation and classification → S2a Ag-bearing cell/contact particles; S2b silicon-rich particles; S2c glass, Cu, polymers and other residues → Stage 3 electrostatic separation candidate → S3a candidate enriched concentrate; S3b middlings and rejects → Stage 4 representative sampling and assay → Ag mass balance, recovery, grade and uncertainty.

Stage 1 is component routing, not silver refining. It should distinguish front glass, front/rear encapsulant, crystalline-silicon cells, front and rear metallization, Cu interconnects/ribbons (which may be silver-coated), aluminum frame, junction box/cables, rear glass or polymer backsheet, and any identified solder, coatings, sealants, or contaminants. Monocrystalline versus multicrystalline identity, cell architecture, bifacial/glass-glass construction, busbar count, module age, and damage can change the inventory. None is yet confirmed for an Agastya feed.

Stage 2 is the liberation problem. Silver contacts are printed on silicon cells and can remain attached to silicon fragments; ribbons and busbars may carry Cu and Ag coatings. A particle-flow solver can predict motion only after particle shape, size, density, electrical properties, and contact/charge behavior are defined. It does not automatically predict microscopic fracture or silver liberation. A suitable fracture or measured liberation model is required.

Stage 3 is an electrostatic hypothesis to test, not a guaranteed silver separator. Conductivity is not magnetic susceptibility, and Ag is not the only conductive material: Cu and Al are also present. Moisture, surface contamination, particle shape, size, charge-to-mass ratio, field geometry, feed loading, and grounding can change trajectories. Separate electric-field calculation and particle dynamics may be possible, but the data-transfer and license combination must be confirmed before they are represented as a coupled run.

Stage 4 measures and reconciles all outputs. A silver-bearing concentrate is not pure silver. Record concentrate mass, Ag mass fraction, Ag mass, stage recovery, overall recovery, and chemical purity as separate quantities. XRF measures elemental composition and is a candidate for rapid screening, but EPA Method 6200 is specified for soils and sediments; PV fragments/powders need matrix-specific method validation and calibration. ICP-OES (EPA 6010D) and ICP-MS (EPA 6020B) measure elements in solutions/digests; a solid PV aliquot must first be prepared by a lab-validated digestion, and completeness/recovery for the Ag/Si/glass/polymer matrix must be confirmed. None of these elemental methods by itself identifies Ag chemical phase or establishes product purity. Confirm the method scope, sample preparation, detection and quantification limits, uncertainty, reference materials, and minimum sample mass with the receiving laboratory. [EPA 6200](https://www.epa.gov/hw-sw846/sw-846-test-method-6200-field-portable-x-ray-fluorescence-spectrometry-determination), [EPA 6010D](https://www.epa.gov/hw-sw846/sw-846-test-method-6010d-inductively-coupled-plasma-optical-emission-spectrometry-icp-oes), [EPA 6020B](https://www.epa.gov/hw-sw846/sw-846-test-method-6020b-inductively-coupled-plasma-mass-spectrometry).

## 2. Literature findings relevant to the architecture

### Silver occurrence and inventory

A 2016 peer-reviewed study mapped and quantified silver in waste crystalline-silicon modules. It reported an average of 630 g/t (0.63 g/kg) for its study modules, located silver in the semiconductor/cell region as fine printed threads, and reported 100 micrometre line width. Its mill/sieve/leach results are specific to its feed and chemical route; they do not establish the Ag mass of a modern Agastya panel or the performance of a dry separator. [Dias et al., “Recycling WEEE: Extraction and concentration of silver from waste crystalline silicon photovoltaic modules,” Waste Management 57 (2016), DOI 10.1016/j.wasman.2016.03.016](https://doi.org/10.1016/j.wasman.2016.03.016).

A 2026 study on delaminated end-of-life cells cites a typical c-Si module range of 300–500 ppm and notes that residual Ag after delamination and comminution remains associated mainly with the silicon-based matrix. It also reports Ag-rich fractions across multiple size classes, showing why a screen cut alone is not an Ag assay. [Saffarian, Galvin & Firouzi, “Rethinking silver recovery pathways in end-of-life photovoltaic recycling using froth flotation,” Minerals Engineering 242 (2026), DOI 10.1016/j.mineng.2026.110189](https://doi.org/10.1016/j.mineng.2026.110189).

Therefore, use 0.30–0.63 g Ag per kg module only as an early literature-bounded sensitivity interval across different published feeds. Do not treat it as a measured Agastya feed value. Do not infer grams of silver from total mass of an Ag-bearing particle.

### Delamination and fracture

A 2026 thermal-softening experiment tested six 15 cm × 15 cm coupons per condition from a decommissioned 370 Wp monocrystalline module, after removing frame and junction box. Coupons were heated at 100 °C or 140 °C for 60 minutes and peeled at about 45 degrees with a reported 20–30 N force. The study found different residue and failure morphologies between conditions. This is a useful experimental design reference, not an Agastya setpoint: its oven, coupon, module and peel method differ from a proposed local hot-knife process. [“Effect of Temperature on the Glass Delamination in End-of-Life of Crystalline Silicon Photovoltaic Panels,” Solar (2026)](https://www.mdpi.com/3042-9242/1/1/2).

A 2025 paper describes a full-module cohesive-zone numerical delamination model and studies cell dimension and inter-cell spacing. This supports cohesive-zone modeling as a relevant mechanics class, but its output is not a validated prediction for Agastya's thermal process or material interfaces. [Meslier et al., “Numerical simulation of the delamination behavior of photovoltaic modules,” Solar Energy 300 (2025), DOI 10.1016/j.solener.2025.113792](https://doi.org/10.1016/j.solener.2025.113792).

A separate 2022 experimental study established a temperature/time relationship for thermal removal of polymers and chemically characterized glass, cell, ribbon, and residue outputs. It concerns higher-temperature polymer removal and must not be conflated with a softening-and-peel mechanism. [Dobra, Vollprecht & Pomberger, “Thermal delamination of end-of-life crystalline silicon photovoltaic modules,” Waste Management & Research 40 (2022)](https://doi.org/10.1177/0734242X211038184).

### Particle separation

A 2023 electrostatic-separation study by Li et al. on mechanically crushed waste c-Si panels reports silicon recovery: for a 0.30–0.45 mm powder fraction it reports a best condition at 15 kV and 30 rpm, with 91.0% Si proportion and 48.9% Si recovery. These are not Ag recovery values. A separate 2023 study by de Souza & Veit reports qualitative co-concentration of Ag, Al and Si in PV scrap, but the accessible abstract does not provide a mass-weighted Ag recovery or product grade. Do not substitute the Li silicon metrics for silver or treat the other study as silver-selective. [Li et al., Journal of Cleaner Production (2023)](https://doi.org/10.1016/j.jclepro.2023.137908); [de Souza & Veit, Circular Economy (2023)](https://doi.org/10.1016/j.cec.2023.100027).

A 2026 experimental study applied rougher flotation to delaminated, crushed cells. It reports 97.55 ± 0.03% Ag recovery and an upgrade factor of 32.2 ± 2.3 in tap water; a rougher-cleaner example reports about 47 wt% Ag concentrate at 86.5% recovery. Its tests used a 0.5 L mechanical cell, then 1 L tests, prepared feed with a 2 mm top size and further ground material with measured d80 of 103 micrometres. This is a direct silver-beneficiation comparator, not an Agastya result or a no-reagent process. [Saffarian et al. (2026), DOI 10.1016/j.mineng.2026.110189](https://doi.org/10.1016/j.mineng.2026.110189).

A 2022 crush-and-sieve study found silver enrichment in its finest studied fraction, while also reporting strong feed- and category-dependence. Its result supports screening as a preparation or preconcentration step, not as proof that all panels or feeds place a fixed fraction of Ag in fines. [Sim et al., “A facile crush-and-sieve treatment for recycling end-of-life photovoltaics,” Waste Management 150 (2022)](https://doi.org/10.1016/j.wasman.2022.11.023).

**Preliminary technical conclusion:** keep electrostatic separation as the charter's Stage 3 candidate, but benchmark it against at least a non-electrostatic route. Literature currently gives stronger direct silver-recovery evidence for flotation than for electrostatic separation of an Ag-bearing PV feed. The best route depends on measured Stage 2 feed liberation, composition, and test-scale assay; no approach has been selected as proven.

## 3. Preliminary inventory and uncertainty

The accompanying preliminary material inventory CSV contains a one-kilogram literature composition scenario and explicit unknowns. One review reports a composition breakdown with about 0.03 wt% Ag (300 ppm); this is a secondary-source scenario, and the original sample population, denominator and provenance have not been resolved. It is not a typical-value claim or the bill of materials for an AGASTYA panel. The component entries sum to 97.53%; the 2.47% remainder stays unassigned. [Mulazzani et al., Energies 15 (2022)](https://doi.org/10.3390/en15228419). A separate Dias et al. study reports 600 g/t in its publisher abstract, while 630 g/t is found in secondary conclusion excerpts; that discrepancy and denominator are unresolved, so neither value is used as a verified AGASTYA feed value.

At a 1 kg normalization, that scenario corresponds to 720 g glass, 150 g Al, 70 g polymer, 25 g Si, 8 g Cu, 0.3 g Ag, 1 g Sn, 1 g Pb, and 24.7 g unassigned. A separate published study reported 0.63 g Ag/kg for its modules. Keep these as separate literature references; do not combine measurements from different panel populations into one supposedly measured panel.

No material stream is yet weighed. Stage 1 removal efficiencies, Stage 2 liberation fractions, Stage 3 partitioning, Stage 4 assay concentrations, mass losses, and process yields are blank/unknown. No particle size distribution has been measured for an Agastya feed. The published d80 and sieve classes cited above are reference feed conditions only.

Use traceable stream IDs once a real feed is registered, for example: PV-001 (parent panel), PV-001-S1-GLASS, PV-001-S1-FRAME, PV-001-S1-LAMINATE, PV-001-S2-COARSE, PV-001-S2-FINES, PV-001-S3-CONCENTRATE, PV-001-S3-REJECT, and PV-001-S4-ALIQUOT-01. Store parent ID and split/merge links so mass is not double-counted.

For each stage, calculate:
- Total mass closure = sum of output stream masses + documented losses, compared with input mass.
- Silver stage recovery = 100 × Ag mass in target output / Ag mass entering that stage.
- Silver overall recovery = 100 × Ag mass in final product / Ag mass in original feed.
- Concentrate Ag grade = 100 × Ag mass in concentrate / total concentrate mass.
- Balance residual = input mass − outputs − documented losses. Report this residual; do not force it to zero.

If assay values are reported as concentration, compute Ag mass using the sample/stream dry mass and the laboratory's method basis. Include replicate/aliquot uncertainty and sampling error. Do not call elemental grade “chemical purity” unless the final product is a refined, identity-confirmed Ag product and a suitable purity method has been used.

## Candidate governing equations and model boundaries

The following equations define model classes and data needs; they are not solver results.

- **Stage 1 component inventory:** for component i, the first estimate is mᵢ = fᵢ m_module, where fᵢ is a sourced or measured mass fraction. Routing to stream j is mᵢⱼ = rᵢⱼ mᵢ, with the routing fractions rᵢⱼ measured or explicitly assumed and summing to one only when no losses/unaccounted material exist. Current Agastya fᵢ and rᵢ are unknown.
- **Stage 2 liberation:** applied stress can be represented as σ = F/A for a simple loading screen; fragment/libration prediction requires material fracture strength, interfacial adhesion, load path and a fracture/discrete-element model. No Agastya fracture or liberation data are available. A particle mass or size cut cannot be used as Ag mass.
- **Optional thermal delamination pretreatment:** transient solid heat conduction follows ρcₚ ∂T/∂t = ∇·(k∇T) + Q̇. A peel/debond model additionally needs a traction-separation relation T(δ,T) and interface energy Gc(T) = ∫T dδ. Thermal field alone does not calculate peel quality. MOOSE documents coupled heat and solid mechanics and cohesive-zone capabilities, but its generic examples do not provide PV/EVA properties. [MOOSE heat/mechanics tutorial](https://mooseframework.inl.gov/moose/modules/combined/tutorials/introduction/thermomech_step01.html), [MOOSE cohesive-zone documentation](https://mooseframework.inl.gov/releases/moose/2024-11-11/syntax/Physics/SolidMechanics/CohesiveZone/index.html).
- **Stage 3 electrostatics:** a field solution may use ∇·(ε∇V) = −ρᶠ and E = −∇V for the specified material and boundary conditions. For already charged particles, a trajectory balance can use mₚ dv/dt = qE + F_contact + F_drag + mₚg + F_other. Conductivity, tribocharge, polarization/induced forces, particle contacts and dielectric breakdown may require additional constitutive models. No field geometry, feed charge, electrical properties, or separator settings are known. Maxwell calculates field solutions; Rocky product documentation describes particle dynamics under electromagnetic fields/coupling, but the student-module entitlement and exact data handoff are unverified. [Maxwell FEM overview](https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v251/en/Subsystems/Maxwell/Content/Maxwell/Maxwell3DTechnicalNotes.htm), [Rocky coupling overview](https://www.ansys.com/en-in/products/fluids/ansys-rocky).
- **Stage 4 accounting:** total-mass residual = m_in − Σm_out − m_documented_loss; Stage Ag recovery = 100 m_Ag,target/m_Ag,in; overall recovery = 100 m_Ag,final/m_Ag,initial; concentrate Ag grade = 100 m_Ag,concentrate/m_concentrate. These formulas require representative assay-derived Ag mass and measured stream mass; no Stage 4 Agastya values exist.
## 4. Software selection and access plan

The accompanying software access matrix CSV records official capabilities, deployment and access caveats. None of these tools has been authenticated in a user account or run for the new architecture.

| Tool | Best fit | Cloud/local and student/no-GPU relevance | Agastya limitation |
|---|---|---|---|
| CPython + NumPy | Component inventories, mass balance, uncertainty, parameter sweeps | Already present locally; CPU-only calculations do not require a GPU | Not a fracture, electrostatic-field or chemistry solver by itself |
| Google Colab | Reproducible notebook calculations and plots | Browser-based; free GPU availability is dynamic and not guaranteed | Not a licensed FEM/DEM engine; sessions/resources are variable |
| Onshape Education | Conceptual CAD and exploded assembly | Browser-based; Student plan is free for eligible education users; no local GPU | Student plan is CAD; Simulation appears on the Educator plan. Account eligibility/access is not confirmed |
| SimScale | Browser-based structural, thermal, CFD and selected electromagnetics | Cloud solver; Community is free for limited testing/learning, with analysis and result limits | Current plan does not establish that cohesive-zone or particle-liberation physics needed here is accessible |
| Ansys Student (Rocky and Maxwell inclusions) | Small DEM/particle and electromagnetic-field studies | Windows installation, not browser cloud; free for educational use, no Rocky GPU, 32,000 particle cap and four CPU cores | Student access is conditional on educational use; coupled module entitlement, geometry transfer and Ag-specific parameters need confirmation |
| Aspen Plus academic | Flowsheet mass/energy/process economics after route selection | Academic offering is institution/license based; not assumed free to an individual | Cannot supply missing silver-recovery kinetics or validate a chemistry route by itself |
| MOOSE | CPU-based heat/solid mechanics and cohesive-zone research model | Open-source; supports Linux, WSL and Conda prebuilt installation; no dedicated GPU required for a small model | Requires a solver installation/user; an Agastya-specific traction-separation law and material data are still required |

**Recommended access sequence:** keep local Python/NumPy as the reproducible backbone. Use browser CAD only after the panel and separator geometry are known. For a small educational DEM/field feasibility study, check the actual Rocky/Maxwell student entitlements and verify whether the needed coupling modules are included. For heat-plus-fracture delamination, MOOSE is the most transparent no-GPU open-source candidate identified; SimScale is suitable for simpler cloud thermal/structural screening only if the selected plan supports the needed analyses. Aspen Plus is deferred until a chemical or process flowsheet has a defined route and measured inputs. Do not purchase or request access until account/eligibility and sample needs are settled.

The formats in an eventual run must be recorded from the actual version/account. The working interchange proposal is STEP for CAD geometry and CSV/JSON for material, assay and numerical tables; this is a project interoperability proposal, not a claim that every vendor's student plan exports every format. For any Maxwell-to-Rocky handoff, verify field-map import format and license entitlement before designing the coupled study. SimScale numerical download/export and project privacy must also be checked in the account before using it for reproducible work.

## 5. Sample size and validation plan

**Current Agastya physical sample count:** zero documented panels, zero Stage 3 coupons, zero Stage 2 particle lots, and zero assay aliquots/results.

Published design anchors, not Agastya allocations:
- Thermal glass-peel study: n = 6 independent 15 cm × 15 cm coupons per condition from one decommissioned 370 Wp module, oven heating at 100 or 140 °C for 60 minutes.
- Silver-flotation study: 3.5 kg homogenized crushed-cell feed prepared with a 2 mm top size before wet milling; 0.5 L and 1 L cell studies.
- Electrostatic silicon study: 0.30–0.45 mm feed class; this does not define silver-bearing particle size or a required sample mass.

A defensible Agastya test count must follow the available panel count, material heterogeneity, intended statistical comparison, assay method precision, and supervisor/facility requirements. Replicate aliquots should be selected after homogenization and a sampling plan is agreed with the assay lab. A single assay or many subsamples from one panel does not represent between-panel variability.

Validation order:
1. Register panel identity/source, module datasheet, condition, cell type, mass and dimensions.
2. Document Stage 1 mass measurements and repeatability; retain parent-child stream IDs.
3. Characterize Stage 2 feed with sieve analysis, representative microscopy/EDS or equivalent material ID, and a validated bulk Ag assay.
4. Measure Stage 3 feed conductivity/charge behavior, moisture, size, shape and density; characterize field geometry and splitter settings.
5. Assay every output and tailings stream using a lab-approved, representative method; calculate closure and uncertainty.
6. Compare model predictions with measured mass partition and Ag assay. Refit only with recorded calibration data and reserve independent samples for validation.

## 6. Public laboratory and sample leads

Public facility pages identify possible leads, not available Agastya resources:
- CSIR-CMERI Durgapur describes PV recycling and process-plant development/validation activity. It is a possible process-partner lead; the page does not promise Agastya feed, equipment access, or supervised trials.
- C-MET Hyderabad describes a developed c-Si PV recycling technology and has a public expression of interest for technology transfer through 31 December 2026. This is a technical partnership lead, not confirmation of sample or lab access.
- The CPCB E-Waste portal hosts waste-PV rules/guidance and recycler registry functions. It is a route for identifying a registered channel, not proof that any listed recycler will supply research samples.
- CSIR-CGCRI Kolkata lists analytical facilities including ICP-MS/ICP-AES and XRF and accepts testing enquiries. The precise Ag method, sample mass, preparation, limits, uncertainty, fee, turnaround, and external-user access must be confirmed.
- STQC ERTL(East), Kolkata lists PV module testing/calibration services. This may support module characterization; it does not establish Ag assay or delamination capability.
- NISE lists PV module, cell and materials characterization services. This is a national PV-test lead, not evidence of Agastya access or Ag assay.

No institution has been contacted, no sample donor is confirmed, and no samples have been promised. See the [physical test readiness register](../REAL_TEST_READINESS.md) and [resource inventory and leads](../resource_inventory_and_leads.csv) for the detailed lead status. The Kolkata/Durgapur shortlist is a geographic hypothesis from the existing project context, not a confirmed user location.
## 7. Missing specifications and assumptions to resolve

The accompanying missing-specifications CSV is the intake checklist. The most important gates are:
- Actual module donor/owner, sample ID/count, technology (mono/poly, PERC/TOPCon/HJT if known), construction (glass-backsheet or glass-glass), manufacturer/model/year, and physical condition.
- Which process in the latest charter is the final Stage 1/2/3 design; whether the existing thermal hot-knife concept is retained as an upstream pretreatment, and where it belongs in the new numbering.
- Stage 1 dismantling tools, sequence, safety controls, target stream definitions, and measured mass data.
- Stage 2 breakage mechanism, feed mass, desired particle-size window, fracture/liberation data, and allowed losses.
- Stage 3 separator geometry, electrodes, voltage/polarity, rotor/feeder/splitter dimensions, operating humidity, feed rate, charge model, and measured particle electrical/triboelectric properties.
- Assay lab, Ag method, sample preparation, detection/quantification limits, uncertainty, sample mass, calibration standards, and cost/turnaround.
- Solver account/eligibility, installed versions, usable computer/RAM/CPU/GPU, and available technical supervisor.

Pending values are represented as unknown, not filled with arbitrary “typical” assumptions. Assumptions allowed for a preliminary model must be tagged, cited, given a range, and kept separate from measured values.

## 8. Technically justified roadmap

**Phase A — complete with this baseline.** Research, preliminary inventory, software access comparison, architecture, evidence, and missing inputs are documented. The architecture crosswalk preserves the existing project record.

**Phase B — system model.** After selecting an actual module family, build its exploded CAD/stream map and one-kilogram component model. Create the data schema and a mass-balance calculator with blank yields until tests provide them. Choose the Stage 1 handling logic and Stage 2 particle classes.

**Phase C — individual models.** First validate simple models against analytically known cases. Run an uncalibrated thermal conduction model only as a thermal field calculation. Run cohesive-zone delamination only after temperature-dependent traction-separation properties or a defensible published parameter source is selected. Use Rocky/Maxwell only after module entitlement, field export/import and measured charge/property inputs are confirmed. Do not use particle dynamics as proof of microscopic Ag liberation.

**Phase D — integration.** Pass actual output masses and particle class properties between stages, preserve provenance, check kg/g units, and calculate mass and Ag closure with an explicit unaccounted stream.

**Phase E — validation.** Compare predictions with literature only where process/feed/measurement basis match; then compare with Agastya physical tests. Report validation error, uncertainty, and failed fits.

**Phase F — optimization.** Compare recovery, grade, losses, time, energy, complexity, consumables and uncertainty only after a baseline model has been validated. Electrostatic separation remains the charter's candidate. Flotation is the required literature comparator because direct Ag recovery evidence exists for it; neither is adopted based on literature yield alone.

## 9. Conclusions and evidence classes

1. Ag is present as cell metallization and in interconnect structures, but the Agastya feed inventory is not known.
2. The 0.30–0.63 g/kg literature span is adequate only for a sensitivity envelope; it is not a prior distribution and cannot substitute for assay.
3. Literature electrostatic results cited here recover a silicon-rich fraction, not a measured silver product. The claim that conductivity alone separates Ag is unsupported.
4. Direct silver-focused separation evidence currently favors testing flotation as a comparator to electrostatic concentration; the published performance is feed- and method-specific.
5. A thermal-assisted interface peel and high-temperature polymer removal are different processes. They require separate stage definitions and material/process models.
6. A credible integrated Agastya result cannot yet be produced because the feed composition, Stage 2 liberation, Stage 3 separator parameters/particle properties, lab assay and software entitlements are absent.

Evidence labels for all new records:
- **Established/structural:** c-Si modules include glass, encapsulants, cells, interconnects, frame and electrical hardware; cell contacts contain Ag.
- **Published experimental:** the numbers cited above, tied to their study samples and test methods.
- **Assumed/scenario:** the one-kilogram composition listing and any future sensitivity ranges.
- **Simulated:** none newly produced in this Phase A baseline.
- **Experimentally measured for Agastya:** none.

19. CSIR-CMERI PV recycling activity: https://www.cmeri.res.in/department/coe-centre-excellence-waste-processing-segregation-technologies
20. CSIR-CGCRI analytical facilities: https://www.cgcri.res.in/research/research-support-divisions/4m-division/4m-divisional-facilities/
21. STQC ERTL(East), Kolkata: https://stqc.gov.in/ertle-kolkata
22. NISE PV module testing: https://nise.res.in/departments/pv-module-systems-bos-testing
23. C-MET c-Si PV recycling technology / EOI: https://www.cmet.gov.in/node/4025
24. CPCB E-Waste Management System: https://eprewaste.cpcb.gov.in/
25. EPA SW-846 Method 6200 (XRF): https://www.epa.gov/hw-sw846/sw-846-test-method-6200-field-portable-x-ray-fluorescence-spectrometry-determination
26. EPA SW-846 Method 6010D (ICP-OES): https://www.epa.gov/hw-sw846/sw-846-test-method-6010d-inductively-coupled-plasma-optical-emission-spectrometry-icp-oes
27. EPA SW-846 Method 6020B (ICP-MS): https://www.epa.gov/hw-sw846/sw-846-test-method-6020b-inductively-coupled-plasma-mass-spectrometry
## 10. References and official software documentation

1. Dias et al. (2016), DOI: https://doi.org/10.1016/j.wasman.2016.03.016
2. Saffarian et al. (2026), DOI: https://doi.org/10.1016/j.mineng.2026.110189
3. Chen et al. (2026), Solar: https://www.mdpi.com/3042-9242/1/1/2
4. Meslier et al. (2025), DOI: https://doi.org/10.1016/j.solener.2025.113792
5. Dobra et al. (2022), DOI: https://doi.org/10.1177/0734242X211038184
6. Sim et al. (2022), DOI: https://doi.org/10.1016/j.wasman.2022.11.023
7. Published c-Si composition scenario, Energies 15 (2022): https://doi.org/10.3390/en15228419
8. SimScale documentation: https://www.simscale.com/docs/ and pricing: https://www.simscale.com/product/pricing/
9. Ansys Student terms/capabilities: https://www.ansys.com/en-in/academic/students/ansys-student
10. Rocky system requirements: https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/dem_ug/system-requirements.html
11. Rocky-Maxwell coupling overview: https://www.ansys.com/en-in/products/fluids/ansys-rocky
12. Maxwell FEM capabilities: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v251/en/Subsystems/Maxwell/Content/Maxwell/Maxwell3DTechnicalNotes.htm
13. AspenTech academic program: https://www.aspentech.com/en/academic-program-for-education
14. Onshape education plans: https://www.onshape.com/en/education/plans
15. Google Colab resource limits: https://research.google.com/colaboratory/faq.html
16. MOOSE coupled thermal-mechanics: https://mooseframework.inl.gov/moose/modules/combined/tutorials/introduction/thermomech_step01.html
17. MOOSE installation requirements: https://mooseframework.inl.gov/getting_started/installation/index.html
18. MOOSE cohesive-zone model: https://mooseframework.inl.gov/releases/moose/2024-11-11/syntax/Physics/SolidMechanics/CohesiveZone/index.html
