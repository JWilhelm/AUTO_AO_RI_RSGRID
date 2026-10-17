# Figure 7: RI superpositions on neighboring atoms

Calculation data for Appendix Figure 7. Panels (a,b) show GW100 mean absolute G₀W₀ HOMO/LUMO errors; panels (c,d) show the corresponding absolute errors for Si₄₅H₅₆, relative to TensorGW.

The AO basis is aug-SZV-MOLOPT-GTH-tier-2. Optimized RI bases use neighbor radii of 0.5, 3 and 5 Å and requested RI/AO ratios of 1, 1.5, 2, 3, 4 and 5. At 0.5 Å, no neighboring atom pairs are included and the RI functions are atom-local. The 3 and 5 Å series also include RI superpositions on neighboring atoms. Tabulated RI bases provide the comparison. All RI-RS calculations use RS/AO = 7 and a grid-optimization cluster radius of 3 Å. Si₄₅H₅₆ calculations and their TensorGW reference use `EPS_FILTER = 1e-10`.

| Data | Contents |
|---|---|
| [GW100](GW100/) | 1,800 optimized-RI and 657 tabulated-RI calculations; each output supplies both panels (a,b) |
| [Si45H56](Si45H56/) | 18 optimized-RI and 6 tabulated-RI calculations; each output supplies both panels (c,d) |
| [References](references/) | The 100 GW100 and one Si₄₅H₅₆ TensorGW reference calculations |
| [Energies](energies.csv) | Individual HOMO/LUMO energies, reference energies, basis sizes and absolute errors |
| [Figure values](figure_values.csv) | All 98 plotted coordinates, molecule counts and underlying errors |
| [Assets](assets/) | Basis sets, pseudopotentials, Si₄₅H₅₆ geometry and required SCF restart files |

For tabulated GW100 bases, the seven thresholds use 100, 100, 100, 100, 91, 89 and 77 molecules, respectively; `EXCLUDED.txt` identifies molecules without an available basis. Their horizontal coordinates are the mean actual RI/AO ratios. Optimized-RI horizontal coordinates are the requested ratios. Energies are in eV and errors in meV. The plot places errors below 1 meV at 1 meV; `figure_values.csv` includes both the actual error and the plotted value.

Each calculation contains `input.inp` and the original `output.log`. Run CP2K from the calculation's directory so that the relative paths to the supplied assets resolve correctly. SCF restart files are supplied where the input requests them.
