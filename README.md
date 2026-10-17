# Calculation data for Figures 1–6

CP2K inputs, outputs and orbital energies for the AO-basis, RI-basis and RI-RS-grid optimization study. Each `Figure_<number><letter>` directory corresponds to one figure panel.

| Figure | Data |
| --- | --- |
| [1(a–d)](Figure_1a/) | AO-basis optimization: PBE and G₀W₀ gaps for GW100 and Si45H56 |
| [2(a–d)](Figure_2a/) | PBE and G₀W₀ HOMO/LUMO values from the Figure 1 calculations |
| [3(a–d)](Figure_3a/) | RI-basis convergence for GW100 and Si45H56 |
| [4(a–ad)](Figure_4a/) | RI-RS-grid convergence with aug-SZV tier 2: GW100, Si45H56, Si293H172, H24P64 and H60P400 |
| [5(a–r)](Figure_5a/) | RI-RS-grid convergence with aug-DZVP tier 2: GW100, Si45H56 and H24P64 |
| [6(a–f)](Figure_6a/) | GW100 RI-RS-grid convergence with PBE0/def2-TZVP and PBE/def2-QZVP |

Within each calculation directory, `input.inp` contains the CP2K settings, `output.log` contains the program output, and `bandstructure_SCF_and_G0W0` contains the orbital energies where available. Paired HOMO/LUMO panels share the same calculations. Each panel README identifies its system, parameters and reference data; energies are in eV unless specified otherwise.

Shared basis files, geometries, reference calculations and available SCF wavefunctions are in the panels' `reproducibility/` directories. For reruns, adjust the file paths in the input to your installation.
