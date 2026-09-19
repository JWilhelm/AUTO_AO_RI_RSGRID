# AUTO_AO_RI_RSGRID

Calculation inputs and outputs for Figures 1–3 of the manuscript
"Optimization of Gaussian basis sets and real-space grids for efficient
low-scaling GW calculations."

## Repository layout

- `Figure_1a/`–`Figure_1f/`, `Figure_2a/`–`Figure_2f/`, and
  `Figure_3a/`–`Figure_3r/` contain the raw CP2K inputs and outputs.
- `Plot_Figure_1/`, `Plot_Figure_2/`, and `Plot_Figure_3/` each contain one
  plotting script, the generated figure, and the corresponding numerical
  values or reference data.
- `PROVENANCE.json` records the original Noctua directory and checksums for
  every archived calculation.

Every point directory is named by the plotted method/parameter combination.
Every GW100 point contains 100 molecule directories. `EXCLUDED.txt` is used
only where a calculation is genuinely undefined; no output is fabricated.

## Reproduce the figures

Run the scripts from the repository root:

```console
python3 Plot_Figure_1/plot_figure_1.py
python3 Plot_Figure_2/plot_figure_2.py
python3 Plot_Figure_3/plot_figure_3.py
```

Figures 1 and 3 require Matplotlib. Figure 2 uses only the Python standard
library and writes an SVG.

The Figure 1 script parses all six panels. Panels 1(a,b) use the archived 99
conventional-GW aug-TZVP-t1 reference calculations; Xe is marked as excluded
because the required orbital basis is unavailable.

The Figure 2 and Figure 3 reference files document the provisional
Si293H172 HOMO/LUMO reference values used in the manuscript. No independent
TensorGW or full-grid reference calculation is available for that system.
