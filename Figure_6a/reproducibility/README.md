# Current manuscript Figure 6: complete raw calculations

This archive contains all **6,912 accepted molecule/grid calculations** plotted in Figure 6(a–f): 92 GW100 molecules × 12 grid sizes in each PBE0/def2-TZVP panel (a–c), and 100 GW100 molecules × 12 grid sizes in each PBE/def2-QZVP panel (d–f). Radii are 0.5, 3, and 5 Å in panel order. The output of each accepted calculation sits in its `Figure_6a` … `Figure_6f` panel directory. `raw_file_manifest.json` identifies the production campaign, original run directory, and SHA-256 hash of every input, CP2K output and GW orbital table. Failed and superseded attempts are not substituted for accepted outputs.

Panels a–c use GWP36 PBE0/def2-TZVP orbital-matched references for 92 molecules; the He calculation is outside this series. Their RS/AO 2–10 runs are from Noctua campaign 597, panel a's RS/AO 11–13 runs from campaign 599, and panels b/c's RS/AO 11–13 runs from campaign 594. Campaign 599 includes 19 individually verified retry results. Campaign 594 uses Tikhonov 1e-8 for the plotted 11–13 points; the other plotted a–c inputs use 1e-5. Panels d–f use the 100 FHI-aims Table I (2021 SI) orbital-matched PBE/def2-QZVP references. Their accepted RS/AO 2–10 runs are from production campaign 597 and 11–13 from 600, on Noctua 2 and the final Otus FFTW3 build. HOMO MAE/median exclude BN, BeO, MgO, O3 and CuCN (95 molecules per point); LUMO includes all 100. The Xe/BeO numerical-diagnostic campaign 601 and old failed/cancelled Otus attempts are not included.

Every archived input reads an SCF wavefunction restart. `assets/` contains the **192 unique original SCF-WFN files** referenced by the accepted 6,912 inputs (92 PBE0 and 100 PBE), 100 QZVP XYZ geometries and the five exact basis/potential source files. All these molecules have at most 18 atoms. `asset_manifest.json` records their sizes and SHA-256 hashes. The raw `input.inp` files deliberately preserve original cluster paths. For a local rerun, generate a relocated copy, for example:

```console
python3 Figure_6a/reproducibility/prepare_local_input.py d 2 01_He /tmp/figure6d_he_rs02.inp
```

The CP2K executable must be compatible with the frozen production source and relevant build settings; the original outputs, source revisions, binary identifiers and scheduler audits are preserved in `audits/`. This repository does not treat a successful input parse as proof of a valid GW point.

Run the independent raw-to-figure audit from the repository root:

```console
python3 Figure_6a/reproducibility/reproduce.py
```

It verifies 6,912 complete raw triples, their 20,736 SHA-256 hashes, all 297 shared assets, normal CP2K end and actual SCF-WFN restart, finite orbital-matched QP values, normalized three-centre fitting error, evaluation counts, and **all 288 plotted MAE/median coordinates** in `figure6_source_snapshot.tex` (SHA-256 `987d3e497470057b8e716fd10de2c9974f2d4fa7cb81f3558d9582be1336d7ca`). `aggregate.csv` and `molecule_errors.csv` are regenerated from raw files. The six panel directories and the source snapshot are the current Figure 6 data only; they do not include earlier preview curves.
