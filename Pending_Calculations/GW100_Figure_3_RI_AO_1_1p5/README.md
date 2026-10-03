# Completed GW100 Figure 3 RI/AO=1 and 1.5 extension

Submission archive, October 2, 2026: 200 independent one-node CoopFST jobs,
IDs 34586224--34586423, with no arrays or dependencies. This directory contains
inputs, job scripts, original completed outputs, orbital-resolved band tables,
and Slurm stdout/stderr. All 200 jobs completed with exit code zero and normal
CP2K termination, verified on October 3, 2026.

Each ratio covers all 100 GW100 molecules using the original Figure-4(c,d)
CP2K build and settings: aug-SZV-MOLOPT-GTH-tier-2, RS/AO=7, RI neighbors 3 Å,
grid clusters 3 Å, EPS_FILTER=1e-7, Tikhonov=1e-4, 30 time/frequency points,
Hedin shift off, D_PRIME/FULL_ATOM Cholesky selection on GAPW_LOG radial/Lebedev
candidates, initial RS/AO=30, L_ADDITIONAL=2, 300 optimizer iterations.
GW restart output is disabled; previously converged source SCF wavefunctions
are reused. Absolute runtime and dependency paths refer to Jan's Noctua archive.
They must be adapted on another installation; WFN/basis/executable files are
not included here.

`manifest.json` records full scientific inputs, source paths, hashes,
wavefunction provenance, timing-based limits and MPI/OpenMP layouts.
`submissions.json` maps every run to its individual Slurm job.
The preparation/submission scripts are retained for provenance, not automatic
execution by the figure workflow. No missing result is filled from older runs.

`validation.json` records SCF, settings, orbital-edge and warning checks,
including P95, maximum errors and raw outlier inspection. `statistics.csv`
contains both complete 100-molecule series. `completion_status.json` preserves
the Slurm/application evidence. The original directory name is retained for
backward links; this campaign is complete.

RI/AO 1: HOMO/LUMO MAE 400.42/122.53 meV.
RI/AO 1.5: HOMO/LUMO MAE 95.90/40.61 meV.
The same outputs are included in the active Figure_3a/b directories.
