# AGASTYA Technical Research Dossier

**Report ID:** AG-R01  
**Version:** 1.0 | **Prepared:** 13 October 2026  
**Evidence boundary:** Project-file audit, source review, deterministic calculations and numerical model studies. No physical AGASTYA material was processed or assayed.

## Executive summary

AGASTYA investigates recovery of silver-bearing material from end-of-life crystalline-silicon (c-Si) photovoltaic modules. Its current four-stage architecture is: (1) disassembly and component routing, (2) mechanical liberation and classification, (3) candidate electrostatic separation, and (4) representative sampling, assay and accounting. The silver-bearing fraction leaving these stages is not refined silver. Optional hot-knife delamination belongs upstream of Stage 2; older project documents retain their historic stage labels and are not silently relabeled.

The repository contains substantial scenario calculations, an assumed thermal model and a guarded accounting kernel. None is an AGASTYA process measurement. No traceable panel lot, measured stream mass, validated Ag assay, electrostatic separator geometry, or independently validated process model was found. Consequently, feed grade, recovery, concentrate grade, purity, throughput, energy, environmental benefit and economics remain unknown.

This phase adds a balanced main-effect variance decomposition over the historical 5,040-case thermal sweep and a spatial-refinement study for an optional hot-knife pretreatment. The sweep identifies dwell time and contact conductance as the largest main effects for its modeled outputs. Spatial refinement raises predicted EVA contact-side peak temperatures materially relative to the five-node approximation, demonstrating model-resolution sensitivity. These are deterministic calculations over selected assumed inputs, not empirical validation or probabilistic uncertainty.

## 1. Problem definition and scope

The engineering question is whether a measured c-Si module feed can be routed and processed into a well-characterized Ag-bearing fraction with a defensible material balance. Silver is printed as fine cell-contact metallization and is physically attached to composite cell fragments before liberation. PV cell architectures, metallization layouts, module generations, and Ag usage change over time; manufacturer consumption statistics therefore cannot substitute for assay of an end-of-life feed. Hallam et al. document large technology-dependent differences in reported 2020 silver consumption per watt, including PERC, TOPCon and SHJ cells ([Hallam et al., 2023](https://onlinelibrary.wiley.com/doi/10.1002/pip.3661)).

The project boundary ends at measured streams and the Stage 4 assay/accounting record. Chemical silver dissolution, precipitation, smelting, refining, and saleable-metal production are outside the current architecture. A downstream receiver may be evaluated later, but it must be represented as a separately defined process.

## 2. Current four-stage process

{{FIGURE:process}}

| Stage | Current operation | Main evidence needed | Current status |
|---|---|---|---|
| 1 | Identify the module; disassemble and route frame, box/cables, glass, cell-bearing laminate and losses | Traceable feed lot, verified component masses, Ag partition if claimed | Process specification only |
| 2 | Contained mechanical liberation and classification | Equipment/settings, particle-size distribution, all stream masses, Ag association/liberation | No AGASTYA run data |
| 3 | Candidate electrostatic separation of characterized particles | Geometry, field/voltage, feed properties, humidity, run replicates, all bin masses and assays | Literature-supported hypothesis; no separator model or trial |
| 4 | Representative sampling, laboratory assay and reconciled accounting | Sampling plan, validated preparation/assay, QA/QC, uncertainty and sample lineage | Formula/template level only |

Published electrostatic PV studies show that the concept merits controlled testing, but their reported values do not transfer directly. Yang et al. report 94.37% “silver separation efficiency” for a needle-roll study at specified settings, but the accessible abstract does not define the metric or disclose a complete mass balance ([Yang et al., 2019](https://xbzrb.hbu.edu.cn/CN/abstract/abstract4632.shtml)). de Souza and Veit report co-concentration of Si, Ag and Al under their tested conditions; this is evidence against assuming elemental selectivity from a dry separator ([study record](https://doi.org/10.1016/j.cec.2023.100027)).

## 3. Material inventory and silver basis

The Phase D ledger retains three separate literature-derived cases on a normalized 1 kg basis: 300 ppm gives 0.300 g Ag; 600 g/t gives 0.600 g; and an unresolved secondary 630 g/t value gives 0.630 g. These values have different source and denominator provenance. They are neither a pooled range nor an assay of AGASTYA feed. Module construction also includes front glass, two encapsulant layers, cells, interconnect ribbons, solder, backsheets, frame, junction box and cables; material fractions vary by construction and generation. The composition scenario's 2.47% unassigned remainder is retained explicitly.

Silver must be tracked by stream as mass, not inferred from fines or concentrate mass. For measured stream `i`, `m_Ag,i = M_i x_Ag,i`. Stage recovery is the target-stream Ag mass divided by Ag mass entering that stage. Product grade is Ag mass divided by total product mass. Mass yield, grade, recovery, enrichment, purity and balance closure are distinct metrics.

## 4. Thermal and chemical context

The inherited thermal model concerns an optional hot-knife-like pretreatment; it does not represent current Stage 3 electrostatics. The original five-node one-dimensional model predicts sensible temperature changes in glass/EVA/cell/EVA/backsheet layers using assumed properties, a fixed-temperature blade boundary, conduction, and outer convection/radiation. It does not model EVA decomposition kinetics, adhesion loss, fracture, moving contact, volatile emissions, or actual material separation.

The new sensitivity and mesh studies show that dwell and contact conductance dominate the main-effect shares within the specified grid, and that the coarse five-node representation under-resolves the modeled contact-side temperature gradient. Literature on thermal degradation at furnace conditions, including treatment up to 600 °C, cannot validate a hot-knife contact model. A 2023 IEA PVPS hot-knife LCA used pilot-plant inventory data and treated glass/laminate delamination as a distinct operation; its system boundary does not establish AGASTYA Ag recovery ([Frischknecht et al., 2023](https://iea-pvps.org/wp-content/uploads/2023/07/Report_IEA-PVPS_T12-25-2023_LCA-PV-Recycling-Hot-Knife.pdf)).

## 5. Integrated material and energy accounting

No measured integrated balance can currently be assembled. Stage 1 requires identified component masses and documented loss streams. Stage 2 requires all class and dust masses plus particle characterization. Stage 3 requires every collected fraction, including middlings and rejects. Stage 4 requires representative assays and the lab's preparation/QA record. Unknown terms must remain unknown; no balancing plug or zero substitution is allowed.

The legacy thermal sweep reports energy per assumed contact area, not measured equipment energy. Its result excludes blade heat capacity, machine warm-up, drive power, actual panel geometry and electrical losses. The Stage 4 accounting code demonstrated arithmetic and null propagation on normalized reference cases and synthetic software-check fixtures; those checks establish code behavior only.

## 6. Findings, limitations and decisions

1. **Established:** the current process definitions, source-specific literature arithmetic, and explicit data gaps are documented in Phase D.
2. **Established computationally:** a 5,040-case deterministic thermal sensitivity decomposition; a 20-case 1–16 cells-per-layer spatial refinement; one-cell-per-layer replication of the historical model at the same timestep; and numerical energy closure for the refined model.
3. **Not established:** any AGASTYA material recovery, assay, grade, purity, equipment performance, environmental benefit or economic feasibility.
4. **Model implication:** a better-resolved thermal model can materially change predicted local EVA temperature. This warrants characterization only if thermal delamination is retained as a design option.
5. **Research priority:** obtain a documented c-Si feed lot, confirm representative sampling and matrix-valid assay, and measure Stage 1/2 streams before attempting a calibrated electrostatic model.

## References

- Frischknecht, R., Komoto, K. & Doi, T. (2023). *Life Cycle Assessment of Crystalline Silicon Photovoltaic Module Delamination with Hot Knife Technology*. IEA PVPS T12-25:2023. [Report PDF](https://iea-pvps.org/wp-content/uploads/2023/07/Report_IEA-PVPS_T12-25-2023_LCA-PV-Recycling-Hot-Knife.pdf).
- Hallam, B. et al. (2023). The silver learning curve for photovoltaics and projected silver demand for net-zero emissions by 2050. *Progress in Photovoltaics*. [DOI](https://doi.org/10.1002/pip.3661).
- Yang, X. et al. (2019). Electrostatic separation of silver and silicon in waste crystalline silicon solar cells. [Journal abstract](https://xbzrb.hbu.edu.cn/EN/10.3969/j.issn.1000-1565.2019.03.004).
- Shang, Y. et al. (2026). Kinetic characteristics and emission reduction potential of gaseous pollutants during thermal treatment of decommissioned photovoltaic modules with different encapsulants. *Journal of Environmental Chemical Engineering*. Abstract reviewed. [DOI](https://doi.org/10.1016/j.jece.2026.121479).
