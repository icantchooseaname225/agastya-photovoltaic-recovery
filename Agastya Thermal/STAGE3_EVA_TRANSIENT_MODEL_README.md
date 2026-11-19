# Stage 3 idealized EVA transient model

The executable Python model in `stage3_eva_transient_1d.py` solves one-dimensional transient conduction through a homogeneous 0.5 mm EVA slab. It uses a fixed 100 °C boundary at one face, an insulated opposite face, a 25 °C uniform initial condition, and literature-based constant thermal properties: k = 0.34 W/(m·K), density = 951 kg/m³, and heat capacity = 1,400 J/(kg·K). These are modeling inputs, not measurements of an AGASTYA coupon.

The explicit finite-difference calculation writes temperature profiles, energy summaries, run inputs/derived values, and an SVG into `stage3_eva_model_outputs/`. It is useful for checking the effect of a stated thermal boundary on a thin idealized layer. It does not simulate the hot knife, composite PV stack, temperature-dependent EVA, contact resistance, foam roller, adhesive fracture, delamination quality, energy use of a machine, or safe process conditions.

No lab sample or thermal station was present, so the model is unvalidated and must not be used as a hot-knife setpoint or operating procedure. See the limitations and validation requirement in `stage3_eva_model_outputs/model_summary.json`.

Run using the available Python runtime, from this folder:

`python stage3_eva_transient_1d.py`

No third-party package is required.

The EVA properties come from the material table in Tomšič et al., *Advanced Theory and Simulations* (2025; first published 13 December 2024), DOI [10.1002/adts.202401026](https://doi.org/10.1002/adts.202401026). The paper models operating PV-module temperatures; its values are used here only as explicit illustrative constants for EVA. It does not model thermal delamination.
