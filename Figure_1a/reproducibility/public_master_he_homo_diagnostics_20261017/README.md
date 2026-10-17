# He HOMO: fit-window and minimax spot checks (17 October 2026)

System: Figure 4a He, AUTO_RI ratio 4, RI-RS ratio 10, 0.5 Å cluster radius. All successful diagnostics used public CP2K `master` commit `08825b921571435c7155122cf567393533eeb2ca` on Noctua 2 with one MPI rank and eight OpenMP threads. They differ from the [adapted Figure 4a input](../../../Figure_4a/current_eps12/ri4_rs10/01_He/input.inp) only in the explicitly tabulated GW parameters. [Raw inputs, CP2K outputs, orbital tables and scheduler stderr](cases/) and [machine-readable values with hashes and job IDs](comparison.csv) are included. Each of the ten jobs completed with exit code 0, a normal CP2K end marker and zero CP2K warnings.

The historical calculation and the adapted public-master baseline both printed `FREQ_MAX_FIT = 10 eV`, `REGULARIZATION_MINIMAX = 1e-6`, `NUM_TIME_FREQ_POINTS = 30`, `EPS_FILTER = 1e-12`, and `AUTO_RI` frontier orbital window `= 5 eV`. Their HOMOs were −22.600 and −22.125 eV, respectively; the TensorGW reference shown for this system is −22.548 eV. The historical/public-master difference therefore did **not** come from silently changing one of these printed parameter values. The two CP2K versions and parallel layouts differ; the [earlier spot-check report](../public_master_spotcheck_20261017/README.md) describes those limits.

| `FREQ_MAX_FIT` (eV) | Minimax points | `REGULARIZATION_MINIMAX` | GW HOMO (eV) | GW LUMO (eV) |
| ---: | ---: | ---: | ---: | ---: |
| 5 | 30 | 1e-6 | −21.874 | 6.495 |
| 10 (baseline) | 30 | 1e-6 | −22.125 | 6.495 |
| 20 | 30 | 1e-6 | −22.322 | 6.494 |
| 40 | 30 | 1e-6 | −22.423 | 6.494 |
| 80 | 30 | 1e-6 | −22.469 | 6.494 |
| 160 | 30 | 1e-6 | −22.281 | 6.492 |
| 10 | 34 | 1e-6 | −21.643 | 6.484 |
| 80 | 34 | 1e-6 | −22.135 | 6.491 |
| 10 | 30 | 1e-4 | −21.166 | 6.487 |
| 10 | 30 | 1e-8 | −21.715 | 6.489 |

At otherwise baseline settings, tightening `EPS_FILTER` from 1e-12 to 1e-14 returned the same HOMO/LUMO to 0.001 eV. The SCF HOMO (−15.765 eV), occupied-orbital exchange self-energy (−27.522 eV), RI-RS initial normalized error (7.615188545462e-9), and final normalized three-centre error (1.5e-9) were identical at the shown precision across all successful diagnostics. The large HOMO changes follow the occupied-orbital correlation self-energy: e.g. 3.004 eV at baseline, 2.659 eV with an 80 eV fit window, and 3.486 eV with 34 points at a 10 eV fit window.

The 80 eV/30-point result is numerically closer to TensorGW (79 meV difference), but the shift reverses at 160 eV, and changing 30 to 34 points moves the 80 eV result by 334 meV. Neither fit-window nor point-count series is converged. Altering minimax regularization in either tested direction also worsens the HOMO versus TensorGW. Thus a single parameter choice that happens to move the HOMO toward the reference is not a justified correction to the Figure 4a input or evidence that the old/new CP2K difference is fully explained by analytic continuation. The tiny three-centre fitting error does not guarantee a converged GW HOMO.

Two additional 50-point attempts (Slurm 34666493 and 34666494) failed with CP2K's explicit `The grid size you choose is not available` abort. Their raw files are retained in the authorized Noctua project directory. The public source's `get_rpa_minimax_coeff_larger_grid` accepts 30, 32 and 34 near this range, but not 50; 34 was used for the successful point-count comparison.
