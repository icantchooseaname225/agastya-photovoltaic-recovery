# Integrated process accounting model

## Scope

This is a small, auditable Stage 4 stream-accounting implementation with source-specific inventory normalization. It is not an integrated physics solver and does not simulate disassembly, breakage, liberation, particle charging, or separator trajectories. Those stages have no measured geometry, feed properties, or operating data in the project.

## Files

- `agastya_accounting.py` — standard-library Python model.
- `inputs/reference_inventory.json` — three separate literature-reference cases and intentionally null measured-process fields.
- `results/normalized_inventory_results.json` — generated output.

## Equations and units

- Ag mass in a stream: `m_Ag(g) = M_stream(kg) × Ag_grade(wt%) / 100 × 1000`.
- Mass yield and Ag recovery are stored as fractions from 0 to 1 when calculable.
- Grade remains wt%.
- Mass residual: feed mass minus all output stream masses and documented mass loss.
- Ag residual: feed Ag mass minus all output stream Ag masses and documented Ag loss.
- Reference conversions: `mg/kg ÷ 1000 = g/kg`; `g/t ÷ 1000 = g/kg`.

## Reproduce

From this folder:

```powershell
python .\agastya_accounting.py --input .\inputs\reference_inventory.json --output .\results\normalized_inventory_results.json
python .\agastya_accounting.py --self-check
```

Missing mass, grade, or documented loss remains unknown; the model will not infer zero or force a closed balance. The self-check runs a synthetic fixture strictly to verify formulas. The generated reference file lists 0.300 g, 0.600 g, and 0.630 g per normalized 1 kg feed, while all measured AGASTYA process metrics are `null`.
