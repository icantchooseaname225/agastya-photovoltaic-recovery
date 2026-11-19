# Next research plan

The sequence below closes physical evidence gaps before spending effort on process simulation. Activities involving tools, heat, high voltage, cutting, or laboratory preparation require the project's ordinary safety review and appropriate supervision.

| Step | Work | Deliverable / gate | Stop condition |
|---|---|---|---|
| 1. Define feed | Select one traceable c-Si module lot; record module identity, architecture, age if known, condition, source, photos, and chain of custody. | Feed record and approved sample-handling/safety plan. | Unknown technology or unsafe/unapproved handling; segregate and resolve first. |
| 2. Stage 1 balance | Calibrate/check scale; weigh module and each routed component; document tare, residues, fragments, and losses. | Complete Stage 1 mass inventory and retained sample map. | Material balance cannot account for transfers/losses; repair method before next stage. |
| 3. Baseline assay | Discuss matrix and preparation with qualified lab; split representative samples; request blanks, standards, duplicates, spikes, reporting limits, and uncertainty. | Feed Ag grade with method, preparation, QA/QC, and uncertainty. | Lab cannot validate preparation/recovery or sample is not representative. |
| 4. Stage 2 characterization | Run controlled comminution/sieving trials; measure settings, feed/output masses, PSD, captured dust, and Ag by size class; characterize association/liberation. | Replicated size/Ag partition dataset. | No representative sampling or uncollected fines; redesign capture and split protocol. |
| 5. Stage 3 design definition | Document separator dimensions, electrodes, roll, splitter, voltage/polarity, speed, feed rate, grounding, environment, and safety controls. | As-built geometry and operating envelope. | Geometry/charge/safety limits unknown; do not parameterize a particle model. |
| 6. Stage 3 screening experiment | Use randomized/repeated settings with measured feed; log humidity and operational events; weigh and assay concentrate, middlings, rejects, and dust. | Full mass/Ag balance and repeatability dataset. | Any stream missing or assay QA/QC fails; no recovery comparison. |
| 7. Solver selection | Decide whether field/particle modeling answers a specified design choice; confirm license/cost; set calibration and withheld validation splits. | Model protocol with equations, parameters, mesh/time-step and acceptance criteria. | Inputs cannot be measured or independent validation data unavailable; defer solver. |
| 8. Model and validate | Calibrate only on training runs; compare predicted bin distributions/recovery proxies on withheld runs; document errors and sensitivity. | Versioned model, reproducible inputs/outputs, validation report. | Large/structured residuals or no improvement over simple baseline; revise or reject model. |
| 9. Route and impact decision | Obtain receiver requirements for the resulting concentrate; define downstream route and system boundary if evaluating environmental/economic outcomes. | Qualified acceptance criteria and separate downstream study scope. | No receiver or missing boundary data; make no purity/economic/environmental claim. |

## Minimum dataset for a first useful Stage 3 model

- One representative and assayed Stage 2 feed lot, with size/shape and Ag association by class.
- As-built separator geometry, electric potentials, polarity, grounding, roll speed and splitter positions.
- Environmental logs and feed rate; particle moisture, density and conductivity/charge-decay measurements.
- Replicated and randomized run data with every output-bin and dust mass plus corresponding assay.
- Predeclared calibration/holdout split and quantitative model-error acceptance criteria.

Until that dataset exists, the correct deliverable is a measurement plan and traceable blank model inputs, not a simulated recovery value.
