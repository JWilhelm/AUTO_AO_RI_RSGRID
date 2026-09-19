# Reproducing Figure 3

This directory contains the missing reference calculations and the complete
data path needed to recompute Figure 3 from this repository alone.

## Contents

- `references/GW100_TensorGW/<molecule>/input.inp` and `output.log`: the 100
  TensorGW reference calculations used for all GW100 mean absolute errors.
- `references/Si45H56_TensorGW/input.inp` and `output.log`: the TensorGW
  reference calculation used for the Si45H56 panels.
- `reference_values.csv`: HOMO, LUMO, and total-energy values parsed from the
  archived reference outputs.  The Si293H172 row is explicitly marked as the
  provisional non-Tensor reference used in the current manuscript.
- `published_values.csv`: the 648 numerical values plotted in the current
  manuscript, retained as the comparison target.
- `reproduce_figure3.py`: parses every Figure-3 output and reference, requires
  100/100 GW100 coverage, checks SCF total-energy consistency, recomputes all
  points, and writes two plots plus machine-readable comparison files.

## Run

From the repository root:

```bash
python -m pip install matplotlib
python Figure_3_reproduction/reproduce_figure3.py
```

Results are written to `Figure_3_reproduction/generated/`.

## Reference limitation

No independent Si293H172 TensorGW reference calculation was found in the
Noctua project archive.  The current manuscript uses the provisional values
HOMO = -6.029 eV and LUMO = -2.657 eV.  They are included so that the plotted
errors can be evaluated, but they are not presented as TensorGW results.

The repository's archived Si293H172 outputs independently reproduce all but 16
published points to within 1 meV.  The 16 material discrepancies are all in
panel (m), for `R_RS = 0.5 Å` and `N_RS/N_AO = 3, 4, 5, 9`, across all four
RI/AO ratios.  The reproduction script reports these differences rather than
silently substituting the published values.
