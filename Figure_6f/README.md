# Figure 6f

Current manuscript Figure 6(f): GW100 $G_0W_0$ @ PBE/def2-QZVP, $R_{\mathrm{RS}}=5$ Å, RI-RS grid size $N_{\mathrm{RS}}=\alpha N_{\mathrm{AO}}$ with $\alpha=2,\ldots,13$. Each `calculations/rsNN/<molecule>/` directory contains the original CP2K `input.inp`, `output.log`, and `bandstructure_SCF_and_G0W0` for one accepted molecule and grid size. There are 100 molecules per grid size, 1200 accepted calculations in this panel.

Production sources: 597/600 on Noctua 2 and Otus. The original inputs retain their absolute cluster paths for provenance. Exact SCF-WFN restarts, geometries, basis and potential files are shared in [`Figure_6a/reproducibility/assets/`](../Figure_6a/reproducibility/assets/). [`Figure_6a/reproducibility/reproduce.py`](../Figure_6a/reproducibility/reproduce.py) checks every file hash, SCF restart, final CP2K marker, orbital identity, fitting error, evaluation count, and the plotted MAE and median coordinates.
