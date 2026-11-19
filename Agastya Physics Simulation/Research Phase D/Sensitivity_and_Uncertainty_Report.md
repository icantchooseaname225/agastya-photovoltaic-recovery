# Sensitivity and uncertainty report

## Purpose

This report separates arithmetic sensitivity from uncertainty about the real process. The current project has no measured feed or stream outcomes, so a numerical sensitivity sweep of recovery, grade, throughput, or energy would require invented inputs. No such sweep is reported.

## Calculable reference arithmetic

For a source concentration `C` in mg/kg or g/t, the normalized Ag inventory is `m_Ag(g) = C × M_feed(kg) / 1000`. The conversion is linear in feed mass. At the illustrative 1 kg basis:

| Source case | Source value | Normalized inventory | Interpretation |
|---|---:|---:|---|
| Review-derived composition scenario | 300 mg/kg (300 ppm) | 0.300 g Ag | Denominator/provenance unresolved; not an AGASTYA assay |
| Dias publisher-abstract value | 600 g/t | 0.600 g Ag | Study-specific feed; full basis not audited here |
| Secondary excerpt | 630 g/t | 0.630 g Ag | Unresolved wording; do not combine with 600 g/t |

Changing the normalized feed basis from 1 kg to 2 kg doubles these arithmetic inventories; it does not change a grade, recovery, or actual process behavior. These values are deliberately separate cases rather than a range or probability distribution.

## Uncertainty sources

| Quantity | Current uncertainty source | How to quantify when data exist |
|---|---|---|
| Feed Ag inventory | Literature denominator, module generation, module heterogeneity, sampling and assay bias | Representative sampling; independent assay splits; certified/reference materials; lab uncertainty and detection/reporting limit |
| Stage 1 routing | Scale resolution, material left on fixtures, broken glass/debris, route misclassification | Calibration checks, tare/blank checks, repeat weighings, documented loss collection and uncertainty |
| Stage 2 size partition | Feed variability, sieve cut/shape bias, dust loss, equipment repeatability | Replicate runs, sieve checks, weighed dust capture, replicate PSD and Ag assay by size class |
| Ag liberation/association | Particle heterogeneity and method resolution | Microscopy/elemental mapping or other validated method; replicate representative splits |
| Stage 3 capture | Charge variation, humidity, particle shape/conductivity, feed rate, field geometry, sparks, bin cut and run-to-run variability | Randomized replicated trials, operating logs, bin mass and assay; measure field/charge proxies; hold out runs for model validation |
| Stage 4 assay/accounting | Split representativeness, preparation/digestion recovery, calibration and instrumental repeatability | Lab QA/QC, blanks, standards, duplicates, matrix spikes, validated preparation, uncertainty and reporting limits |
| Legacy thermal calculation | Assumed all-EVA sensible heating, heat-loss multiplier, solar hours/efficiency and panel dimensions | Instrumented temperature/power/time trials and measured coupon mass/adhesion; revalidate model form |

## Propagation once measurements exist

For feed mass `M_f`, feed Ag mass fraction `x_f`, target mass `M_t`, and target Ag mass fraction `x_t`,

- `m_Ag,f = M_f x_f`
- `Y_mass = M_t / M_f`
- `G_Ag,t = x_t`
- `R_Ag = M_t x_t / (M_f x_f)`

For independent uncertainties, a first-order relative approximation for recovery is
`(u_R/R)^2 ≈ (u_Mt/M_t)^2 + (u_xt/x_t)^2 + (u_Mf/M_f)^2 + (u_xf/x_f)^2`. This is only a planning formula; paired sampling, shared calibration, and correlated mass/assay errors require covariance terms. Balance residual uncertainty should be propagated from all measured input, output, assay, and documented-loss terms. Report absolute and relative residuals with the chosen denominator.

## Sensitivity priorities

1. **Feed grade and sample heterogeneity:** recovery is a ratio of assayed Ag masses. A biased feed split can dominate the result even if the separator is repeatable.
2. **Fine-particle capture and dust collection:** omitted fines can change both the denominator and apparent product recovery.
3. **Product boundary:** define whether target is the electrostatic concentrate, a size fraction, or a downstream receiver product before calculating grade or recovery.
4. **Charge and moisture state:** electrostatic outcomes may change with humidity, surface condition, particle class, and operating history; do not use one point value for a distribution without measurement.
5. **Thermal model assumptions:** prior workbook energy/throughput estimates are highly sensitive to assumed heat multiplier, available energy, area, target temperature, and cycle time; they are not current-stage predictions.

No Monte Carlo distribution is assigned because input distributions and correlations are absent. A future uncertainty model should use measured replicate data and lab uncertainties, preserve source-specific literature cases, and be checked against an independent holdout trial.
