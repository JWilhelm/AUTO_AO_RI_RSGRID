# Selected GW100 references for Figure 4(a–f)

Only calculations actually used in the updated Figure 4 are added here. The four
TensorGW calculations use aug-SZV-MOLOPT-GTH-tier-2, the largest matching tabulated
RI basis, 30 time/frequency points, EPS_FILTER=1e-15 and REGULARIZATION_RI=1e-6.
The linked diagnostic library applies RI regularization to the Tensor metric
inversion. Its exact modified source and build commands are in `code/`; original
run scripts and linked-library records are preserved. Basis and potential files
are in `assets/`. Absolute Noctua paths in raw inputs are kept as provenance.

`selection.json` identifies exactly eight new calculations with job IDs, successful
scheduler records, original paths and file checksums: four Tensor references here,
and four RI-RS replacements in `Figure_4e/`, mirrored in `Figure_4f/` for the LUMO
panels. Those are LiF and BeO at 5 Angstrom, RI/AO=5 and RS/AO=7,10. Their only
scientific input change from the original Figure-4 archive is EPS_FILTER=1e-12.
SCF restarts are reused and GW restart-matrix printing is disabled.

All 100 molecules remain in every one of the 108 GW100 parameter points. The other
96 Tensor references remain in `TensorGW_Calculations/GW100_TensorGW/`. Figure 3
retains its own existing reference selection. This is an explicitly selected
correction of four references and four RI-RS calculations, not a uniform rerun of
the whole benchmark. The remaining RI-RS calculations retain EPS_FILTER=1e-7.

This is a fixed-30-point comparison: absolute frequency convergence is not claimed.
No unselected basis/filter/regularization/frequency controls or failed attempts
from the diagnostic sweep are included. Reproduce all means, P95 and extrema with
`python3 Plot_Figure_4/plot_figure_4.py` from the repository root.
