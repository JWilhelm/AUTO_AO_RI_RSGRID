# Current Figure 3

The 50 current manuscript coordinates are checked against the archived CP2K outputs. The GW100 AUTO_RI values at RI/AO 2–5 use the RS/AO=7 slice shared with the historical Figure 4(c,d) archive; the 1 and 1.5 points use the matching Figure 3 production extension. Tabulated RI and corrected Si45H56 results use the sources recorded in `Plot_Figure_3/plot_figure_3.py`. The current manuscript data macros are snapshotted here.

Run `python3 Figure_3_reproducibility/verify.py` from the repository root. The script checks raw CP2K completion, paired TensorGW references and SCF energy consistency, then compares all 50 plotted coordinates with the manuscript source. It does not require Matplotlib.
