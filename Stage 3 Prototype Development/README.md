# AGASTYA Stage 3 — Thermal Prototype Development

**Updated:** 16 October 2026  
**Current definition:** Stage 3 is thermal treatment/delamination. Stage 4 is silver removal/recovery. See the [current architecture](../AGASTYA_ARCHITECTURE.md).

This package now reviews a guarded hot-knife thermal separation concept. The dated 14 October electrostatic package was based on an incorrect stage map and is preserved in [the archive](../99_Archive/Stage3_Electrostatic_Package_2026-10-14/); do not use its BOM, costs, recommendations, or generated documents as current Stage 3 guidance.

## Working Stage 3 boundary

The current baseline is front-glass separation from a prepared crystalline-silicon module. The first expected outputs are sheet glass plus a cell/EVA/backsheet laminate. This does not establish EVA-free cells or silver liberation. A proposed heated roller is a separate, unvalidated question; it should not be included in the first prototype until its target output is defined.

The recommended development path is cold fixture and workflow review first, followed by supervised, instrumented coupon work using an approved thermal station at a qualified facility. Active heating requires review of the actual machine, feed, electrical protection, guarding, ventilation, emergency response, and waste plan by the responsible facility. No household appliance, open flame, improvised reactor, or unreviewed heater is suitable.

## Source-controlled technical material

- [Stage 3 decision report](Stage_3_Decision_Report.md) and [architecture reconciliation](ARCHITECTURE_RECONCILIATION.md).
- [Editable architecture decision SVG](Figures/Stage_3_Architecture_Decision.svg).
- [Document and workbook source generators](Source/).
- [Idealized transient EVA model](../Agastya%20Thermal/STAGE3_EVA_TRANSIENT_MODEL_README.md), code, and reproducible outputs.

The local project folder also contains Word and Excel prototype packages. They remain on the computer and are excluded from the initial GitHub source set until their content, embedded identity, and redistribution metadata have been reviewed. Their omission does not represent a technical decision to discard them.

## Stage 4 interface

Stage 4's purpose is silver removal/recovery from Stage 3-derived cell-bearing material. The hot knife's baseline output still contains EVA and backsheet. Additional preparation may therefore be required before a Stage 4 route can remove silver. The process method and output form remain open; candidate routes in [Stage 4 research](../Build%20Files%20and%20Steps/Stage%204/) are comparisons, not an approved chemical or operating procedure.

Sampling, assay, mass accounting, and uncertainty analysis validate the Stage 3 and Stage 4 outputs. They are not a substitute for Stage 4's silver-removal operation. AGASTYA has not built a thermal station, processed PV material, run an assay, removed silver, or recovered silver.

