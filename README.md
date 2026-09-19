# Calculations of manuscript "Optimization of Gaussian basis sets and real-space grids for efficient low-scaling GW calculations"
This repository contains the calculation inputs and outputs
used for Figures 1–3 of the manuscript.

- Every point directory is named by the plotted method/parameter combination.
- Every GW100 point contains 100 molecule directories.
- `EXCLUDED.txt` is used only where a calculation is genuinely undefined
  (for example, a tabulated RI basis does not exist); no output is fabricated.
- Calculation directories contain only `input.inp` and `output.log`. Submit
  scripts, restart files, and Slurm stdout/stderr files are excluded.
- Identical files used in different figures are hard-linked in the worktree;
  Git also stores identical blobs only once.

`PROVENANCE.json` records the exact original Noctua directory and checksums for
every archived entry.

## Reproducing Figure 1(a,b)

The directories `Figure_1a/Reference_aug-TZVP-t1` and
`Figure_1b/Reference_aug-TZVP-t1` contain the same 99 conventional-GW
large-orbital-basis reference calculations used for both panels.  Xe is
represented by `05_Xe/EXCLUDED.txt` because the required orbital basis is not
available.  Run

```console
python3 evaluate_figure1_ab.py
```

from the repository root to parse the archived CP2K outputs, recompute all 16
mean absolute errors in panels (a) and (b), and write
`FIGURE_1_AB_VALUES.csv`.
