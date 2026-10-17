# Figure 6 data and reference energies

Panels a–c contain 92 molecules at each of 12 grid sizes with PBE0/def2-TZVP; panels d–f contain 100 molecules per grid size with PBE/def2-QZVP. The cluster radii are 0.5, 3 and 5 Å in panel order.

`aggregate.csv` contains HOMO/LUMO mean and median absolute errors in meV. `molecule_errors.csv` contains the individual errors and three-centre fitting errors. `reference_pbe0_def2_tzvp.csv` and `reference_pbe_def2_qzvp.csv` give the reference orbital energies in eV and the corresponding orbital indices. The latter contains the FHI-aims reference values and marks the five molecules excluded from HOMO statistics.

`assets/` contains the 192 SCF wavefunctions, 100 XYZ geometries, and basis/potential files. Match the filenames to the paths requested in each CP2K input when preparing a rerun.
