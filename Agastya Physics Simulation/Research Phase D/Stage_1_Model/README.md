# Stage 1 model — disassembly and component routing

## Purpose and status

Stage 1 establishes a traceable parent module and routes its components. At present, no physical AGASTYA module, measured composition, disassembly yield, or calibrated mass record is available. This stage can be represented first by a material-accounting model; an FEA or machine model is not justified because no tool geometry, loads, or machine design is specified.

## Balance model

For one registered parent panel:

`r_m = M_parent − (M_glass + M_hardware + M_cell_laminate + M_debris + M_documented_loss)`

Every output receives a unique child stream ID and parent ID. Report the residual `r_m`; do not assign it to an unknown component. Ag partition requires representative assays of all streams, not visual inspection or color.

## Inputs needed

Use [`component_routing_template.csv`](component_routing_template.csv) to record panel nameplate/photos, confirmed c-Si technology and construction, source/owner and permission, calibrated mass/dimension measurements, disassembly sequence, all stream masses, debris capture, and a sample/assay plan if an Ag balance is intended.

## Outputs and checks

Output stream register, total mass residual, lineage, and (only if measured) Ag mass by stream. No Stage 1 simulation has been executed. Thermal delamination is optional pretreatment in legacy documents and is not included in this stage model.
