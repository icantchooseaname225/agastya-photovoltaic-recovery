# Stage 3 Thermal Separation - Working Development Note

> **19 November 2026 revision:** The current foam-roller concept is not characterized in the existing thermal model or source package. The model remains a conduction scenario model, not a roller, separation-quality, or liberation prediction. See the [current architecture](../../AGASTYA_ARCHITECTURE.md) and [Stage 3 roller/liberation reassessment](STAGE3_ROLLER_AND_LIBERATION_PLACEMENT_REASSESSMENT_2026-11-19.md).


**Status:** literature scoping and model definition; no thermal trials or hardware validation have been performed.  
**Scope:** current Stage 3 is hot-knife separation followed by the foam-roller concept after Stage 2 robotic mechanical disassembly. Stage 4 handles material liberation/separation and silver recovery, with the route open. Thin-film modules remain routed to a licensed handler.

## Stage 3 objective

Record and evaluate traceable hot-knife and foam-roller operations that separate front glass from the cell/EVA/backsheet laminate. Define the roller interaction and characterize whether post-thermal mechanical liberation should be colocated at the outlet or handled in Stage 4. Stage 2 is now a robotic-arm-centered design concept; no physical robot is selected or tested. EYE is a record and measurement interface; it does not control heaters or other hazardous equipment.

The two separation claims must be treated separately:

1. **Glass-to-laminate separation:** hot-knife literature and commercial equipment support this as an established process. The separated laminate still contains EVA.
2. **Foam-roller interaction:** the current project direction specifies a foam roller after the hot knife, but its material, temperature, contact load, speed and intended output have not been specified. Older thesis text describes a heated roller; that historical wording does not establish that the current foam roller is heated or that it removes EVA. Treat both roller function and result as unvalidated.

Do not describe the second operation as validated thermal delamination until a source or experiment demonstrates its output and quality. EVA pyrolysis/decomposition is a distinct process and is not implied by softening-assisted mechanical separation.

## Literature findings to date

| Evidence | Reported conditions and outputs | Relevance and limit |
|---|---|---|
| IEA PVPS Task 12 hot-knife LCA, using pilot-plant data from NPC | Heated cutter separates glass from the EVA/cell/backsheet laminate; about 50 seconds per module. Reported electricity input is 0.035 kWh per kg of modules for the take-back and hot-knife treatment process. | Strong process and benchmark source. The electricity figure covers the reported treatment system, not an isolated Stage 3 heater and not a per-panel thermal energy measurement. Data quality is rated fair and downstream laminate treatment is outside the boundary. |
| NPC commercial equipment description | Hot-knife glass separation is specified at about 60 seconds per panel and a 300 C knife temperature. It outputs sheet glass and a cell/EVA sheet. A separately listed EVA scraper uses a brush on the separated glass surface to remove residual EVA. | Confirms glass separation and throughput are distinct from EVA removal. Supplier claims are not independent measurements. The scraper description does not validate EVA stripping from the cell/EVA sheet. |
| Saitta et al. (2026), thermal-assisted glass delamination | Small specimens heated in an oven at 100 C or 140 C for 60 minutes, followed immediately by manual peeling at about 45 degrees and 20-30 N; six specimens per condition. The article reports TGA stability below roughly 280 C and degradation onset near 300 C for its tested EVA. | Useful low-temperature, mechanically assisted comparison and a source for experimental variables. The hour-long oven treatment is not evidence of a sub-minute continuous process. Results are specific to the tested specimens and material. |
| Experimental EVA pyrolysis study (2023) | Reports two EVA pyrolysis stages at 284-411 C and 378-527 C. | Establishes that decomposition-focused thermal treatment is a different, much hotter process. It is not an operating target for Agastya's proposed softening and mechanical separation. |

### Implications for the thesis design

- The thesis's 180-220 C blade range is within ranges reported in some hot-knife descriptions, but commercial practice is not uniform: NPC currently describes a 300 C knife. Temperature must be validated against the actual feedstock, contact geometry, separation quality, and measured energy.
- A knife set-point is not the laminate temperature. Record both tool temperature and material/interface temperatures.
- The current foam-roller concept is not described by the glass hot-knife reference. First define its intended output and material-contact role. Reduced EVA, clean glass, and fully EVA-free cells are different outcomes and may need separate operations.
- The 100/140 C study supports testing a lower-temperature, longer-dwell condition as a comparison, not as a throughput claim.
- The IEA value of 0.035 kWh/kg can be used as a whole-process order-of-magnitude cross-check only after matching functional units and system boundaries. It must not be attributed to Stage 3 alone.

## Energy and heat-reuse model

Use separate quantities for heat absorbed by material, electrical energy drawn by equipment, and energy recovered between operations. All measured values should include the run boundary and instrument provenance.

### 1. Material sensible heat

For material layers or zones that actually change temperature:

`Q_sensible = sum_i [m_i * integral(T_in to T_out) cp_i(T) dT]`

For a constant heat capacity approximation:

`Q_sensible = sum_i (m_i * cp_i * delta_T_i)`

The current thesis estimate uses 1.45 kg of EVA per panel and heats all of it by 175 K:

`1.45 kg * 2.3 kJ/(kg K) * 175 K = 583 kJ = 0.162 kWh`

The arithmetic is consistent, but it is not yet a demonstrated Stage 3 requirement: a hot knife applies localized heat at a moving interface, so this estimate cannot assume that the complete EVA mass reaches the blade set-point. Conversely, it omits the blade, roller, supports, other heated material, warm-up, standby, and measured losses. Do not retain the 2.2 multiplier as a fact; replace it with measured energy and/or a loss model.

### 2. Equipment electrical energy

Measure heater input over the full run:

`E_electric = integral(t_start to t_end) V(t) * I(t) dt`

For an approximately steady load, `E_electric = P_avg * time`. Record warm-up, processing, idle/standby, and cool-down energy separately when the meter permits. Report both gross run energy and a clearly defined per-panel allocation:

`e_panel = E_batch / N_panels`

Do not infer electrical energy from the EVA mass or a heater nameplate rating. A wattmeter/power logger is needed for a measured energy result; voltage and current spot readings alone are insufficient when the heater cycles.

### 3. Process heat losses and mechanical work

For a model-based estimate, partition heat into material heating, equipment thermal mass, and losses:

`Q_input = Q_material + Q_tool + Q_loss`

Potential loss terms include convection, radiation, and conduction through fixtures:

`Q_conv = integral h * A * (T_surface - T_ambient) dt`

`Q_rad = integral epsilon * sigma * A * (T_surface^4 - T_ambient^4) dt`

`Q_cond = integral (k * A / L) * (T_hot - T_cold) dt`

Treat these as model terms only when their parameters are known. Measure total electrical input directly and use the model to explain or bound it. Record separation force or mechanical drive energy separately if the required peeling action is part of the research question.

### 4. Retained heat between operations

Estimate sensible heat carried by the stream leaving operation 1:

`H_stream = sum_j [m_j * integral(T_next to T_exit,j) cp_j(T) dT]`

The maximum useful heat for operation 2 is bounded by that stream enthalpy and the temperature range where the intended separation remains possible. Define a measured transfer effectiveness `eta_transfer` between 0 and 1:

`Q_reused = eta_transfer * H_stream`

`Q_external,2 = max(0, Q_required,2 - Q_reused)`

Measure material temperatures at the first-operation exit and second-operation contact, along with the elapsed transfer time. Heat reuse is supported only if the second operation achieves its defined separation outcome at the measured incoming temperature with lower metered external energy and without unacceptable yield/quality loss. Do not count the same retained heat in both operations.

### 5. Power, throughput, and solar sizing

After measured energy and cycle time are available:

`thermal panels/day = available Stage 3 energy per day / measured kWh per panel`

`cycle-limited panels/shift = shift_seconds / measured seconds per panel`

`Stage 3 panels/shift = min(energy-limited capacity, cycle-limited capacity)`

For a solar-only scenario:

`daily electrical yield = array_kWp * peak_sun_hours * system_efficiency`

The existing 4 kW, 5.5 peak-sun-hours, and 0.8 efficiency assumptions give 17.6 kWh/day. The thesis's approximately 49 panels/day follows only if the assumed 0.36 kWh/panel is valid; this is therefore a provisional scenario, not a measured throughput. Also check heater peak power, battery usable energy, inverter rating, duty cycle, and non-Stage-3 loads before making a system claim.

## Bench-validation plan

The thesis's temperature-versus-time experiment is a starting point. A useful Stage 3 experiment must measure energy and output quality as well as temperature and time.

### Before any active heating

- Inventory the actual blade/heater, temperature controller, power meter, thermocouples, force gauge, panel coupons, enclosure/guarding, ventilation, and available emergency controls.
- Have the responsible lab supervisor assess the actual materials and setup, including damaged-panel hazards, sharp glass, electrical isolation, hot surfaces, fumes, ventilation/exhaust, fire response, and waste handling. No active trial until the actual equipment and controls are approved by that supervisor.
- Begin with a cold/dry workflow and measurement-record rehearsal. This document does not claim that any thermal trial has occurred.

### Experimental sequence

1. Use traceable c-Si coupons or scrap module sections with known construction where available. Record source, dimensions, mass, glass condition, backsheet type if known, EVA layer count/thickness if known, and prior damage. Keep coupons from one module grouped when comparing conditions.
2. Run an unheated mechanical-peel control where safe and feasible. Then test a small set of literature-grounded conditions, including lower-temperature assist (100/140 C as a slow-heating comparator) and hot-knife conditions (180/200/220 C, with 300 C only if justified by the equipment and supervisor review). These are candidate test points, not established safe or optimal settings.
3. Hold coupon geometry, cut length, tool geometry, feed/peel speed, applied force, ambient conditions, and operator method constant or record them. Randomize trial order where practical. Use at least three independent coupons per condition for an initial screen; increase repeats after variability is understood.
4. Record blade set-point and measured tool temperature, material/interface temperature, inlet/outlet stream temperatures, warm-up time, process time, electrical energy, separation force or motor load, and transfer delay between operations.
5. Score each output against a predeclared rubric: glass intact/usable, separation completeness, residual EVA location/amount, cell breakage, backsheet condition, and mass of each collected stream. Photograph each coupon/output with an ID and scale. Do not claim EVA purity or removal without a suitable measurement method.
6. Only after glass separation is repeatable, test the roller as a separate operation against a defined output and a no-roller control. Compare external energy, retained stream temperature, separation quality, and damage. This isolates whether the roller adds value and whether retained heat is sufficient.

### Minimum record fields

`trial_id`, source/module and coupon ID, Stage 2 event reference, operator, station, date/time, instrument IDs and calibration references, material/geometry, ambient temperature, tool set-point and measured temperatures, process and transfer times, voltage/current/power trace or integrated energy, force/load, output stream masses, quality scores, safety holds/deviations, and notes.

Each coupon must remain linked to its source panel and Stage 2 handoff. If coupons or outputs are combined, create and record a batch/stream ID and parent IDs before combining them.

## EYE event-record fit

The Stage event API accepts mass, temperature, voltage, current, power, energy (`J`, `Wh`, `kWh`), and duration (`s`, `min`). Keep instrument and calibration references for every measured event. The event API is not a heater controller or a safety interlock.

## Open decisions

- Is Stage 3 required to produce glass plus cell/EVA/backsheet laminate, or glass plus substantially EVA-free cells? The latter requires a separate evidence-backed operation.
- Is the Stage 3 bench test intended to use whole small panels, donated modules, or coupon sections? What actual instruments and supervised lab facilities are available?
- Which process temperatures are supported by the available equipment's rating and supervisor-approved controls?
- What measurable product-quality threshold defines successful glass separation and, separately, EVA removal?

## References

1. Frischknecht, R., Komoto, K., and Doi, T. (2023). *Life Cycle Assessment of Crystalline Silicon Photovoltaic Module Delamination with Hot Knife Technology*. IEA PVPS Task 12, Report T12-25:2023. [Report PDF](https://iea-pvps.org/wp-content/uploads/2023/07/Report_IEA-PVPS_T12-25-2023_LCA-PV-Recycling-Hot-Knife.pdf).
2. NPC Incorporated. *Solar Panel Recycling Machine*. Manufacturer process description and equipment separation: glass separator and separate EVA scraper. [Product page](https://www.npcgroup.net/eng/solarproduct/dismantling).
3. Saitta, L. et al. (2026). *Effect of Temperature on the Glass Delamination in End-of-Life of Crystalline Silicon Photovoltaic Panels*. Green, 1(1), 2. [Article](https://doi.org/10.3390/green1010002).
4. *Pyrolysis mechanism and recycling strategy of end-of-life photovoltaic modules based on the experiment and the density functional theory* (2023). Polymer Degradation and Stability, 217, 110545. [Article](https://doi.org/10.1016/j.polymdegradstab.2023.110545).


