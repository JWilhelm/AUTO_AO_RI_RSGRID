# Figure 5(a–f): complete GW100

This snapshot contains the exact 10,800 RI-RS calculations and 100 selected TensorGW references used in the GWP41 manuscript on 2026-10-03. Adenine is included. Each of the 108 parameter combinations contains all 100 molecules; HOMO and LUMO share the same calculation.

| Panels | Cluster radius | Directory |
|---|---|---|
| a,b | 0.5 Å | RI_RS/panels_a_b |
| c,d | 3 Å | RI_RS/panels_c_d |
| e,f | 5 Å | RI_RS/panels_e_f |

All panels use aug-DZVP-MOLOPT-GTH-tier-2, RI/AO ratios 2–5 and RS/AO ratios 2–10. RI-RS EPS_FILTER is 1e-12. The selected TensorGW calculations use EPS_FILTER 1e-15, metric regularization 1e-6, 30 time/frequency points and 32 MPI ranks × 4 OpenMP threads. This is a fixed-30-point method comparison, not a claim of absolute GW frequency convergence.

## Reference selection

The 18 explicitly listed diagnostic molecules in Analysis/reference_selection.json use the smallest matching tabulated RI basis per element with reported relative RI-MP2 error strictly below 1e-4, as requested by Jan. The remaining molecules, including adenine, use the largest matching tabulated RI basis. Selection follows the recorded numerical stability checks, not minimum disagreement with RI-RS. The mixed basis policy is explicit and can contribute to residual differences.

The TensorGW library applies REGULARIZATION_RI to the M_PQ inversion; the original code applied it only in the RI-RS branch. Code/ contains the exact diagnostic source, narrow patch and build commands. The original installation was unchanged. Provenance/software.json records the selected library checksum. This isolated research correction is not a claim of upstream CP2K validation.

Tabulated bases are from JWilhelm/BASIS_AUG_MOLOPT at commit a93ac12fcba4985dfa3f5bddd3db40a7471b88a1; the precise Git blob audit and basis files are included. No AUTO_BASIS or combined union basis is used.

## Raw data and provenance

Each run includes its exact input, output and orbital table. Shared farm submission scripts and logs are stored once under Slurm/. Provenance/calculations.json maps every run to its source and Slurm ID. All selected jobs were checked as COMPLETED with exit code 0:0, normal CP2K end, restart density, converged SCF and finite GW values. Warnings are retained. SCF does not always converge in one step; the observed iteration counts are recorded rather than suppressed.

Large binary WFN restart files and executable libraries remain on Noctua; their paths and checksums are recorded, not bundled. Inputs retain original Noctua paths as raw provenance; adapt those paths and supply the recorded WFN files to rerun. SHA256SUMS.json covers the transferred raw package; supplementary analysis/readme files are versioned by Git.

## Reproduce the published averages

Run `python3 Analysis/reproduce.py` from this directory. It verifies all raw-file checksums, reads all 10,900 outputs, checks matched DFT energies and reproduces all 216 HOMO/LUMO aggregate rows against Analysis/aggregate.csv. Energies are evaluated at the precision printed by CP2K. Historical alternative and unstable references are not silently mixed into this snapshot.
