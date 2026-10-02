# Submitted GW100 Figure 3 RI/AO=1 and 1.5 extension

Submission archive, October 2, 2026: 200 independent one-node CoopFST jobs,
IDs 34586224--34586423, with no arrays or dependencies. This directory contains
inputs and job scripts, not validated completed outputs.

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

Completed outputs will be added after Slurm/application validation and checks
of the SCF state, printed settings, errors and warnings. Figure-3 statistics
require all 100 valid reference pairs for each new ratio.
