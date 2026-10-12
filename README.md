# GWP41 figure calculations

CP2K inputs and raw outputs for the **current** manuscript Figures 1--5 are grouped as `Figure_1a`, `Figure_1b`, ..., `Figure_5r`. Each panel directory has a short README. Paired HOMO/LUMO panels contain byte-identical copies of the underlying calculations so a panel can be inspected on its own; they do not represent independent reruns. The repository retains older campaigns in their original locations, clearly separated from the current series.

| Current panels | System and plotted quantity | Raw calculations and reference |
| --- | --- | --- |
| Figure 1(a--d) | GW100 and Si45H56 frontier-orbital energies, initial versus optimized AO bases | `Figure_1a`--`Figure_1d`; GW100 aug-TZVP reference in each GW100 panel |
| Figure 2(a--d) | PBE and G0W0 gap errors/values from the same calculations | `Figure_2a`--`Figure_2d`, byte-identical to Figure 1(a--d) |
| Figure 3(a--d) | GW100 and Si45H56 RI-basis convergence | `Figure_3a`--`Figure_3d`; TensorGW/reference outputs already stored with the established Figure 3 archive |
| Figure 4(a--f) | GW100 RI-RS grid convergence, aug-SZV tier 2 | **Current** `Figure_4a/current_eps12`--`Figure_4f/current_eps12`, 10,710 normal molecule calculations; `Figure_4_GW100_current_eps12/` documents 90 missing molecule/grid combinations. The older data at the roots of `Figure_4a`--`Figure_4f` use a different filter and are historical. |
| Figure 4(g--ad) | Si45H56, Si293H172, H24P64 and H60P400 grid convergence | `Figure_4g`--`Figure_4ad`; 864 panel coordinates and source check in `Figure_4_archived_panels/` |
| Figure 5(a--f) | GW100 grid convergence, aug-DZVP tier 2 | `Figure_5a`--`Figure_5f`; all 10,800 molecule calculations and 100 TensorGW references are also in `Figure_5_GW100/` |
| Figure 5(g--j) | Si45H56, 0.5 and 3 Å | `Figure_5g`--`Figure_5j`; 72 historical calculations with `EPS_FILTER=1e-7` and the matching historical TensorGW reference (−7.194/−1.506 eV) |
| Figure 5(k,l) | Si45H56, 5 Å | `Figure_5k`, `Figure_5l`; 36 calculations with `EPS_FILTER=1e-12` and their matching TensorGW reference (−7.191/−1.502 eV) |
| Figure 5(m--r) | H24P64, 0.5/3/5 Å | `Figure_5m`--`Figure_5r`; 108 calculations with `EPS_FILTER=1e-12` and TensorGW reference (−5.998/−2.353 eV). At 0.5 Å and RS/AO=7, the four plotted outputs use Tikhonov 1e-5 instead of 1e-8. |

The filter and basis settings are not identical across every series. Each `input.inp` is authoritative for its point. In particular, Figure 5(g--j) and Figure 5(k,l) must not be described as one uniform `EPS_FILTER=1e-12` series. Figure 4(g,h) retains `EPS_FILTER=1e-7`; Figure 4(i--l) uses `1e-10`; Figure 4(a--f) and 4(s--x) use `1e-12`. H60P400 uses a provisional internal RI-RS reference. See the panel README files for the reference of each series and the remaining panels' settings.

## Reproduce the plotted values

Run from the repository root:

```console
python3 Plot_Figure_1/plot_figure_1.py --output-dir /tmp/figure1
python3 Plot_Figure_3/plot_figure_3.py --output-dir /tmp/figure3
python3 Figure_4_GW100_current_eps12/reproduce.py
python3 Figure_4_archived_panels/reproduce.py
python3 Figure_5_GW100/Analysis/reproduce.py
python3 Figure_5_cluster_analysis/reproduce.py
```

The first two plot scripts calculate their CSV before plotting and require Matplotlib for PNG output. The Figure 4/5 audit scripts use only the Python standard library. The `Figure_4_GW100_current_eps12/molecule_errors.csv` file records all 10,710 inputs, outputs, hashes, molecule energies, reference energies and errors. Its `aggregate.csv` and `plot_coordinates.csv` record all 216 current Figure 4(a--f) points; `missing.csv` lists the 90 unfinished combinations rather than treating them as zero. `Figure_4_archived_panels/plot_coordinates.csv` records 864 current Figure 4(g--ad) points. `Figure_5_cluster_analysis/points.csv` gives the two plotted values, raw hashes, filters, Tikhonov value and matching TensorGW reference for each of 216 cluster calculations. `Figure_5_GW100/Analysis/reproduce.py` independently verifies its 10,800 molecule outputs, 100 references and 216 mean-error coordinates.

Figure 1(a--d), Figure 2(a--d), and Figure 3(a--d) were recomputed from the archived outputs and compared with the current manuscript: 64 Figure 1 frontier coordinates, 32 Figure 2 gap coordinates, and 50 Figure 3 coordinates matched. Figure 4(g--j) initially had 81 plotted coordinates differing by 1--5 meV from the archived CP2K outputs; the manuscript was aligned to the verified raw values. All current Figure 4 and Figure 5 coordinates now match their respective audit data.

Historical extra panels `Figure_1e/f` and `Figure_3e/f` remain in the repository but are not panels of the current manuscript. `Historical_Figure_3/`, `Filter_Controls/`, `Fixed_References/`, `TensorGW_Calculations/`, and `PROVENANCE.json` preserve the earlier archives and specialized controls. They were not deleted or substituted for the current point-level sources.
