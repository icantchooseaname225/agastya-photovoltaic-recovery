# Agastya Project Logbook

## Tue, Day 3-4 Combined - Shift from Stage 1 Automation to Stage 3 Process Development

### OBJECTIVE

Keep the overall recycling workflow coherent while changing the immediate build focus. Stage 2 robotics is outside the current budget, so Stage 2 will be a supervised manual handoff for this prototype. Development effort now moves to Stage 3, with EYE and its panel records retained as the upstream identification and evidence source.

### WHAT WE ESTABLISHED

- The planned process remains: EYE inspection -> manual Stage 2 preparation/de-framing -> Stage 3 thermal separation -> later material separation and recovery.
- Stage 2 will be performed manually for the current research demonstration. No Stage 2 robotic cell or automated panel-handling arm is part of this build.
- Stage 1 is not being removed from the Agastya system. Its automated sorting and hardware are deferred; panel identity, inspection evidence, and routing records remain useful inputs to later stages.
- Stage 3 is the immediate development focus. Its process records should describe measured inputs, calibrated process conditions, outputs, and material recovery, rather than claim success from an image-model prediction.
- Keep EYE as a laptop-hosted vision and record-keeping service. It does not control a heater, robot, or other hazardous actuator. The existing Stage 3 API requires traceable measurements and a completed Stage 2 record; it is a data/workflow interface, not a safety controller.
- A Stage 3 model is not selected yet. First define the process, collect repeatable measurements, and establish a simple measured baseline. Image AI can be evaluated later against those records if it answers a specific, measurable question.

### DAY 3 - WORKFLOW AND MEASUREMENT DEFINITION

- Map the manual transfer from Stage 2 into Stage 3, preserving the source panel/passport reference wherever material streams remain traceable.
- Draft the Stage 3 record around input material mass, station and operator identity, instrument and calibration reference, process temperature and time, output-stream masses, and completion or safety-hold status.
- Identify a batch/stream traceability gap before material from multiple panels is combined. Do not treat the existing per-panel passport as proof of batch-level mass balance unless those links are recorded.
- Separate planned measurements from assumptions. EYE imagery cannot supply material mass, calibrated temperature, process energy, or recovered purity.

### DAY 4 - BUILD APPROACH AND BOUNDARIES

- Keep Stage 2 manual and supervised for this prototype; record the completion and material handoff rather than attempting an under-budget robot build.
- Plan Stage 3 first as a documented workflow and instrumented data-capture station. Begin with a cold/dry-run of the records and operator sequence; this entry does not claim a thermal process trial has been performed.
- Do not begin active thermal processing until the equipment, materials, ventilation/emissions controls, guarding, emergency response, and qualified supervision have been reviewed for the actual lab setup.
- Use measured process and recovery data as the primary evaluation. Defer AI model selection until there are enough correctly linked, independently checked trials to justify it.
- Preserve the distinction between research demonstration and production recycling performance. Report only measured outcomes and their test conditions.

### CURRENT STATUS

- Decision recorded: Stage 2 robotics deferred; Stage 2 is manual for the current prototype.
- Focus recorded: Stage 3 process definition and measurement plan.
- Existing EYE/app work remains available for PC inspection, panel identity, and passport records; it is not an actuator or thermal-process controller.
- No Stage 3 hardware, active thermal trial, recovery result, or new model training is claimed by this logbook entry.

### OPEN FOR DAY 5

- Inventory available Stage 3 equipment and identify what can be measured with existing instruments.
- Draw the material flow and define how panel IDs, Stage 2 outputs, and Stage 3 batches/streams will be linked.
- Prepare a blank measurement sheet and run a cold/dry workflow test, including instrument and calibration fields.
- Review the actual site's safety and environmental controls with the responsible supervisor before any active thermal experiment.
- Revisit model choice only after the first verified process records exist; compare a transparent measured baseline before adding AI.
