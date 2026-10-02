# H60P400 Figure 4 reference and controls

The working reference is `base_e10`: R_RS=3 Å, RI/AO=4, RS/AO=7, EPS_FILTER=1e-10, 30 time/frequency points. Its G0W0 HOMO/LUMO are -4.683/-2.182 eV. `freq40_e12_invalid` is retained only as provenance: 40 is not a supported minimax grid size. RS/AO=8 changes the HOMO/LUMO by -6/+2 meV at EPS_FILTER=1e-12, so RS/AO=7 is provisional, not a fully converged limit.

The 108 Figure 4(y)-(ad) output logs ended normally with WFN restarts. At the pinned snapshot, 92 jobs had Slurm COMPLETED/0:0; for 16 jobs Slurm accounting still reported RUNNING/0:0 after they left squeue and CP2K ended normally. The `job_metadata.json` files preserve this distinction. Three 0.5-Å, RS/AO=3 runs reorder empty G0W0 levels; their bandstructure files are preserved with both panel copies. Full original directories and WFN restarts remain on Noctua 2; large WFN files are intentionally not copied into Git.
