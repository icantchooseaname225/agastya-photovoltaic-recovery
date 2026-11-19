# Stage 1 Sorter Bench Build

Reviewed 2026-09-26. This is a laptop-assisted, low-voltage tabletop demonstration. It is not a photovoltaic safety tester or a production panel-handling robot.

## Order this first

This first order creates a low-voltage sensor-and-camera demo around the AI Thinker ESP32-CAM and laptop you already have. Prices are seller-page listings checked 26 September 2026; tax/shipping and stock can change.

| Item | Price | Why |
|---|---:|---|
| 7Semi INA219 breakout | ₹229 | Demo voltage/current/power sensor; set its A0 address pad to `0x41` before use with a later PCA9685. [Robu listing](https://robu.in/product-category/current-and-voltage-sensor/) |
| 0.45 W, 3 V mini panel, 80 × 60 mm | ₹156 | Safe tiny test module for sensor/software bring-up. [Robu listing](https://robu.in/product-category/solar-panel-and-controller/) |
| 100 Ω, 0.25 W resistor | about ₹1 | Current-limited demo load. [Robu resistor listings](https://robu.in/product-category/carbon-resistors/) |
| 830-point breadboard | ₹61 | Sensor wiring. [Robu listing](https://robu.in/product-category/electronic-components/breadboard-and-zero-pcb/) |
| Female-female and male-female jumper sets | ₹41 + ₹39 | I²C/sensor wiring. [Robu listing](https://robu.in/product-category/dupont-cable/) |
| 15 cm steel ruler | roughly ₹30-100 locally | Measure the 80 × 60 mm demo panel; type readings into EYE. Not an automated dimension sensor. |
| ESP32-CAM-MB programmer, only if you do not already have one | ₹85 | USB upload. [Robo Bazar listing](https://robobazar.in/product/esp32-cam-mb-micro-usb-download-module-for-esp32-cam-development-board/) |

Core sensor parts total about **₹527**, or about **₹612 with the programmer**, before the ruler and shipping. Borrow a multimeter for the first low-voltage cross-check if you do not already own one; a listed basic meter adds about ₹699. Do not connect the demo parts to a full-size panel.

Optional foam-panel arm parts: acrylic frame ₹397 (frame only), four SG90 servos ₹344, PCA9685 driver ₹229. That is **₹970 listed**, but excludes the separate regulated 5 V servo supply, wiring, and delivery. [Frame](https://quartzcomponents.com/products/diy-acrylic-robot-manipulator-mechanical-arm-kit), [SG90s](https://quartzcomponents.com/collections/servo-motor), [PCA9685](https://robu.in/product-category/servo-motor-driver/). This is a lightweight classroom-style arm for a cardboard/foam prop, not a real solar module. Buying the arm plus all measurement hardware, multimeter, and power supply will exceed a ₹2,000 all-in budget.

If a suitable supply is not already available, Robu lists a 5 V/3 A adapter around ₹449; the arm bundle plus this supply is about **₹1,419 before shipping/wiring**. ([Power adapter listing](https://robu.in/product-category/power-supply-adapter/))

## What EYE does now

1. The AI Thinker ESP32-CAM captures a visible-light image and sends it over the private Wi-Fi network to the laptop.
2. Optional INA219 readings and manually entered frame dimensions travel with that capture. The laptop runs the image model, rules, operator screen, and panel ledger.
3. The saved inspection shows a lane result: **LEFT** for a c-Si second-life candidate only after an electrical pass is recorded; **RIGHT** for a c-Si Stage 2 route only after the operator records module isolation; otherwise **HOLD**.
4. Lane results are dry-run recommendations. EYE has no arm endpoint and sends no servo, motor, or claw command. The UI is useful now for PC image tests and for checking which route an operator would select.

The ESP32 does not run the vision AI. Raw voltage/current numbers are archived as measurements; they do not automatically become electrical pass/fail. Human test status and instrument/procedure details remain separate evidence. Do not mark a pass from an INA219 reading alone.

## Can it do the requested automatic scan today?

Not yet. The current app is a useful **PC inspection and dry-run triage prototype**, not an automatic scan-and-pick machine. Today it uploads one visible RGB image, runs the available screening models on the laptop, accepts manually recorded measurements, and shows a lane recommendation. It does not automatically identify panel technology, measure the frame, find a rear junction box, test electrical output, or command an arm.

The intended station is feasible as a staged research build, with different evidence sources for each field:

| Desired output | Credible Stage 1 method | What AI can contribute | Missing today |
|---|---|---|---|
| Panel technology | Read the rear nameplate; have an operator verify the result | OCR can suggest a technology/model from a readable label; image classification can be a secondary suggestion | No trained technology/OCR model or verified label set. Keep `unknown` when evidence is unclear. |
| Frame width and height | Fixed measurement fixture, or a calibrated camera with a known-size target in the panel plane | Computer vision can locate panel edges after lens/perspective calibration and convert pixels to mm | Current image has no scale/depth calibration; dimensions are manual. Do not train raw pixels to guess millimetres. |
| Junction-box position | Capture the rear side with a second camera or a controlled flip/turn step | A detector can return a box and normalized location from labeled rear images | The current camera sees only the front in its normal setup; no rear-view training labels/model. |
| Voltage/current/power | Appropriately rated, isolated PV I-V tracer or test instrument, with documented test conditions | AI can flag anomalies after instrument readings exist; it cannot measure these from RGB | The optional INA219 is only for a small low-voltage demo. The chip's common-mode limit is 26 V, so it is not a full-module tester. [TI INA219 specifications](https://www.ti.com/product/INA219) |
| IR/EL evidence | Thermal camera for temperature patterns; for EL, a suitable NIR-sensitive camera in a controlled setup with safe forward-bias equipment | Separate thermal/EL models can classify modality-specific patterns | A reflective IR obstacle sensor is not an EL camera. EL requires current injection and specialized imaging; it is not a passive snapshot. [EL imaging requirements](https://www.mdpi.com/2072-666X/16/4/437) |
| LEFT/RIGHT/HOLD | Evidence-gated software recommendation, followed later by a safety controller | AI is advisory; rules and interlocks own the route decision | EYE only displays the dry-run lane. No actuator protocol exists. |

For an unattended scan cycle, add a panel-present photoelectric sensor, a repeatable front/rear capture fixture, controlled lighting, physical dimension stops or a calibration target, and a separate rated electrical test station. Send a complete inspection record to the laptop; only a separate PLC/safety controller should later authorize motion. Missing images, uncertain identity/technology, uncalibrated readings, stale decisions, or any interlock fault must produce **HOLD**, never an inferred lane.

### Train the new outputs with the right labels

The existing public defect datasets do not supply trustworthy technology, physical dimensions, junction-box coordinates, or calibrated V/I/P targets for each photographed full panel. Training on them cannot teach those outputs. Do not label synthetic guesses as ground truth. Collect a research set where every capture is linked to a stable physical `panel_id` and has verified nameplate/OCR text, technology source, measured width/height, front/rear image side, junction-box box or `not_present`, instrument ID/calibration, voltage/current/power units, irradiance, module temperature, test procedure, timestamp, and modality. Keep all views/repeats of each physical panel in one split, and reserve a site/time-separated panel set for final testing.

Use separate tasks rather than one opaque “panel score”: OCR/technology suggestion; calibrated edge geometry; rear-view junction-box detection; defect localization/severity by modality; and measured electrical performance analysis. Electrical V/I/P are sensor readings, not AI regression targets unless a clearly defined, independently measured research target and operating conditions exist. EYE currently calculates snapshot power as V×I when those readings are supplied and retains the nameplate rating for comparison; this is not an STC-normalized performance test or a reuse certification.

## Stage 1 measurement parts

| What to measure | Stage 1 part or method | What reaches EYE | Limit |
|---|---|---|---|
| Visible appearance | Existing AI Thinker ESP32-CAM and fixed light/camera mount | JPEG to the laptop model and image ledger | Model is a screening aid; there is no trained burn/crack full-panel RGB model or verified severity estimate. |
| Low-voltage demo V/I/P | INA219 breakout, small 3 V demo panel, 100 Ω load resistor, jumper leads | INA219 sends raw voltage, current, and power headers with the image | Firmware adapter is enabled, but still sends `not_tested`; it never generates an electrical pass. INA219 uses ESP32-CAM GPIO13/14 for I²C, shared with microSD; do not use microSD at the same time. Never connect it, a breadboard, or the ESP32 to a full-size PV panel/string. |
| Reference V/I | Digital multimeter, in the meter's rated range | Record the reading and instrument ID in the laptop app | A multimeter reading is not a full I-V curve or a reuse certification. |
| Frame width/height | Steel ruler for the 80 × 60 mm demo module; tape measure for later full modules | Enter `width=<mm>` and `height=<mm>` in the ESP32 Serial Monitor, or type them in the app | This is a physical measurement, not automatic. The camera has no scale/depth reference. |
| Real module output test, later | PV-rated I-V curve tracer and qualified operator/procedure | Later instrument adapter or operator entry with instrument/calibration provenance | This is outside the sub-₹1,000 robot budget and must be rated for the module's maximum voltage/current. Never improvise a full-panel load with the demo INA219. |
| Panel temperature, optional later | Contact thermometer on the rear surface; thermal imager only if available | Not currently part of Stage 1 device telemetry | The experimental thermal-image model is not a calibrated temperature sensor. Add a separately identified instrument/API field before treating temperature as a measurement. |

For the current bench, use the 3 V demo panel, INA219 breakout, 100-ohm current-limited load, multimeter, breadboard, and leads. Keep the meter connections within its manual and rated range. Compare INA219 readings at several low-voltage points and record the instrument in the app. The firmware reads the sensor at I²C `0x41`; bridge the INA219 breakout A0 address pad to `0x41`. The PCA9685 uses `0x40` by default. If the INA219 board does not expose address pads, use a separate controller/bus instead of connecting both default-address devices together. No electrical pass/fail is produced by firmware.

### Rear nameplate and box capture

Use the same ESP32-CAM for the demo: keep the panel reference stable, capture `view=front`, turn the small prop over, then capture `view=rear_nameplate` and `view=rear_junction_box`. EYE stores each image as a separate inspection under the same panel passport and records the capture-view label. Read the nameplate manually and enter verified technology/rated watts; record the box position from the rear view. The `view` label is data organization, not OCR or automatic junction-box detection. The app can ingest a second rear camera later by assigning it its own sensor ID.

Do not buy IR obstacle modules to locate the junction box. A low-cost reflective IR module can detect nearby object/surface contrast at close range; it cannot tell a junction box from a cable, frame, or other rear feature. If wanted, it can serve only as a panel-present trigger. Use rear RGB images and labeled bounding boxes for box localization.

## Acrylic arm price check

Prices below were visible on seller pages during the review and can change; shipping is extra and the buyer should verify the pack contents before ordering.

| Part | Seller listing | Listed price |
|---|---|---:|
| 4-DOF acrylic frame/plate kit, without servos | [Quartz Components KIT-QC4911](https://quartzcomponents.com/products/diy-acrylic-robot-manipulator-mechanical-arm-kit) | ₹397 |
| Four 9 g SG90 servos | [Quartz Components SG90](https://quartzcomponents.com/products/tower-pro-sg90-servo-9-gms-mini-micro-servo-motor) at ₹86 each | ₹344 |
| PCA9685 16-channel servo signal board | [Robu PCA9685 listing](https://robu.in/product-category/servo-motor-driver/) | ₹229 |
| **Listed parts subtotal** | Acrylic frame + 4 servos + signal board | **₹970** |

The ₹970 subtotal excludes a suitable regulated 5 V servo supply (about ₹449 for a listed 3 A adapter), wiring, delivery, and mechanical calibration. It only stays under ₹1,000 if the power supply and controller are already available. The Quartz listing's package contents specify an acrylic plate set and fasteners, not servos; confirm that the exact frame has a gripper plate before buying.

There is an I²C address collision if both boards use their defaults: INA219 and PCA9685 commonly use `0x40`. The current EYE firmware now expects the INA219 at `0x41`, so bridge its A0 pad before testing; the PCA9685 may stay at `0x40`. Verify addresses with an I²C scan before attaching servos. [PCA9685 default address](https://learn.adafruit.com/16-channel-pwm-servo-driver/pinouts), [INA219 address pads](https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout?view=all).

Most importantly, SG90 servos and a thin acrylic educational arm are for a light tabletop mock panel only. They cannot safely pick up real glass PV modules. Use a foam/card mock-up for this demo. A real panel requires a purpose-designed support fixture, load-rated gripper, stronger actuators, guarding, emergency stop, and a safety controller; that is a later-stage build and cannot fit this budget.

## PC test and current upload path

1. Run `Start-EYE.bat`, upload a sample panel image, and verify the visual evidence appears.
2. For LEFT: select c-Si, enter measured voltage/current/power and instrument/procedure/operator evidence, set electrical test to Pass, and save a clean/second-life route. The lane card says LEFT / reuse candidate, not reuse approval.
3. For RIGHT: set panel technology to c-Si, select Stage 2 c-Si, check isolation, enter a reviewer note if overriding, and save. The lane card says RIGHT / Stage 2 recycling. Without isolation, it says HOLD.
4. For a broken/cracked/burned or uncertain panel, use HOLD until a person has assessed it and recorded the authorized Stage 2 route and isolation state.
5. To use the camera, follow the Arduino IDE and private-LAN instructions in the project README. The laptop must be running the device-enabled EYE server. Firmware uploads only the camera sketch; the AI/model remains on the laptop.

## Later actuator interface

Keep the ESP32-CAM as the capture/telemetry node. No arm-motion code or calibrated arm coordinates exist yet. The listed arm kit has no published geometry/payload suitable for computing coordinates from its listing; once assembled, measure link lengths, servo zero/limits, gripper offset, pickup fixture, and bin centers. Define the workcell frame at the pickup fixture (X across the two bins, Y along the feed direction, Z upward), calibrate camera pixels to that plane with a known target, then verify taught pick/drop poses slowly with a foam dummy and guarded workspace. A later sorter adapter must validate panel identity and decision freshness, require a human/PLC enable, and fail to HOLD on Wi-Fi loss, stale inspection, unknown technology, interlock fault, or emergency stop. A PLC or safety-rated control owns motion; the EYE API token and camera ESP32 are not safety circuits.
