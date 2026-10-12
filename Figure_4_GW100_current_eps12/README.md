# Current Figure 4(a--f): GW100

The current manuscript uses aug-SZV-MOLOPT-GTH-tier-2 RI-RS results at 0.5, 3, and 5 Å with `EPS_FILTER=1e-12`. Their raw files are under each `Figure_4[a-f]/current_eps12/ri<RI>_rs<RS>/<molecule>/`. The six paired panels share three sets of calculations. `molecule_errors.csv` lists every normal run, its original Noctua path, repository-relative path, SHA-256 hashes, frontier energies and signed errors against the TensorGW reference. The reference outputs are in `TensorGW_Calculations/GW100_TensorGW/`, with four updated references in `Figure_4_GW100_References/`.

Of 10,800 planned molecule/grid combinations, 10,710 completed normally and appear in the 216 manuscript means. The remaining 90 combinations are listed in `missing.csv`; each point therefore covers 96--100 molecules. Four LiH results at 0.5 Å and RS/AO=2 have a negative quasiparticle gap and remain as documented grid diagnostics. `aggregate.csv` gives pointwise mean errors, `plot_coordinates.csv` records the manuscript values, and `summary.json` gives coverage. `python3 Figure_4_GW100_current_eps12/reproduce.py` checks raw hashes, CP2K end markers, input filters, orbital edges, reference hashes, all aggregate values and all plotted coordinates.

Older `EPS_FILTER=1e-7` runs directly under `Figure_4a`--`Figure_4f` are retained for provenance but are not the current manuscript points.
