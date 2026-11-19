# Targeted literature review — 13 October 2026

## Scope and method

This update focuses on current AGASTYA's c-Si disassembly, mechanical liberation/classification, electrostatic separation, and sampling/assay boundary. It prioritizes primary research abstracts and official method/software documentation. The Phase B/C source register remains the broader literature base; this review adds or requalifies directly relevant studies. Access is not equivalent to full-text review: where only an abstract or metadata page was available, that limit is recorded. Sources and claim-level limitations are in [Evidence_Register.csv](Evidence_Register.csv).

## Direct electrostatic evidence

Yang et al. (2019) is the most direct located study of electrostatic separation of Ag and Si from waste crystalline-silicon solar cells. Its official journal abstract describes a needle-roll separator and reports 94.37% “silver separation efficiency” and 78.58% silicon separation efficiency at an 80° corona-electrode angle, 80 mm electrode spacing, 27.5 kV, and 90 rpm. The abstract does not define the reported efficiency, state the full feed/output Ag balance, or make its feed preparation/size distribution transparent. Treat the number as a paper-reported metric, not a directly comparable mass-weighted recovery, not a grade, and not an AGASTYA expectation.

de Souza and Veit (2023) mechanically processed polycrystalline Si-C PV scrap, size-separated it, then used electrostatic separation. The accessible abstract reports that 49.22% of the material mass fell below 0.5 mm and that at 38 kV and 75 rpm the separator co-concentrated silicon, silver, and aluminum. This supports testing a characterized, size-conditioned feed. It also cautions that co-concentration is plausible: elemental Ag selectivity cannot be inferred from a silver-bearing fraction. The accessible abstract does not provide a mass-weighted Ag recovery, product grade, or complete balance.

Younes et al. (2013) modeled and tested a roll-type corona separator for PVC/Cu cable-waste particles. The paper identifies conductivity, particle size, speed, humidity, and spark events as factors that can change field and trajectory; model distribution results agreed with experiments for their PVC/Cu setup. It is a useful model-form and instrumentation analogue, not PV validation or a source of Ag-specific parameters.

Taken together, these sources justify a **testable hypothesis**, not a current process-performance estimate. A future AGASTYA model needs measured particle class, shape, moisture, conductivity/charge behavior, field geometry and operating conditions, then validation against observed bin distributions and assays. Fitting one separator's optimal voltage to a different feed would not close these gaps.

## Mechanical liberation and silver partition

Sim et al. (2022) report that up to 70% and 80% of total Ag was in the finest F4 fraction for two studied PV feed categories (EVAc and MP). This is a size-partition result on those feeds, not 70–80% recovery for AGASTYA and not a product-grade statement. Juyo Salazar et al. (2024) is recorded in the project literature as reporting 94.12% of Ag in a <0.25 mm fraction for its own polycrystalline feed; the exact feed definition and mass-balance basis should be checked in the full paper before reusing that value. Both support collecting complete size-fraction mass and assay data in Stage 2. A sieve cut alone establishes size, not that Ag contacts are liberated or selectively captured.

Cell metallurgy also changes with module generation. c-Si cells use printed Ag front contacts and interconnect structures, with narrow printed features and composition/process variations; particles can remain bonded to Si and can include Al/Cu-bearing components. Therefore Stage 2 should distinguish size fraction, particle identity, and liberation/association rather than assume “fine” equals free silver.

## Feed-grade values and denominators

The project has retained three non-equivalent reported bases: 300 ppm from a 2022 secondary review scenario with denominator/source provenance unresolved; 600 g/t from Dias et al.'s publisher abstract for its studied material; and 630 g/t appearing in a secondary excerpt whose relation to the Dias value is not resolved. On a normalized one-kilogram basis these are 0.300, 0.600, and 0.630 g Ag. The arithmetic is useful for checking units, but these values must not be combined into a confidence interval or assigned to an unassayed AGASTYA module. The Dias study also reports a concentration yield affected by pyrolysis; that process and metric do not transfer to AGASTYA's current stages.

## Optional thermal delamination

Saitta et al. (2026) reports oven exposures of 100°C or 140°C for 60 minutes followed by manual peeling on six samples per condition. In the tested material, 140°C gave smoother separation but thicker residue; 100°C gave more fragmented/incomplete separation. Thermal analysis and FTIR characterize that study's polymer behavior. These data do not validate the AGASTYA hot-knife/roller concept, a sub-minute cycle, complete EVA removal, or current Stage 3. Thermal delamination remains an optional pretreatment between current Stages 1 and 2.

## Downstream enrichment and chemical boundary

Saffarian et al. (2026) reports high recovery and enrichment in a bench flotation study of prepared/delaminated/ground PV feed using reagents; its best rougher result is reported as 97.55±0.03% Ag recovery, with a separate cleaner condition reporting 46.7±1.5 wt% Ag at 86.5±2.8% recovery. This is evidence that downstream concentration can depend on feed preparation and chemistry. It is not a dry separation model, not a silver-purity result, and not in AGASTYA's current boundary. Its percentages should only be quoted with their feed/route and stage-specific conditions.

## Sampling, assay and accounting

The Stage 4 output is an auditable balance, not a refining process. EPA SW-846 methods 6010D and 6020B provide ICP-OES and ICP-MS analytical guidance; method 6200 addresses field-portable XRF for soil/sediment. None is automatically validated for PV powder. A qualified laboratory must agree sample preparation/digestion, matrix spikes, blanks, duplicates, reference materials, reporting limits, and uncertainty for the actual Ag-Si-glass-polymer-metal matrix. XRF can screen elemental composition but does not by itself determine silver chemical phase or establish recovered-metal purity.

Use actual measured stream masses and assays. Report mass yield, Ag grade, Ag recovery, enrichment, mass residual, Ag residual, and uncertainty separately. Preserve sample identity and split lineage. Do not force closure by assigning unknown losses or treating missing streams as zero.

## Macro context

Wang et al. (2026) provide a global end-of-life PV material-flow scenario, estimating 297–402 Mt of waste by 2060 under its scenarios. That supports the importance of the broader waste-management problem but cannot establish AGASTYA's technical, economic, or environmental performance. The paper's macro scenarios should not be used to support unsupported per-module Ag-value or process-recovery claims.

## Research conclusions

1. A current AGASTYA numerical Stage 1–3 prediction is not identifiable from the workspace: physical feed, geometry, operating conditions, particle properties, and assays are missing.
2. A staged, replicated benchtop experiment is the priority. First establish feed identity, mass, particle-size distribution, and assay; then test a range of separator conditions with full stream accounting.
3. The next solver decision depends on the experiment. Particle tracing is potentially useful after geometry, charge, and force data exist; it cannot replace those measurements. A custom coupled model would require validation on this material and hardware.
4. The highest-priority research gap is not compute: it is the absence of representative feed and validated stream data.
