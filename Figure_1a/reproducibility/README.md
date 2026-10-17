# Current Figures 1 and 2

The current Figure 1 presents 32 PBE/G0W0 gap coordinates; Figure 2 presents 64 HOMO/LUMO coordinates from the same CP2K calculations. The two panel sets contain identical raw calculation files; they are not independent reruns. The source snapshots are the current manuscript's `ao_frontier_validation_results.tex` and `ao_frontier_orbital_energies.tex`.

Run `python3 Figure_1a/reproducibility/verify.py` from the repository root. It reparses the raw CP2K output and the 99 GW100 aug-TZVP references, recomputes the gap and orbital MAEs and Si45H56 energies, and checks every plotted manuscript coordinate. It does not require Matplotlib.
