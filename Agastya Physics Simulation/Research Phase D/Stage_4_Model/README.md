# Stage 4 model — sampling, assay, and accounting

## Purpose and status

Stage 4 is the measurement and accounting stage in the current charter. It does not dissolve, precipitate, electroplate, or refine silver. No AGASTYA sample or assay is recorded. The existing Phase B/C accounting implementation and tests are linked from the [research master report](../Research_Master_Report.md); this Phase D package adds a stream-level input template and a small, fail-closed reference calculator.

## Mechanism sequence

1. Register the run and parent-child stream lineage.
2. Weigh feed, every product, and documented losses using checked instruments.
3. Homogenize/split representative aliquots under a qualified lab plan; retain a sample and record aliquot mass.
4. Assay feed and all outputs using a laboratory-validated method for this PV matrix. Portable XRF may be screening only after matrix validation. ICP-OES/ICP-MS quantify elements in prepared solutions; digestion completeness, matrix recovery, limits, and uncertainty must be supplied by the laboratory. Elemental concentration alone does not identify chemical phase or establish metallic purity.
5. Calculate mass yield, Ag grade, Ag recovery, Ag balance, residual, and uncertainty as separate quantities.

## Equations

For each stream `i`, `m_Ag,i = M_i x_Ag,i`. Then `R_Ag = 100 m_Ag,target / m_Ag,feed`, `grade_Ag = 100 m_Ag,target / M_target`, and `mass_yield = 100 M_target / M_feed`. Total and Ag residuals use **all** measured streams plus documented losses. If a necessary value is absent, the corresponding output remains null/unknown.

For independent mass and assay standard uncertainties, `u²(m_Ag) = (x_Ag u_M)² + (M u_x)²`; include covariance when justified. Sampling variability is not removed by this formula and needs duplicate/representative sampling data.

## Assay stream template

Use [`assay_stream_template.csv`](assay_stream_template.csv). Confirm the receiving lab's accepted matrix and QA/QC before submitting any sample. Any chemical refining after assay is outside the AGASTYA process boundary and belongs to a qualified receiver.
