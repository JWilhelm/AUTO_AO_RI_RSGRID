# Selected GW100 references for Figure 4(a–f)

The four TensorGW references use aug-SZV-MOLOPT-GTH-tier-2, the largest matching tabulated RI basis, 30 time/frequency points, `EPS_FILTER=1e-15` and `REGULARIZATION_RI=1e-6`. The linked diagnostic library applies RI regularization to the Tensor metric inversion. Its source and build commands are in `code/`; run scripts and linked-library records are included. Basis and potential files are in `assets/`.

`selection.json` gives job IDs, scheduler records, paths and checksums for four TensorGW references here and four RI-RS calculations in `Figure_4e/` and `Figure_4f/`. The RI-RS calculations are LiF and BeO at 5 Å, RI/AO=5 and RS/AO=7,10, with `EPS_FILTER=1e-12`. They read SCF restarts and disable GW restart-matrix printing. The other 96 TensorGW references are in `Figure_4a/reproducibility/tensor_references/GW100_TensorGW/`.

All 100 molecules contribute to each of the 108 GW100 parameter points. This is a fixed-30-point comparison; absolute frequency convergence is not claimed. Verify the plotted means with `python3 Figure_4a/reproducibility/current_gw100/reproduce.py` from the repository root.
