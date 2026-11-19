# Stage 3 Prototype Build Plan

> **19 November 2026 revision:** Current direction is Stage 2 robotic mechanical disassembly and Stage 3 hot knife followed by a foam-roller concept. The earlier build plan treats hot-knife-only glass separation as the baseline. No robot, foam roller, integrated station or physical result is validated. Use the new roller characterization section and the [placement reassessment](STAGE3_ROLLER_AND_LIBERATION_PLACEMENT_REASSESSMENT_2026-11-19.md).


## Build target

Build an instrumented proof-of-concept for **front-glass separation from flat, intact crystalline-silicon modules** after Stage 2 robotic mechanical disassembly using a panel-support fixture. The first output is sheet glass plus a cell/EVA/backsheet laminate. Do not claim that this first station produces EVA-free cells.

The current process direction includes a foam roller after the hot knife, but its mechanical/thermal role and operating parameters are not yet specified. Use the hot-knife-only condition as a baseline/control and evaluate the roller in matched, measured trials after the interface is defined. Stage 4 is silver removal/recovery; its accepted feed condition is not yet specified. Do not silently treat the Stage 3 hot-knife laminate as EVA-free cells or as a proven Stage 4 feed.

## Recommended mechanism

Use a **fixed, guarded hot knife with controlled panel feed**. The panel travels through a guided support/feed mechanism and the blade acts at the glass/EVA boundary. Keep the two separated outputs supported and directed to different collection areas.

This follows the documented direction of NPC's development: its initial moving-blade concept had difficulty with uneven end-of-life panels and output handling; the later concept held the knife in place and fed the panel between rollers. The same development account describes the panel-edge entry as a major glass-breakage challenge and reports later blade and two-step improvements. This is useful design evidence, not a ready-to-copy drawing or validated Agastya specification. [NEDO/NPC development account](https://webmagazine.nedo.go.jp/practical-realization/articles/202503NPC/)

### Station blocks

1. **Feed and support:** rigid table, side guides, flat support under the module, and a controlled feed mechanism. Initially limit feed to known, flat modules. The IEA-assessed pilot process also required flat, unbent modules. [IEA PVPS Task 12 report](https://iea-pvps.org/wp-content/uploads/2023/07/Report_IEA-PVPS_T12-25-2023_LCA-PV-Recycling-Hot-Knife.pdf)
2. **Blade assembly:** replaceable blade with adjustable height/position so the contact path can be aligned to the bonded interface. The heater controller, sensor placement, insulation, guarding, and independent over-temperature protection must be selected and reviewed for the actual lab equipment. This plan does not specify a heater wiring design.
3. **Separation and collection:** keep a controlled path for the glass sheet and a separate supported path for the cell/EVA/backsheet laminate. Do not let either output fall freely or collide with the blade or frame.
4. **Measurement:** tool and material/interface temperature sensors, elapsed-time logging, electrical energy meter, feed-speed measurement, scale, and optional force/load measurement. Record instruments and calibration references.
5. **Guard and stop:** physically guard the hot blade, moving feed, pinch points, and glass edges. Provide an accessible stop and a reviewed response for stuck material, breakage, heater over-temperature, and loss of power.

## Build sequence

### Phase A: Freeze the process boundary

- Confirm the Stage 2 robotic workcell hands off a traceable, de-framed, de-junctioned, electrically isolated c-Si module supported and handled under the approved facility procedure.
- Define the initial accepted feed: flat, intact glass and documented panel/coupon identity.
- Define the desired first output and a simple visual/physical scoring rubric for glass damage, separation completeness, cell damage, backsheet damage, and EVA residue location.
- Confirm the feed state required by the selected Stage 4 silver-removal route. If it requires EVA-free or liberated cells, specify and validate that additional operation instead of silently treating the hot-knife laminate as clean cells.

### Phase B: Cold fixture

- Build the frame, support, guides, feed path, blade holder, guards, and separate collection supports without energizing a heater.
- Use inert dimensions/templates or cold panel coupons to check alignment, panel support, edge entry, clearance, output routing, and safe removal of a jammed coupon.
- Rehearse the operator sequence and data sheet. Correct support or alignment issues before active heating.

### Phase C: Instrumented coupon trials

- Begin only after the responsible lab supervisor has reviewed the actual materials, machine, ventilation, guarding, electrical equipment, and emergency response.
- Use traceable coupons from one known module where possible. Keep coupon geometry consistent and photograph each coupon before and after.
- Run an unheated separation control if the fixture permits it. Then compare a small set of approved thermal conditions while changing one factor at a time. Literature temperatures are references only; they are not pre-approved settings.
- Record blade set-point and measured blade temperature separately from the material/interface temperature. Log warm-up energy, processing energy, processing time, feed speed, cut length, force/load if available, and transfer delay.
- Weigh input and each output stream. Record glass cracking, incomplete separation, cell damage, backsheet condition, and EVA residue separately. Keep raw observations unchanged in the trial workbook.
- Repeat promising conditions on independent coupons. Do not extrapolate coupon energy or throughput to a full panel without a full-panel check.

### Phase D: Whole-panel confirmation

- After repeatable coupon results, process one eligible whole panel using the same controlled feed and measurement setup.
- Record the full cycle, including warm-up and handling, and reconcile output masses. Report the tested module geometry, construction, condition, and any excluded feed types.
- Repeat on additional panels before describing the operating window as robust. Warped or broken panels remain outside the first prototype's demonstrated scope.

### Phase E: Foam-roller characterization study

- Treat foam-roller interaction as a separately measured operation after the hot-knife baseline. Define the roller material, temperature rating, diameter/hardness, compression, line load, speed, contact path, cleaning method and output-quality endpoint before testing. Do not assume it removes all EVA.
- Compare matched feed with and without roller action. Record hot-knife outlet temperature, transfer delay, roller temperature if controlled, force/line load, speed, electrical energy, separation quality, cell/glass damage, residual polymer, foam wear/debris and cleaning residue.
- Make no heat-reuse or EVA-removal claim unless the corresponding output-quality and energy comparison is predeclared and measured.

## Stage 3 measurements

For each trial, retain these core fields:

- Identity: trial, source panel, coupon, batch/stream, Stage 2 event, station, operator, timestamp.
- Feed: panel construction if known, dimensions, coupon area, input mass, flat/warped/broken condition.
- Conditions: ambient temperature, blade set-point, measured blade temperature, material/interface temperatures, feed speed, cut length, warm-up time, process time, and transfer delay.
- Inputs: integrated electrical energy, instrument IDs, calibration references, and force/load if measured.
- Outputs: glass, laminate, and debris masses; mass-balance closure; glass condition; separation completeness; cell/backsheet damage; EVA residue observation; photo references; deviations and holds.

The EYE event API can store calibrated temperature, mass, power, energy, and duration observations. It remains a traceability interface and does not control the heater or provide a machine safety function.

## Components and budget status

The functional BOM is the five station blocks above. The knife/feed fixture, guards, thermal controller and independent over-temperature protection must be engineered and quoted for the actual lab; no online hobby rope cutter or unreviewed heater is an acceptable substitute for a PV delamination station.

The following live India listings provide only a **partial instrumentation reference**, checked 3 October 2026:

| Item | Reference listing | Listed price | Scope note |
|---|---|---:|---|
| Plug-in AC energy meter | [AmiciKart 16 A power/energy monitor](https://www.amicikart.com/products/amicisense-digital-socket-power-meter-energy-monitor-for-voltage-amps-frequency-test-16a-capacity-with-real-time-cost-calculation) | ₹1,499 | For exploratory energy logging only if compatible with the approved load and supply; not a substitute for a calibrated lab power analyser. |
| Dual-input K-type thermometer | [HTC DT-302-2 listing](https://www.japsin.co.in/product/digital-thermometer-dual-input/) | Price not shown in accessible listing | Requires suitable probes and calibration/check records; measure tool and interface separately. |
| 30 kg bench/platform scale | [Hindustan Scale Bluetooth 30 kg](https://www.hindustanscale.com/product/bluetooth-enabled-customized-scale/) | ₹11,682 incl. GST (listed lower configuration) | Resolution and platform size must suit coupon/output masses; supplier offers higher-cost versions. |
| Fixed hot-knife fixture, feed/support, guards, heater/control, independent limit, output supports | Lab-specific fabrication and approved component selection | **Quote required** | Cost cannot be responsibly estimated before lab dimensions, feed geometry, electrical supply, supervision and safety review are known. |
| Temperature probes and reference/check instrument | Lab-specific | **Quote/borrow required** | Do not count an uncalibrated thermocouple display as validated temperature data. |
| Feed-speed and optional force measurement | Lab-specific | **Quote/borrow required** | Can be omitted in the earliest cold-fixture phase but must be defined before the corresponding claim is tested. |

The visible priced references above total ₹13,181, but this is **not** a Stage 3 machine cost and is not a complete experiment kit: it excludes the thermometry price, core hot-knife station, fixture, guards, probes, electrical review, feed mechanism, consumables, delivery, and calibration. Reuse or borrow suitable instruments where possible and seek a lab quote before procurement. Seller prices and availability can change.

For scale context only, a 2022 TNO cost assessment reports €579,000 for the hot-knife part of a commercial automated line and €1.3 million for the combined installation ([TNO assessment](https://www.stichting-open.org/wp-content/uploads/2022/12/22-12822_tno_rapport_recycling_zonnepanelen_-def.pdf)). This is an industrial installation reference, not a quote or an appropriate price estimate for a supervised coupon-scale research fixture.

## Evidence boundary

The IEA report describes glass separation from the EVA/cell/backsheet laminate in about 50 seconds per module. NPC's current product page describes approximately 60 seconds per panel and a 300 C knife. These provide process references only; Agastya has not measured its own temperature window, energy per panel, throughput, output quality, or heat-reuse benefit. The IEA's 0.035 kWh/kg is a broader pilot treatment-process inventory value, not an isolated Stage 3 heater measurement.

No thermal trial, hardware build, or recovery result is claimed in this plan.


