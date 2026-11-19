# Stage 3 model — candidate electrostatic separation

## Purpose and current status

The current Stage 3 is an electrostatic separation candidate. The project has no separator geometry, field boundary conditions, representative feed, particle charge/conductivity distributions, humidity record, or assayed outputs. No electrostatic field, trajectory, DEM, or CFD solver was run. No temperature/reaction model is applicable to the current dry unit operation unless a specific measured thermal effect is established.

## Mechanism and candidate equations

For a specified dielectric and charge distribution, a field model may solve `E = −∇V` and, where volume charge is represented, `∇·(εE) = ρ_e`. A particle trajectory may then be represented in an inertial frame by `m dv/dt = qE + mg + F_drag + F_contact + F_image`; a rotating-frame model must state its centrifugal/Coriolis terms and constraints. Charge must evolve with an evidence-based corona/contact/induction/decay model, for example a schematic `dq/dt = I_charge − q/τ_decay`. These forms identify required physics; they are not a fitted AGASTYA model.

In a roll-type corona separator, insulating particles can retain corona charge and be held to the roll by image force, while conductive particles contacting the grounded roll can discharge and then respond to induction/field forces. Particle size, conductivity, shape, humidity, roll speed, electrode geometry, feed loading, and spark events affect trajectories. A conductive fraction is not a silver-only fraction: Ag-bearing particles can remain composite and Al/Cu/Si also respond.

## Inputs required before solving

Use [`electrostatic_model_inputs_template.csv`](electrostatic_model_inputs_template.csv). Record one row per output bin; repeat the run-wide settings on each row and give every bin a unique ID and role. At minimum obtain dimensioned geometry, voltage/polarity, roll and feed speeds, particle size/shape/density, moisture, conductivity and charge-to-mass distributions by class, humidity, field and grounding data, and splitter/bin geometry. Calibrated, weighed, assayed output fractions are needed for validation.

## External evidence boundary

Yang et al. (2019) report 94.37% “silver separation efficiency” for a specific needle-roll study; the accessible abstract does not define that metric or expose the full balance. de Souza & Veit (2023) report Ag/Al/Si co-concentration and a 38 kV, 75 rpm condition for their prepared scrap, but no mass-weighted Ag recovery or grade is available in the accessible abstract. Younes et al. (2013) experimentally/ numerically studied roll-type separator trajectories on PVC/Cu cable waste and showed humidity, size, speed, and sparks matter. These support physical plausibility and model requirements, not AGASTYA outputs.

## Chemistry and heat

No process reaction or deliberate heating is specified for current Stage 3, so thermodynamic equilibrium, reaction kinetics, and coupled thermal-reaction calculations are not warranted. The older hot-knife model belongs to optional upstream pretreatment and must remain separately labelled.
