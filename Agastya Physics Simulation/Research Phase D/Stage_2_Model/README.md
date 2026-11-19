# Stage 2 model — mechanical liberation and classification

## Purpose and status

Stage 2 prepares and characterizes particles from the Stage 1 cell-bearing feed. The present project provides no crusher/mill design, feed mass, material property, particle-size distribution, or liberation measurement. Fracture/DEM parameters cannot be set defensibly, so no breakage or liberation simulation was run.

## Model hierarchy

1. Measure and reconcile all feed and output masses.
2. Measure particle size distribution by mass and report the method/apertures.
3. Characterize particle shape, moisture, and material association on representative samples.
4. Determine whether Ag contacts are liberated or still attached to Si/Cu/polymer/glass.
5. Only then consider a population-balance, fracture, or DEM model that answers a specific question.

A sieve-cut calculation can predict a size split for a known PSD; it cannot infer Ag grade, Ag recovery, or liberation. Prior virtual lognormal-cut sweeps yielded 0–100% fines over assumed PSD/cut combinations and demonstrate parameter dependence, not equipment performance.

## Data template

Use [`size_fraction_measurement_template.csv`](size_fraction_measurement_template.csv). Blank means unknown. Do not copy published size cuts or silver-partition fractions into an AGASTYA result column.

## Required validation

Retain every size fraction and loss; compare the total mass balance; assay each fraction using a representative, lab-accepted method; and compare duplicate subsamples to quantify sampling variability. No Stage 2 AGASTYA result exists.
