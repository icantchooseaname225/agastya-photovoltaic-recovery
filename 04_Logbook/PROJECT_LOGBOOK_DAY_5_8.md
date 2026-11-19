# Agastya Project Logbook: Days 5-8

**Prepared:** 30 September 2026  
**Record status:** desk research, calculations, and planning only. No Stage 3 hardware build or active thermal experiment is claimed. Day numbers continue the Day 3-4 entry; calendar dates for those project days were not supplied.

## Day 5 - Thermal Delamination Literature Review

### Objective

Understand what hot-knife thermal delamination separates, what evidence exists for operating conditions, and how it differs from EVA removal and pyrolysis.

### Work completed

- Reviewed the IEA PVPS Task 12 hot-knife assessment, NPC's commercial process description, and NEDO's account of NPC's hot-knife development.
- Compared the hot-knife route with a 2026 lower-temperature assisted-peeling study and a separate EVA pyrolysis study.
- Recorded that the established hot-knife output is front glass plus a cell/EVA/backsheet laminate. The roller step proposed in the thesis is a separate, unvalidated EVA-removal hypothesis.

### Findings

- The IEA pilot-plant assessment reports approximately 50 seconds per module. NPC describes approximately 60 seconds per panel and a 300 C knife on its current product page. These are reference conditions, not Agastya trial results.
- NEDO's development account describes moving from a moving-blade concept to a fixed blade with controlled panel feed. It also documents glass breakage at panel entry and the later need to refine blade design and the separation sequence.
- Lower-temperature assisted peeling at 100 C and 140 C used an oven dwell of 60 minutes followed by manual peeling. This supports comparison research, not a fast-throughput claim.
- EVA pyrolysis occurs at much higher temperatures and is a different, emissions-relevant process from heat-assisted mechanical separation.

### Status

Literature findings recorded in `../Build Files and Steps/Stage 3/STAGE3_THERMAL_DEVELOPMENT.md`. No physical experiment performed.

## Day 6 - Stage 3 Process Definition

### Objective

Choose a defensible first prototype boundary and map how material moves through it.

### Work completed

- Defined the Stage 3 first-build objective as glass-to-laminate separation on flat, intact c-Si feed after manual Stage 2 de-framing and junction-box removal.
- Selected a fixed, guarded blade with controlled panel feed, supported outputs, and separate glass/laminate collection as the candidate architecture.
- Deferred the heated roller until the glass-separation baseline is repeatable and the EVA-removal output can be measured.
- Recorded the unresolved Stage 3-to-Stage 4 interface: Stage 4's thesis description expects EVA-stripped cell material, while the hot knife produces an EVA-containing laminate.

### Status

Build phases and station blocks recorded in `../Build Files and Steps/Stage 3/STAGE3_BUILD_PLAN.md`. No parts selected or hardware built.

## Day 7 - First-Principles Energy Model

### Objective

Recalculate the thesis's EVA sensible-heat estimate and identify what can and cannot be inferred from it.

### Work completed

- Used the thesis assumptions: panel area 1.7 m2, two EVA layers each 0.45 mm, density 950 kg/m3, heat capacity 2.3 kJ/(kg K), ambient 25 C, and target 200 C.
- Calculated EVA mass as 1.4535 kg and the whole-EVA sensible-heat estimate as 585.0 kJ, or 0.1625 kWh per panel.
- Applied the thesis's explicitly assumed 2.2 multiplier to calculate 0.3575 kWh per panel. This multiplier remains an assumption, not a measurement.
- Recalculated the thesis solar-yield case: 4 kW x 5.5 peak-sun-hours x 0.8 = 17.6 kWh/day. Dividing by 0.3575 kWh/panel gives about 49.2 panels/day, conditional on the assumed energy figure.
- Noted that a localized hot knife does not heat the whole EVA mass uniformly. The sensible-heat result is therefore not a measured heater demand or a validated minimum for the real process.

### Status

Calculated values are included in the Stage 3 workbook and labeled as thesis-input calculations. No measured energy or throughput exists.

## Day 8 - Measurement and Trial-Record Design

### Objective

Prepare a repeatable way to capture real coupon and panel trials without mixing observations with assumptions.

### Work completed

- Defined raw trial fields for material identity, geometry, temperature, feed speed, time, energy, force/load, output masses, quality observations, instrument provenance, and safety deviations.
- Added energy and duration units to the EYE stage-event measurement vocabulary so future observations can be recorded with their instrument and calibration references.
- Prepared a blank trial-log worksheet and formula-driven model/sensitivity scenarios. Blank trial rows contain no invented observations.
- Kept active thermal work behind an equipment-specific supervisor review. No temperature setting is declared safe or optimal by this desk study.

### Status and next actions

- No active heating, delamination result, heat-reuse result, or hardware validation is claimed.
- Inventory the actual heater/blade, temperature sensors, power meter, scales, force gauge, panel material, guarding, ventilation, and available supervised lab facilities.
- Conduct the cold fixture and record-rehearsal phase before requesting review of any active thermal trial.
- Confirm what Stage 4 can accept before deciding whether EVA removal belongs in Stage 3.
