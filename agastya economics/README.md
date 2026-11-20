# AGASTYA economics

**Updated:** 20 November 2026
**Currency:** INR
**Status:** catalogue-based education-scale comparison and a parameterized process-economics shell; no process-cell cost or ROI estimate.

The detailed catalogue screen is in STAGE2_ROBOT_ECONOMIC_SCREEN_2026-11-20.md. Its price references are seller display prices checked on 20 November 2026, not written quotations. The underlying workcell design has no measured payload, release forces, operating time, throughput, duty cycle, guarding scope or service requirements.

## Reproduced arithmetic

- Four listed Hiwonder servos: 4 × ₹2,579 = ₹10,316.
- Those four servos plus the listed Arduino Mega: ₹14,066.
- Adding the optional PCA9685 signal board: ₹14,315.
- Separate kit benchmarks in the source review: ACEBOTT ₹5,019 and Robokits ₹13,600; these are classroom products, not process-arm candidates.

These subtotals exclude motor power, wiring, fuses, hardware stop devices, guards, mechanical structure, fabrication, tax, delivery, commissioning and maintenance. The 2 m arm concept therefore remains unpriced.

## Reproducible model

Run:

    node "agastya economics/models/catalogue_cost_model.mjs"

The script writes the catalogue CSV, a JSON result and an all-null plant-input template under outputs/. The template lists the evidence needed for installed capital, annual throughput, sales or service revenue, silver-bearing product revenue, reagents, energy, water, labour, maintenance, transport and disposal. When inputs are absent, the model returns NOT_CALCULABLE and keeps cashflow and payback null.

A numeric example in the test suite verifies only the formula implementation; it is not an AGASTYA forecast or assumed scenario. Do not populate the template until values have traceable quotes or measured operating data.

## Source links

The copied review includes the original seller links. The catalogue model retains each listing URL with its price row and a scope note. No purchase was made. Catalogue availability and prices may change.
