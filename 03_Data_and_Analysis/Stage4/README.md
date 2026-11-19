# Stage 4 route mass-balance sensitivity model

Run `stage4_route_mass_balance_sensitivity.py` with the available Python runtime to reproduce two transparent calculations:

1. Convert the paired Saffarian et al. (2026) tap-water rougher flotation result (97.55% Ag recovery, 32.2× upgrade on prepared delaminated/ground cell feed) into a derived mass pull, R/U = 3.0295%. A 1 kg feed scale is used only to express the ratio as 30.30 g concentrate and 969.70 g tails; it does not set an AGASTYA feed basis. The silver balance is normalized to one input unit because no AGASTYA assay is known.
2. Sweep algebraic values for `e`, the fraction of silver in a separately accepted ECS product, and `p`, the fraction sent to flotation. The break-even relationship is `R_total = e + p*r_f` and `r_f_required = (0.9755-e)/p`. The 0.05 increments are a mathematical sensitivity grid; they are not ECS measurements or forecasts.

The script writes a JSON run record, CSV sensitivity grid, and SVG threshold plot to `outputs/`. The literature benchmark is specific to the paper's prepared feed. It does not predict performance on whole panels, Stage 3 laminate, or an AGASTYA feed.

Eddy-current separation stays in the route comparison as a candidate. Its Ag partition, mass split, product quality, and interaction with flotation are unknown. A matched-feed experiment with complete stream assays and balance closure is required. See the [flotation reagent feasibility report](../../01_Research/Stage_4_Flotation_Reagent_Investigation/AGASTYA_FROTH_FLOTATION_REAGENT_FEASIBILITY_REPORT.md) and the [Stage 4 reassessment](../../Build%20Files%20and%20Steps/Stage%204/STAGE4_ARCHITECTURE_REASSESSMENT_2026-11-19.md).
