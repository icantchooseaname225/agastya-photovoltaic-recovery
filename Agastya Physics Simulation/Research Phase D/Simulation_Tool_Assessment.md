# Simulation tool assessment

**Environment inspected:** Windows PowerShell, CPython 3.14.4. NumPy, pandas, and openpyxl were present. SciPy, Cantera, DWSIM, OpenFOAM, and gmsh executables/modules were not found in the checked environment. No solver account or license was authenticated. This is a local availability snapshot, not a guarantee about the user's other machines or accounts.

## Fit by question

| Tool | Best fit for AGASTYA question | Cost/access and current state | Inputs / compute | Outputs and validation burden | Decision |
|---|---|---|---|---|---|
| Python standard library | Reproducible balances, unit conversions, audit trail, parameter bookkeeping | Available locally; no added license | Measured masses, assays, units; negligible compute | Deterministic tables/JSON; verify formulas and reconcile to hand calculation | **Use now** for Stage 4 bookkeeping; implemented in Phase D |
| NumPy / pandas / openpyxl | Data handling, uncertainty summaries, existing workbook inspection | Installed locally; no paid account required here | Measured data; low to moderate compute | Tabular results; validate transformations, units, missingness and independent spot checks | Use when measured data arrive; avoid probabilistic runs until distributions are supported |
| Google Colab | Shared Python notebooks and lightweight numerical scripts | Hosted free tier exists; resource availability, usage limits, and runtime are dynamic (FAQ notes availability-dependent limits) | Python; cloud session, commonly CPU, resource availability varies | Reproducible notebook possible, but it is not a dedicated electrostatic solver; pin code/data and export artifacts | Optional convenience, not a physics capability |
| SimScale | Browser CFD/FEA; possible field/thermal analyses depending plan | Public pricing page lists Community constraints and plan-specific solver access; no AGASTYA account verified | Geometry, mesh, material models, boundary conditions; cloud compute quotas | Field/flow/thermal outputs; requires mesh/time/energy convergence and physical validation. Specialized electromagnetics availability is plan dependent | Recheck exact solver/plan before use; no free access assumption for a needed solver |
| COMSOL Multiphysics + Particle Tracing | Charged particle trajectories under defined fields/forces | Commercial; module/license not available in this workspace | Dimensioned separator, field/electrode potentials, particle size/mass/charge, drag/contact/charge decay, air properties; substantial mesh/trajectory runs | Trajectories and capture zones. Must validate field, charge and bin split against AGASTYA measurements; sparks/contact/tribocharging may exceed simple one-way particle tracing | Strong candidate only after experimental characterization and a defined decision question |
| Ansys Maxwell / Student | Electromagnetic field solutions; student page currently lists student suite and limits | Free educational option advertised; local install/account not verified; student licensing/model limits apply | Electrode/roll geometry, voltage, dielectric/electrical properties; modest-to-heavy FEM | Electric field/potential. Does not alone predict granular particle capture; couple to particle model and validate | Consider for field solution if current student license and geometry are confirmed |
| OpenFOAM | Airflow/continuum CFD if separator airflow materially affects particles | Open source; not installed in checked environment | CAD/mesh, flow properties, boundary conditions; moderate/high CPU | Flow field; a custom particle/electrostatic coupling is required. Validate velocity and particle response | Defer unless air motion is measured as important |
| FEniCSx | Custom PDE/FEM field, heat, or structural model | Open source; not installed | Equations, mesh, coefficients, boundary conditions; custom implementation | Flexible fields/temperatures/stresses; high development and verification burden | Useful only if a custom governing equation is justified |
| DWSIM | Process-flow material/energy bookkeeping and unit operations | Open source; not installed. Current docs show standard unit operations including balance/separation examples | Stream definitions and component property model; low-to-moderate compute | Flowsheet balance; no granular electrostatic trajectory physics | Not needed now; Python accounting is simpler and more transparent |
| Cantera | Reaction thermodynamics, kinetics, and transport | Open source; not installed | Species, phases, reaction mechanism, temperatures, pressure | Chemical state/kinetics; no current AGASTYA stage requires reacting chemistry | Not applicable to current dry stages; reassess only if an approved chemical stage is added |

## Decision matrix against the project

| Candidate simulation | Decision readiness | Main blocker | Minimum gate before model run |
|---|---|---|---|
| Stage 1 digital material balance | Ready as a schema, not a measured run | No identified panel and measured component masses | Sample ID, panel technology, calibrated mass measurements, documented losses |
| Stage 2 comminution / size distribution | Not ready for performance prediction | No actual feed, equipment, PSD, liberation, or assay | Characterized lot and replicated mass/PSD/Ag association data |
| Stage 3 electrostatic field/particle tracking | Not ready | No separator design, field/charge data, or particle-property distributions | Dimensioned geometry; field and charge/trajectory measurements; assayed bins |
| Optional thermal pretreatment | Historical assumed model only | No observed temperature history, force/adhesion measurement, or trial | Instrumented coupon trials and measured material properties; separate from Stage 3 |
| Stage 4 balances | Formula-ready | No physical streams or assay values | Representative splits and lab-validated assays |

## Recommended sequence

1. Use the existing Python implementation as a blank, traceable Stage 4 schema and load only measured values.
2. Perform a mass and material-characterization trial before buying simulation capacity. Confirm feed technology and retain all fractions.
3. Obtain a vendor/manufacturer drawing or measure the Stage 3 separator. Record electrode shape, gaps, roll, splitter, voltage, speed, feed rate, polarity, humidity, grounding, and safety limits.
4. Measure size, shape, moisture, bulk density, conductivity or charge-decay proxy, and output-bin distributions. Ask the assay lab to confirm matrix preparation and QA/QC.
5. Decide whether COMSOL/Ansys field and particle models answer a concrete design question. If yes, document solver version, license, mesh, time-step, convergence, coupling assumptions, and validation data. A software result without an observed comparison is not validation.

No solver, cloud job, external account, or paid service was invoked during Phase D. Public product statements may change; source links and checked date are in the evidence register.
