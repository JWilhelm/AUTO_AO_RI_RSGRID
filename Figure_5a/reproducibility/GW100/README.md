# GW100 data for Figure 5(a–f)

`RI_RS/` contains the 10,800 molecule/grid calculations; `TensorGW/` contains the 100 reference calculations. `Analysis/aggregate.csv` gives the mean absolute errors in meV. Shared basis and potential files are in `Assets/`.

| Panels | Cluster radius | Calculations |
| --- | --- | --- |
| a,b | 0.5 Å | `RI_RS/panels_a_b/` |
| c,d | 3 Å | `RI_RS/panels_c_d/` |
| e,f | 5 Å | `RI_RS/panels_e_f/` |

The calculations use aug-DZVP-MOLOPT-GTH-tier-2, RI/AO 2–5 and RS/AO 2–10. RI-RS uses `EPS_FILTER=1e-12`. TensorGW uses `EPS_FILTER=1e-15`, RI-metric regularization `1e-6` and 30 time/frequency points. The exact tabulated RI basis is specified in each reference input.
