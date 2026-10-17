# Public CP2K master: three small input spot checks (17 October 2026)

The six raw files under `cases/` are new CP2K outputs and orbital tables, generated on Noctua 2 with public CP2K `master` commit `08825b921571435c7155122cf567393533eeb2ca`. The input of each run is byte-identical to the adapted `input.inp` linked below; input hashes, output hashes, Slurm job IDs, parallel layouts and parsed values are in [`comparison.csv`](comparison.csv). All three jobs ended with Slurm `COMPLETED/0:0`, a normal CP2K end marker, and zero CP2K warnings. The original output files remain in their figure directories.

| Case and input | Historical → public-master initial normalized grid error | Historical → public-master final normalized 3C error | Historical → public-master GW HOMO / LUMO (eV) |
| --- | ---: | ---: | ---: |
| [Figure 4a, CH4, RI3/RS6](../../../Figure_4a/current_eps12/ri3_rs06/20_CH4/input.inp) | 5.907734e-3 → 5.507874e-3 | 1.4e-5 → 2.1e-7 | −13.132 / 1.640 → −13.209 / 1.664 |
| [Figure 4a, He, RI4/RS10](../../../Figure_4a/current_eps12/ri4_rs10/01_He/input.inp) | 1.923540e-9 → 7.615189e-9 | 1.9e-9 → 1.5e-9 | −22.600 / 6.492 → −22.125 / 6.495 |
| [Figure 4c, CH4, RI3/RS6](../../../Figure_4c/current_eps12/ri3_rs06/20_CH4/input.inp) | 2.051129e-5 → 1.994053e-4 | 4.3e-8 → 2.0e-8 | −13.224 / 1.689 → −13.224 / 1.689 |

Thus the adapted inputs run with public `master`, but numerical equality cannot be assumed. The historical inputs requested pivot selection using the scaled, regularized $D'_{ll'}$; public `master` uses $D_{ll'}$. The He input additionally requested 250 initial candidates per AO function, while the public code uses `max(30, 2 RS_AO_RATIO)` (30 for RS/AO 10). The two CH4 inputs requested 30. The three historical outputs used 37 MPI ranks with 32, 16 and 32 OpenMP threads, respectively; the new runs used one MPI rank and eight OpenMP threads. The comparison establishes the result of running the adapted inputs in this public-master configuration; it does not isolate which code or parallel-layout change caused each numerical difference. Only three of the 68,500 figure `input.inp` files were run again.

New CP2K output and orbital table pairs are in `cases/a_ri3_rs06_CH4/`, `cases/a_ri4_rs10_He/`, and `cases/c_ri3_rs06_CH4/`. The complete historical raw files are next to the linked figure inputs. The original input bytes are available at repository commit `768b14d59d5870e92a01ca9bcd544a9e3a9af84f`.
