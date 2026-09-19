# GWP41 figure calculations

This repository contains the calculation inputs and scientific text outputs
used for Figures 1–3 of the manuscript.

- Top-level figure directories are named `Figure_1a` through `Figure_3r`.
- Every point directory is named by the plotted method/parameter combination.
- Every GW100 point contains the canonical 100 molecule directories.
- `EXCLUDED.txt` is used only where a calculation is genuinely undefined
  (for example, a tabulated RI basis does not exist); no output is fabricated.
- Calculation directories contain only `input.inp` and `output.log`. Submit
  scripts, restart files, and Slurm stdout/stderr files are deliberately excluded.
- Identical files reused by HOMO/LUMO panels are hard-linked in the worktree;
  Git also stores identical blobs only once.

`PROVENANCE.json` records the exact original Noctua directory and checksums for
every archived entry.
