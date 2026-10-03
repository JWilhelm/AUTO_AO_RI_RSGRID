# Figure 5 H24P64 RS/AO=7 Tikhonov correction

These are the four validated CP2K RI-RS calculations used for the H24P64/aug-DZVP-MOLOPT-GTH-tier-2 points at RS/AO=7 and R_RS=0.5 Å in Figure 5(m,n). They replace the outlying TIKHONOV=1e-8 points. Each calculation uses `RI_RS%TIKHONOV=1e-5`, `GW%EPS_FILTER=1e-12`, one Noctua node and account `hpc-prf-coopfst`. `GW%PRINT%RESTART` is OFF.

| RI/AO | Slurm job | G0W0 HOMO (eV) | G0W0 LUMO (eV) | Normalized 3C error | Maximum absolute 3C error |
|---:|---:|---:|---:|---:|---:|
| 2 | 34586737 | -6.003 | -2.349 | 5.8E-08 | 1.4E-03 |
| 3 | 34586738 | -6.007 | -2.346 | 5.8E-08 | 1.4E-03 |
| 4 | 34586739 | -6.008 | -2.345 | 5.8E-08 | 1.4E-03 |
| 5 | 34586740 | -6.008 | -2.345 | 5.8E-08 | 1.4E-03 |

All four Slurm jobs finished `COMPLETED/0:0`; CP2K ended normally after converged restart SCF. The stderr files contain only CPU binding and module-purge notices. The previous TIKHONOV=1e-8 values from campaign 416 and the matching TensorGW reference are recorded in `validation.json`. The new regularization removes the RS/AO=7 3C-fitting-error spike (approximately 1.5e-3 to 5.8e-8 normalized); the filter-only controls at 1e-13 and 1e-14 in campaign 418 left the previous band edges unchanged at 1 meV output precision. The TensorGW reference (-5.998/-2.353 eV) is from campaign 416, job 34586510.

Each `ri*_rs07/` folder has the exact CP2K input, output, orbital band table, Slurm submission script, stdout and stderr. `source_manifest.json` maps the original campaign-416 inputs to the corrected inputs; `submissions.tsv` maps each new run to its job ID. `checksums.sha256` covers every archived source file and `validation.json`. The WFN restart was read from campaign 149 and is retained on Noctua; its path, size and SHA256 are in `validation.json`, while the binary WFN is omitted from Git.

Source campaign: `/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/421_h24p64_rc0p5_rs07_tikh1e5_20261003`.
