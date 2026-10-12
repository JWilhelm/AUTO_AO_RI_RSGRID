# Current Figure 4(g--ad)

These 24 panels use the pre-existing raw input/output trees in `Figure_4g`--`Figure_4ad`. They cover Si45H56, Si293H172, H24P64 and H60P400 at 0.5, 3 and 5 Å. Their filters and reference choices differ by system; inspect each `input.inp` and the repository README. The H60P400 reference is provisional.

`plot_coordinates.csv` records the 864 current manuscript points. Run `python3 Figure_4_archived_panels/reproduce.py` from the repository root to parse the raw CP2K outputs and reference calculations and compare each plotted coordinate. The audit found and corrected 81 Figure 4(g--j) manuscript values that had differed by 1--5 meV from the archived output; all 864 values now match.
