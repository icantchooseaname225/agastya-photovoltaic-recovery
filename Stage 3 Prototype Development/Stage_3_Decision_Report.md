# AGASTYA Stage 3 — decision report

**Decision date:** 16 October 2026  
**Current map:** Stage 3 thermal treatment/delamination; Stage 4 silver removal/recovery.  
**Evidence status:** literature/design review only; no AGASTYA hardware, thermal trial, Stage 4 silver-removal trial, or assay.

## 1. What is Stage 3 supposed to accomplish?

Stage 3 applies controlled heat to separate the front glass from a prepared crystalline-silicon module. The working reference is a fixed, guarded hot knife with controlled support/feed. Its first expected outputs are sheet glass plus a cell/EVA/backsheet laminate. It does not establish complete EVA removal or silver liberation.

## 2. Is the thermal concept scientifically justified?

Hot-knife glass separation is described in PV recycling literature and commercial equipment sources, so the mechanism is a reasonable prototype target. Published cycle times and temperatures belong to other equipment and feeds. They do not establish an AGASTYA operating window, quality, energy use, or safety. Thermal-softening coupon studies are useful comparisons but use different heating geometry and much longer dwell times. Pyrolysis is a separate, higher-temperature process and is not included in this hot-knife concept.

## 3. What is the best low-cost implementation?

Start with a cold fixture and data workflow. If that gate passes, conduct instrumented coupon trials using an approved, guarded thermal station at a qualified facility. A benign tabletop surrogate can test handling and logging but cannot demonstrate PV delamination. Do not build or energize an improvised heater or thermal enclosure.

## 4. What is the estimated cost?

A complete thermal station cost is unknown because the blade/feed fixture, guarding, heater/control, independent over-temperature protection, facility work, probes, calibration, and supervisor requirements need host-specific specifications and quotes. Previously checked reference prices for a plug-in energy meter and a suitable scale total ₹13,181; this is only a partial instrumentation reference, excludes thermometer/probes and the thermal station, and is not a prototype total. See the editable [cost model](Stage_3_Prototype_Cost_Model.xlsx).

## 5. Which components can a student realistically prepare?

The student can document requirements, build a cold support/guide mock-up from approved materials, label and weigh benign test pieces, prepare the data workflow, and analyze facility-provided measurements. Any energized heating, hot blade, moving feed, PV coupon, or glass-breakage trial requires the responsible facility's approval, trained supervision, and approved controls.

## 6. Which tasks require a qualified facility or professional?

Thermal equipment selection and active heating; PV feed admission; electrical protection; independent over-temperature protection; guarding; ventilation/fume review; emergency response; broken-glass handling; and waste disposition require a qualified facility and responsible supervisor. Stage 4 silver removal/recovery also requires its own route-specific facility, chemical/process safety review, waste plan, and assay method if the selected route involves hazardous chemistry.

## 7. Which software should be used first?

Use the existing local Python/NumPy environment or spreadsheet for energy and mass-balance calculations, uncertainty, plots, and traceable trial records. Retain the custom thermal model as an unvalidated planning tool; compare it with coupon measurements before using it for design decisions. CAD can wait until the host supplies dimensions. CFD or multiphysics software is not justified before geometry and measured boundary conditions exist.

## 8. What can be demonstrated without PV waste?

A cold fixture can demonstrate panel support, edge access, handling, and output routing with inert templates. A supervised low-risk temperature-control demonstration on non-PV surrogate material may test instrumentation if approved. Neither demonstrates PV glass separation, EVA removal, silver liberation, or silver recovery.

## 9. What evidence is required to claim that Stage 3 works?

Use traceable coupons, a predeclared separation-quality rubric, calibrated tool and interface temperature measurements, electrical energy logging, repeat trials, input/output mass reconciliation, glass damage scoring, cell/backsheet condition, and clear photo/sample lineage. Whole-panel claims require whole-panel trials; coupon results do not establish throughput. Any EVA-removal claim needs its own defined and measured outcome.

## 10. What are the first five actions?

| Rank | Action | Cost now | Dependency/output |
|---:|---|---:|---|
| 1 | Confirm Stage 3 target output and Stage 4 feed requirement; decide whether Stage 3 initially stops at glass/laminate separation. | Desk work | Written stage-interface specification. |
| 2 | Inventory actual feed, thermal station, probes, power meter, scales, guards, ventilation, and emergency controls with a facility supervisor. | No purchase | Verified host inventory and permitted feed. |
| 3 | Freeze a cold-fixture drawing and coupon record fields using measured host dimensions. | Desk work | Approved geometry and handling sequence. |
| 4 | Request a facility quote for guarded thermal equipment/time, supervision, instrumentation, and waste handling. | Quote only | Complete cost basis before procurement. |
| 5 | Prepare a small, supervised coupon comparison and review its acceptance criteria, safety plan, and data sheet before any active heating. | Quote only | Signed method and risk review. |

## 11. Largest unresolved risks

The Stage 3 feed construction and output target are unknown; the hot-knife temperature/contact/feed window is not measured; the first output retains EVA and backsheet; the heated roller and heat-reuse claims are unvalidated; energy and throughput cannot be estimated from the current panel-level heat calculation; facility and instrumentation access are unconfirmed; and Stage 4's silver-removal route needs a feed-preparation decision, qualified controls, assay QA/QC, and a defined product form.

## 12. Next milestone for integration

Approve a written interface specification: Stage 2 feed condition, Stage 3 thermal output(s), what Stage 4 must accept, and whether Stage 3 is only a front-glass separation or includes a separately tested EVA-removal operation. Then obtain the host inventory/quote and complete the cold fixture. No purchase or active heating is justified before those gates.

## Evidence boundary

Literature settings, cycle times, and energy values are attributed to their original equipment and process boundaries. No AGASTYA process setting, recovered silver, purity, throughput, cost, or energy result is claimed. See the [Stage 3 references/evidence register](Stage_3_References_and_Evidence_Register.xlsx) and [current architecture](../AGASTYA_ARCHITECTURE.md).

