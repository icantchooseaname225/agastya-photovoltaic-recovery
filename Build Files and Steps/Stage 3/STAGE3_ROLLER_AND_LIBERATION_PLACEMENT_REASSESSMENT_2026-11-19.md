# Stage 3 hot-knife, foam-roller, and liberation placement reassessment

**Reviewed:** 19 November 2026  
**Status:** evidence review; no integrated hot-knife/foam-roller station or liberation trial is documented.

## Scope and reconciliation

The current project instruction sets the Stage 3 concept as hot-knife separation followed by a foam roller, then asks whether mechanical liberation should occur immediately after those operations. Older local build notes describe a guarded hot knife and treat the roller as a later, unvalidated study. This reassessment records the new foam-roller direction while preserving the earlier notes as a truthful record of the previous design state.

The local Stage 3 simulation is a thermal conduction model for layered PV materials. It does not include foam, roller contact mechanics, peel/fracture behaviour, adhesive removal, particle liberation, dust, or measured machine energy. There is no roller material, temperature rating, diameter, hardness, line load, speed, nip geometry, or cleaning specification in the current Stage 3 package. The foam-roller concept is therefore a design input for research, not a tested or fully specified component.

## Evidence on process order

The IEA PVPS 2025 report describes an industrial Japanese line that performs automated junction-box removal and de-framing, hot-knife treatment of unbroken modules, and then shredding of the laminate followed by sorting. Its flow supports placing mechanical size reduction downstream of thermal glass separation as a coherent material sequence. It does not report a comparison proving that a foam roller should be used, or that locating the shredder in Stage 3 is cheaper or performs better than a separate Stage 4 station. [IEA PVPS T12-31:2025](https://doi.org/10.69766/XLFG7020).

## Recommendation

**For physical process layout, carry a modular, contained mechanical-liberation module immediately after the hot-knife/foam-roller outlet as the leading arrangement to evaluate.** This follows the documented industrial sequence and can avoid transporting a still-laminated sheet to a remote liberation station.

**Keep the formal Stage 3/Stage 4 assignment conditional until the outlet feed is measured.** The stage label itself does not change the material balance or the machine energy. Co-location could reduce transfers, but may increase guarding, dust capture, cooling, contamination control, and maintenance around the thermal cell. It has not been demonstrated that those costs balance out.

A suitable provisional sequence is:

```text
Stage 2 robotic disassembly
  → Stage 3 hot knife
  → Stage 3 foam roller (role and parameters to be defined)
  → controlled cooling and separate glass/laminate collection
  → modular, enclosed liberation interface
  → Stage 4 size classification and silver-selective concentration/recovery
```

If the thermal outlet can already be accepted by the selected Stage 4 separation route, the liberation module can remain bypassed. If the Stage 3 outlet requires fine grinding, do not treat a coarse shredder as adequate liberation; define the required particle-size and silver-exposure endpoint from that route's feed specification.

## Tradeoffs to measure

| Potential benefit of adjacent liberation | Potential cost or failure mode |
|---|---|
| Fewer intermediate transfers and less manual handling of a large laminate | Dust and mixed glass/polymer/cell fines near the hot process; needs an enclosed collection interface |
| Direct routing of a defined cell-bearing feed to Stage 4 | Foam/adhesive wear debris or residual EVA may contaminate the liberated fractions |
| Compact continuous material flow | A jam, broken glass event, or cleaning outage can stop both thermal and liberation operations |
| One traceable batch lineage from module through size fractions | Liberation can destroy glass sheet quality or spread silver-bearing fines into untracked dust |

The foam roller requires a separate controlled comparison of roller/no-roller conditions. Record material, temperature, diameter, compression, line load, speed, transfer delay, energy, output quality, contamination and wear. These variables cannot be inferred from the existing hot-knife-only model.

## Validation gate before permanently moving liberation

On matched, traceable material, compare the same thermal treatment with liberation at the adjacent outlet versus a separate downstream station. Weigh all streams, including dust and cleaning residue; measure size distribution and particle morphology; assay Ag, Si, Al, Cu and relevant solder metals in every principal fraction; record residual glass/polymer and foam debris; meter energy and time for both layouts; and document maintenance/jam events. Only then compare handling, retained silver, product grade, throughput, and total cost per accepted module.

## Decision status

The evidence supports **testing** post-thermal liberation as an adjacent modular operation. It does not justify deleting Stage 4 feed-preparation capability or claiming improved recovery, less equipment, lower cost, or reduced contamination. The Stage 3 boundary remains provisional until feed quality and integration are measured.

## Reference

Agraffeil, C. et al. (2025), *Status of PV Module Recycling in IEA PVPS Task 12 Countries*, IEA PVPS T12-31:2025, Japanese Hamada Corporation line, process-flow description. [DOI](https://doi.org/10.69766/XLFG7020).
