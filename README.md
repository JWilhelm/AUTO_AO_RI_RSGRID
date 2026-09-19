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

## Reproducing Figure 2

`FIGURE_2_REFERENCE_VALUES.json` contains the 100 TensorGW reference energies
for *GW100* and the reference values used for Si45H56 and Si293H172. Run

```console
python3 evaluate_figure2.py
```

from the repository root. The script uses only the Python standard library,
parses all archived CP2K outputs, checks their coverage and SCF total energies,
and writes:

- `FIGURE_2_VALUES.csv`: all 146 plotted coordinates;
- `FIGURE_2_RECREATED.svg`: the recreated six-panel figure;
- `FIGURE_2_REPRODUCTION.json`: coverage and consistency diagnostics.

The *GW100* ordinate is the mean absolute error over the available molecules;
the two nanocrystal ordinates are absolute errors. Values below 1 meV are
displayed at 1 meV on the logarithmic axes, while the unfloored values remain
available in the CSV file.

The Si293H172 values of -6.029 eV (HOMO) and -2.657 eV (LUMO) are the
provisional non-Tensor reference used in the manuscript. No independent
TensorGW or full-grid calculation is available for this system. The reference
file therefore also records the six completed calculations with the largest
tested RI-RS mesh (`RS_AO_RATIO=10`); none gives the fixed HOMO/LUMO pair
exactly, so the provisional reference must not be interpreted as one unique
largest-mesh calculation.

## Figure 3 reproduction\n\n`Figure_3_reproduction/` contains the 100 GW100 TensorGW references, the\nSi45H56 TensorGW reference, the complete published data table, and a script\nthat recomputes all 648 Figure-3 points from the archived outputs. See its\nREADME for the exact command and the explicitly documented Si293H172\nreference limitation.
