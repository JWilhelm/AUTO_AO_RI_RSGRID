# Public CP2K master: five small input checks (17 October 2026)

The ten raw files under `cases/` are new CP2K outputs and orbital tables, generated on Noctua 2 with public CP2K `master` commit `08825b921571435c7155122cf567393533eeb2ca`. The input of each run is byte-identical to the adapted `input.inp` linked below; input hashes, output hashes, Slurm job IDs, parallel layouts and parsed values are in [`comparison.csv`](comparison.csv). All five jobs ended with Slurm `COMPLETED/0:0`, a normal CP2K end marker, and zero CP2K warnings. The original output files remain in their figure directories.

| Case and input | Historical → public-master initial normalized grid error | Historical → public-master final normalized 3C error | Historical → public-master GW HOMO / LUMO (eV) |
| --- | ---: | ---: | ---: |
| [Figure 4a, CH4, RI3/RS6](../../../Figure_4a/current_eps12/ri3_rs06/20_CH4/input.inp) | 5.907734e-3 → 5.507874e-3 | 1.4e-5 → 2.1e-7 | −13.132 / 1.640 → −13.209 / 1.664 |
| [Figure 4a, He, RI4/RS8](../../../Figure_4a/current_eps12/ri4_rs08/01_He/input.inp) | 2.302045e-9 → 6.017687e-8 | 1.1e-9 → 1.6e-9 | −22.599 / 6.492 → −22.125 / 6.495 |
| [Figure 4a, He, RI4/RS9](../../../Figure_4a/current_eps12/ri4_rs09/01_He/input.inp) | 1.053101e-9 → 2.574504e-8 | 1.1e-9 → 1.6e-9 | −22.600 / 6.492 → −22.125 / 6.495 |
| [Figure 4a, He, RI4/RS10](../../../Figure_4a/current_eps12/ri4_rs10/01_He/input.inp) | 1.923540e-9 → 7.615189e-9 | 1.9e-9 → 1.5e-9 | −22.600 / 6.492 → −22.125 / 6.495 |
| [Figure 4c, CH4, RI3/RS6](../../../Figure_4c/current_eps12/ri3_rs06/20_CH4/input.inp) | 2.051129e-5 → 1.994053e-4 | 4.3e-8 → 2.0e-8 | −13.224 / 1.689 → −13.224 / 1.689 |

Thus the adapted inputs run with public `master`, but numerical equality cannot be assumed. The historical inputs requested pivot selection using the scaled, regularized $D'_{ll'}$; public `master` uses $D_{ll'}$. The historical He RS/AO 10 input additionally requested 250 initial candidates per AO function, while the public code uses `max(30, 2 RS_AO_RATIO)` (30 here). Historical He RS/AO 8 and 9 requested 30 and already gave the same HOMO as RS/AO 10 within 0.001 eV. Public `master` also gives the same He HOMO at RS/AO 8, 9 and 10, but shifted by 0.474–0.475 eV from the historical plateau. Therefore the removed 250-candidate setting at RS/AO 10 is not a sufficient explanation. The He SCF energy is identical, and its occupied-orbital exchange self-energy is unchanged to 0.001 eV; the correlation self-energy differs by about 0.475 eV. The final normalized 3C fitting error is about 1.5–1.6e-9 in the public runs despite this GW difference.

Figure 4a denotes the 0.5 Å atomic-cluster radius. For monatomic He this radius does not change cluster membership. The historical outputs used 37 MPI ranks and 16–32 OpenMP threads; the new runs used one MPI rank and eight OpenMP threads. The comparison establishes the result of running the adapted inputs in this public-master configuration; it does not isolate which code or parallel-layout change caused each numerical difference. Only five of the 68,500 figure `input.inp` files were run again.

New CP2K output and orbital table pairs are under `cases/`. The complete historical raw files are next to the linked figure inputs. The original input bytes are available at repository commit `768b14d59d5870e92a01ca9bcd544a9e3a9af84f`.

A [separate He HOMO diagnostic](../public_master_he_homo_diagnostics_20261017/README.md) tests the GW analytic-continuation fit window, minimax regularization, and supported minimax point counts against this public-master baseline.
