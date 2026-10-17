# Current Figure 5(g--r): Si45H56 and H24P64

`points.csv` maps each of 216 cluster calculations to both HOMO and LUMO panels. It records the actual frontier energies, matching TensorGW values, two plotted errors, RI/RS ratios, filter and Tikhonov settings, repository path, and SHA-256 hashes of each input, output and orbital table. Each panel's `calculations/` and `TensorGW_reference/` folders contain the raw files. The paired panels share the same calculations.

Si45H56 at 0.5 and 3 Å uses `EPS_FILTER=1e-7` and its matching TensorGW reference (−7.194/−1.506 eV); the complete 5-Å series uses `1e-12` and its matching reference (−7.191/−1.502 eV). H24P64 uses `1e-12` and reference −5.998/−2.353 eV. The four 0.5-Å H24P64 points at RS/AO=7 use Tikhonov `1e-5`, as recorded in their inputs, rather than `1e-8`.

Run `python3 Figure_5m/reproducibility/cluster_analysis/reproduce.py` from the repository root. It checks every hash, input setting, CP2K normal end marker, orbital edge, reference and plotted value (with a 1-meV floor for logarithmic display).
