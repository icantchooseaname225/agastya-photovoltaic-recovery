# Stage 2 robotic workcell economic screen

**Price check:** 20 November 2026<br>
**Currency:** Indian rupees (INR)<br>
**Status:** public catalogue comparison for education-scale hardware; no vendor quotation, purchase decision or process-cell cost estimate.

## Decision boundary

The 2 m arm in the companion CAD files is a reach-envelope concept, not a selected robot. A price for a classroom servo arm cannot be scaled into a cost for a PV de-framing/J-box-removal cell. The current record has no measured module, tool mass/centre of gravity, frame-release force, junction-box removal force, cycle-time target, duty cycle, guarding design or receiver requirement. I therefore do not give a whole-cell price, cost-per-panel, payback or profitability figure.

## India catalogue comparisons

| Option / listing | Displayed price | What it can help answer | Boundary |
|---|---:|---|---|
| ACEBOTT ESP32 4-DOF arm kit, Robu.in | ₹5,019 | Lowest observed complete educational-arm benchmark. Seller page describes a ready learning kit and six servos. | The title says ESP32 while its detailed specification names ESP8266; confirm controller, servo count, payload, reach and warranty with the seller before purchase. It is not evidence of PV-frame or junction-box capability. |
| 6-DOF DIY robotic arm kit with USB servo controller/software, Robokits India | ₹13,600 | Higher education-scale kit benchmark with a listed controller/software bundle. | The product page lists 350 mm maximum reach and 100 g maximum payload. It is a classroom-scale reference, not evidence of PV-frame or junction-box capability; confirm included controller and power items before purchase. |
| Four Hiwonder HPS-2027 servos, Robu.in listing | 4 × ₹2,579 = ₹10,316 | Price reference for a four-axis hobby-servo build. The seller labels these “20KG” high-torque servos. | The listing consulted did not provide enough verified voltage, stall-current, torque-curve or duty-cycle data to size the arm or supply. The “20KG” label is not used as an engineering rating. |
| Official Arduino Mega 2560, Robu.in listing | ₹3,750 | Controller price reference for a student bench prototype. | It is not a robot safety controller and must not directly authorize process motion. |
| Optional PCA9685 16-channel PWM board, Robu.in listing | ₹249 | Optional signal-generation board if needed for a bench prototype. | It generates PWM signals; it does not provide servo motor power or make a safety function. |

Four listed hobby servos plus one official Mega total **₹14,066** for those listed items only; adding the optional PCA9685 gives **₹14,315**. Both are incomplete electronics subtotals: separate motor supply, hardwired E-stop power interruption, fuses, switches, limit devices, enclosure, wiring, mechanical structure, fabrication, delivery and any added tax are excluded. Availability and displayed prices can change.

## Reach versus torque: why the low-cost kits are not process-arm candidates

The CAD envelope uses 1,100 mm and 900 mm links. At a horizontal 2,000 mm reach, a 1 kg payload alone produces a shoulder gravity moment of about **19.6 N·m** (`1 kg × 9.80665 m/s² × 2.0 m`) and an elbow moment of about **8.8 N·m** for the 900 mm forearm. These are payload-only lower bounds; link mass, tool mass, acceleration, friction and a design margin add load. The figures are an elementary static screen, not an actuator selection.

This makes the catalogue arm kits useful for joystick/control learning, scale mock-ups and coordinate demonstrations only. Do not use the hobby-servo cost subtotal to cost or build the two-metre concept. The actual process arm's purchase and integration costs remain **unestimated** pending measured inputs and manufacturer data.

## Economical path to compare

1. If a demonstration is needed soon, compare the ready ₹5,019 education kit with the ₹13,600 kit after confirming the listed contents and asking for reach/load specifications. Use it only for a small unloaded mock-up and keep it mechanically separate from AGASTYA-EYE and any PV material.
2. For the project cell, compare three layouts after measurement: (a) arm plus tool-changing, (b) a shorter-reach arm on a rail or panel indexer, and (c) dedicated de-framing/J-box fixtures. Include robot/controller, tooling, fixture/indexing, safety guarding, extraction/collection, installation, training, maintenance and downtime in vendor quote requests.
3. Request written quotes only after a qualified reviewer signs off the required reach, payload/wrist moment, tool force, cycle time, duty cycle, operating environment and stop/guard architecture. Ask for India delivery, tax, commissioning, warranty, spares and service terms.
4. Defer cost-per-panel and payback until there are measured cycle times, energy, labour, consumables, yield/losses, maintenance and a verified receiver/disposal route.

## Sources and quote status

The values below are web-displayed catalogue prices observed on 20 November 2026, not pro-forma quotes. No order was placed.

- [ACEBOTT 4-DOF kit listing — Robu.in](https://robu.in/product/acebott-esp32-4-dof-robot-arm-kit/)
- [6-DOF robotic-arm kit listings — Robokits India](https://robokits.co.in/robot-kits/robotic-arm-kit/)
- [6-DOF kit product specifications — Robokits India](https://robokits.co.in/robot-kits/robotic-arm-kit/robotic-arm-6-dof-diy-kit-with-usb-servo-controller-and-software)
- [Hiwonder servo category and HPS-2027 listing — Robu.in](https://robu.in/product-category/hiwonder-servo-motor-and-accessories/)
- [Official Arduino Mega 2560 category — Robu.in](https://robu.in/product-category/classic-family/)
- [PCA9685 servo-driver listing — Robu.in](https://robu.in/product-category/servo-motor-driver/)
- [NXP PCA9685 data sheet](https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf)

No source provides an accepted PV-cell process-arm quotation. No machine selection, purchase, ROI or cost claim is made.

## Day 43 quote-comparison addendum — 21 November 2026

I added a capital quote-input model for three layouts that still need a common, measured design basis:

1. **Arm plus task tooling:** quote the robot/controller package, task tools, panel support, guarding, power/controls, extraction/output handling, installation, training and initial spares.
2. **Short-reach arm with a rail or panel indexer:** quote the smaller arm package and the rail/indexer as separate lines, then include the same tooling, fixture, safety, installation and support scope.
3. **Dedicated mechanisms and fixtures:** quote the task-specific mechanisms, tools, support fixture, guarding, power/controls, extraction, commissioning, training and spares.

The template is [`inputs/workcell_quotes.template.json`](inputs/workcell_quotes.template.json); the result is [`outputs/WORKCELL_QUOTE_COMPARISON.json`](outputs/WORKCELL_QUOTE_COMPARISON.json). The calculator requires every capital line to have a line total, named supplier, quote reference and date, plus explicit tax and delivery/installation/commissioning scope. It leaves the comparison marked incomplete until all three layouts have complete inputs. No prices were supplied or estimated for these process-cell options.

Even a complete capital comparison would not establish the cheapest cost per panel or payback. Those still need measured cycle time and throughput, staffing, energy, consumables, maintenance, yield/losses, receiver terms and disposal costs. None of the educational kit prices above has been carried into this process-cell template.
