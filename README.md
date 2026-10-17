# GWP41 figure calculations

CP2K inputs and raw outputs for the **current** manuscript Figures 1--6 are grouped as `Figure_1a`, `Figure_1b`, ..., `Figure_6f`. Each panel directory has a short README. Paired HOMO/LUMO panels contain byte-identical copies of the underlying calculations so a panel can be inspected on its own; they do not represent independent reruns. Shared references, SCF restarts and reproducibility scripts are inside the relevant numbered panel directories.

The `input.inp` files have been updated for the CP2K public `master` input schema at commit `08825b921571435c7155122cf567393533eeb2ca` (17 October 2026). Obsolete grid-initialization and per-atom process options were removed from 60,974 inputs; the unchanged output files were produced with the historical inputs, available in Git at commit `768b14d59d5870e92a01ca9bcd544a9e3a9af84f`. [`Figure_1a/reproducibility/public_master_input_migration_20261017.csv`](Figure_1a/reproducibility/public_master_input_migration_20261017.csv) records the old and updated SHA-256 hashes and historical settings for every changed file. This is an input-compatibility update, not a claim that the public code yields identical numerical results: 22,710 historical inputs selected pivots using the scaled, regularized matrix $D'_{ll'}$, whereas public `master` selects using $D_{ll'}$. A further 2,387 historical inputs requested 250 initial grid candidates per AO function, whereas public `master` uses at least `max(30, 2 RS_AO_RATIO)`. The original cluster paths in many inputs still need relocation or access to the same files before a new run.

Three [Noctua 2 spot checks](Figure_1a/reproducibility/public_master_spotcheck_20261017/README.md) with public `master` completed normally. One reproduced the published GW HOMO/LUMO values to 0.001 eV; the other two differed by up to 0.475 eV. Their new raw outputs and the historical comparison are included. The spot checks used a different parallel layout than the historical runs and do not establish the cause of each difference.

| Current panels | System and plotted quantity | Raw calculations and reference |
| --- | --- | --- |
| Figure 1(a--d) | GW100 and Si45H56 PBE and G0W0 gap errors/values, initial versus optimized AO bases | `Figure_1a`--`Figure_1d`; GW100 aug-TZVP reference in each GW100 panel |
| Figure 2(a--d) | PBE and G0W0 HOMO/LUMO errors/energies from the same calculations | `Figure_2a`--`Figure_2d`, byte-identical to Figure 1(a--d) |
| Figure 3(a--d) | GW100 and Si45H56 RI-basis convergence | `Figure_3a`--`Figure_3d`; shared TensorGW references in `Figure_4a/reproducibility/tensor_references/` |
| Figure 4(a--f) | GW100 RI-RS grid convergence, aug-SZV tier 2 | `Figure_4a/current_eps12`--`Figure_4f/current_eps12`, all 10,800 molecule calculations and 216 complete aggregate points. |
| Figure 4(g--ad) | Si45H56, Si293H172, H24P64 and H60P400 grid convergence | Raw calculations in `Figure_4g`--`Figure_4ad` |
| Figure 5(a--f) | GW100 grid convergence, aug-DZVP tier 2 | `Figure_5a`--`Figure_5f`; all 10,800 molecule calculations and 100 TensorGW references are also in `Figure_5a/reproducibility/GW100/` |
| Figure 5(g--j) | Si45H56, 0.5 and 3 Å | `Figure_5g`--`Figure_5j`; 72 currently plotted calculations with `EPS_FILTER=1e-7` and their matching TensorGW reference (−7.194/−1.506 eV) |
| Figure 5(k,l) | Si45H56, 5 Å | `Figure_5k`, `Figure_5l`; 36 calculations with `EPS_FILTER=1e-12` and their matching TensorGW reference (−7.191/−1.502 eV) |
| Figure 5(m--r) | H24P64, 0.5/3/5 Å | `Figure_5m`--`Figure_5r`; 108 calculations with `EPS_FILTER=1e-12` and TensorGW reference (−5.998/−2.353 eV). At 0.5 Å and RS/AO=7, the four plotted outputs use Tikhonov 1e-5 instead of 1e-8. |
| Figure 6(a--c) | GW100 PBE0/def2-TZVP, 0.5/3/5 Å | `Figure_6a`--`Figure_6c`; 3,312 accepted calculations, 92 molecules at each RS/AO 2–13 point, including 19 verified campaign-599 retries. |
| Figure 6(d--f) | GW100 PBE/def2-QZVP, 0.5/3/5 Å | `Figure_6d`--`Figure_6f`; all 3,600 accepted calculations, 100 molecules at each RS/AO 2–13 point, including the 387 final one-node Otus results. |

The filter and basis settings are not identical across every series. Each `input.inp` is authoritative for its point. In particular, Figure 5(g--j) and Figure 5(k,l) must not be described as one uniform `EPS_FILTER=1e-12` series. Figure 4(g,h) retains `EPS_FILTER=1e-7`; Figure 4(i--l) uses `1e-10`; Figure 4(a--f) and 4(s--x) use `1e-12`. H60P400 uses a provisional internal RI-RS reference. See the panel README files for the reference of each series and the remaining panels' settings.

## Reproduce the plotted values

Run from the repository root:

```console
python3 Figure_1a/reproducibility/verify.py
python3 Figure_3a/reproducibility/verify.py
python3 Figure_1a/reproducibility/plot_figure_1.py --output-dir /tmp/figure1
python3 Figure_3a/reproducibility/plot_figure_3.py --output-dir /tmp/figure3
python3 Figure_4a/reproducibility/current_gw100/reproduce.py
python3 Figure_4g/reproducibility/plot_figure_4.py --output-dir /tmp/figure4
python3 Figure_5a/reproducibility/GW100/Analysis/reproduce.py
python3 Figure_5m/reproducibility/cluster_analysis/reproduce.py
python3 Figure_6a/reproducibility/reproduce.py
python3 Figure_1a/reproducibility/scf_wfn_restarts/verify.py
```

The three plot scripts calculate CSVs before plotting and require Matplotlib for PNG output. The Figure 1/2 and Figure 3 verification scripts recompute the current manuscript coordinates directly from raw outputs without Matplotlib. The Figure 4(a--f), Figure 5 and Figure 6 audit scripts use only the Python standard library. The `Figure_4a/reproducibility/current_gw100/molecule_errors.csv` file records all 10,800 inputs, outputs, hashes, molecule energies, reference energies and errors. Its `aggregate.csv` and `plot_coordinates.csv` record all 216 current Figure 4(a--f) points; `missing.csv` is empty. The Figure 4(g--ad) raw calculations remain in their panel directories and can be parsed by `Figure_4g/reproducibility/plot_figure_4.py`. `Figure_5m/reproducibility/cluster_analysis/points.csv` gives the two plotted values, raw hashes, filters, Tikhonov value and matching TensorGW reference for each of 216 cluster calculations. `Figure_5a/reproducibility/GW100/Analysis/reproduce.py` independently verifies its 10,800 molecule outputs, 100 references and 216 mean-error coordinates.

The verification scripts match the current manuscript at all 32 Figure 1 gap, 64 Figure 2 frontier and 50 Figure 3 coordinates. Figure 4, Figure 5 and Figure 6 coordinates match their audited raw calculations; Figure 6 includes 6,912 complete calculations and 288 verified MAE/median coordinates. TensorGW and cluster references used by the current panels are in `Figure_4a/reproducibility/tensor_references/` and `cluster_references/`.

The current small-molecule SCF restart files referenced by Figures 1–5 are collected once in `Figure_1a/reproducibility/scf_wfn_restarts/` (320 unique files). All 192 Figure 6 restarts, geometries, and exact basis/potential files are in `Figure_6a/reproducibility/assets/`. Only systems with at most 20 atoms were eligible for WFN storage; the included GW100 systems have at most 18.
