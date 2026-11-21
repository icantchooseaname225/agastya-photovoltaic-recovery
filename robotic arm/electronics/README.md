# Stage 2 bench electronics package

This is a low-load manual-jog teaching interface, separate from the future process arm and AGASTYA-EYE.

## Included artifacts

- STAGE2_ARM_BENCH_DEMO.ino — open-loop four-axis manual-jog scaffold, not compiled.
- STAGE2_BENCH_ARM_PIN_MAP.csv — provisional Mega pin assignments.
- STAGE2_ELECTRONICS_DESIGN_BASIS.md — boundary and assumptions.
- stage2_bench_status_architecture.svg — status and separate stop-power concept.
- spice/NC_LOOP_STATUS_LTSPICE.cir — single-channel LTspice-compatible example netlist with open/closed transient measurements.
- spice/nc_loop_status_model.mjs — executed DC divider model.
- spice/outputs/NC_LOOP_SIMULATION.csv and JSON — run outputs.
- spice/outputs/LTSPICE_TRANSIENT_RESULTS.csv and JSON — batch measurements from LTspice 26.1.1.

The Node model returned approximately 0.00025 V for a closed status contact and 5.0 V for an open/tripped or broken loop. LTspice batch mode measured 0.00024999 V at 7 ms (modeled closed) and 4.99994993 V at 2 ms (modeled open). Those values describe the idealized circuit, not a measured Arduino input. A short-to-ground can mimic a healthy contact in this single-loop example.

The hardware E-stop and safety relay must independently interrupt a separately fused, correctly rated servo supply. The Arduino GPIO only reports status and inhibits the classroom sketch. It is not a safety controller. No wiring has been assembled, the Arduino sketch has not been compiled, and no motor rail has been energized.
