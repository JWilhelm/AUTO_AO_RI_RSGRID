#!/usr/bin/env python3
"""Recompute current Figure 3 from raw CP2K outputs.

GW100 uses precisely the RS/AO=7 slice of Figure 4(c,d), with RI neighbors
within 3 Angstrom. Silicon uses atom-local optimized RI. Incomplete tabulated
GW100 diagnostics remain visible with explicit coverage.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
import re
import statistics
import math


HOMO_RE = re.compile(r"G0W0 valence band maximum \(eV\):\s+([-+0-9.Ee]+)")
LUMO_RE = re.compile(r"G0W0 conduction band minimum \(eV\):\s+([-+0-9.Ee]+)")
ENERGY_RE = re.compile(
    r"ENERGY\|\s+Total FORCE_EVAL \( QS \) energy \[(?:a\.u\.|hartree)\]\s+([-+0-9.Ee]+)"
)
AO_RE = re.compile(r"^\s*Number of Gaussian basis functions for MOs\s+(\d+)\s*$", re.MULTILINE)
RI_RE = re.compile(
    r"^\s*(?:Number of auxiliary Gaussian basis functions for .+?|"
    r"AUTO_RI\| Number of automatic RI functions for .+?:)\s+(\d+)\s*$",
    re.MULTILINE,
)
NORMAL_RE = re.compile(r"PROGRAM ENDED AT")
FATAL_RE = re.compile(
    r"\[(?:ABORT|ASSERT)\]|CPASSERT|MPI_ABORT|SIGSEGV|segmentation fault|"
    r"out of memory|oom.kill|Killed process|Cannot allocate memory",
    re.IGNORECASE,
)
AUTO_RE = re.compile(r"AUTO-RI_radius-(0p5|3|5)_RI-AO-ratio-(1|1p5|2|3|4|5)$")
TAB_RE = re.compile(r"Tabulated_t1e-(\d+)$")

SYSTEMS = (
    ("GW100", "Figure_3a"),
    ("Si45H56", "Figure_3c"),
    ("Si293H172", "Figure_3e"),
)
RADII = {"0p5": 0.5, "3": 3.0, "5": 5.0}
def final_match(pattern: re.Pattern[str], text: str, label: str, path: Path) -> float:
    values = pattern.findall(text)
    if not values:
        raise RuntimeError(f"Missing {label} in {path}")
    return float(values[-1])


def parse_output(path: Path) -> dict[str, float | int]:
    text = path.read_text(errors="replace")
    if not NORMAL_RE.search(text) or FATAL_RE.search(text):
        raise RuntimeError(f"Invalid or incomplete CP2K output: {path}")
    return {
        "homo_eV": final_match(HOMO_RE, text, "G0W0 HOMO", path),
        "lumo_eV": final_match(LUMO_RE, text, "G0W0 LUMO", path),
        "total_energy_hartree": final_match(ENERGY_RE, text, "total energy", path),
        "n_ao": int(final_match(AO_RE, text, "AO count", path)),
        "n_ri": int(final_match(RI_RE, text, "RI count", path)),
    }


def load_references(repo: Path) -> dict:
    tensor_root = repo / "TensorGW_Calculations"
    gw_root = tensor_root / "GW100_TensorGW"
    case_dirs = sorted(path for path in gw_root.iterdir() if path.is_dir())
    if len(case_dirs) != 100:
        raise RuntimeError(f"Expected 100 GW100 TensorGW calculations; found {len(case_dirs)}")
    return {
        "gw100": {case_dir.name: parse_output(case_dir / "output.log") for case_dir in case_dirs},
        "si45h56": parse_output(tensor_root / "Si45H56_TensorGW" / "output.log"),
        "si293h172": parse_output(
            repo
            / "Fixed_References"
            / "Si293H172_RI-RS_reference"
            / "output.log"
        ),
    }


def point_metadata(name: str) -> dict[str, str | float]:
    match = AUTO_RE.fullmatch(name)
    if match:
        radius = RADII[match.group(1)]
        return {
            "method": "AUTO_RI",
            "series": f"auto_r{radius:g}",
            "neighbor_radius_angstrom": radius,
            "requested_ri_ao_ratio": float(match.group(2).replace("p", ".")),
            "tabulated_threshold": "",
        }
    match = TAB_RE.fullmatch(name)
    if match:
        return {
            "method": "tabulated_RI",
            "series": "tabulated",
            "neighbor_radius_angstrom": "",
            "requested_ri_ao_ratio": "",
            "tabulated_threshold": f"1e-{match.group(1)}",
        }
    raise RuntimeError(f"Unexpected Figure 3 point directory: {name}")


def reference_for(references: dict, system: str, case: str) -> dict:
    if system == "GW100":
        return references["gw100"][case]
    if system == "Si45H56":
        return references["si45h56"]
    return references["si293h172"]


def collect(repo: Path, references: dict) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    valid_count = 0
    excluded_count = 0
    reference_energy_deltas: list[dict] = []
    energy_by_system: dict[str, list[float]] = defaultdict(list)

    for system, panel in SYSTEMS:
        panel_root = repo / panel
        if not panel_root.is_dir():
            raise RuntimeError(f"Missing panel directory: {panel_root}")
        for point_dir in sorted(path for path in panel_root.iterdir() if path.is_dir()):
            metadata = point_metadata(point_dir.name)
            if system != "GW100" and metadata["series"] not in ("auto_r0.5", "tabulated"):
                continue
            if system == "GW100" and metadata["method"] == "AUTO_RI" and metadata["series"] != "auto_r3":
                raise RuntimeError(f"Unexpected RI neighborhood in current GW100 Figure 3: {point_dir}")
            calculations: list[tuple[str, dict]] = []
            if system == "GW100":
                case_dirs = sorted(path for path in point_dir.iterdir() if path.is_dir())
                if len(case_dirs) != 100:
                    raise RuntimeError(f"Expected 100 GW100 entries in {point_dir}; found {len(case_dirs)}")
                for case_dir in case_dirs:
                    output = case_dir / "output.log"
                    excluded = case_dir / "EXCLUDED.txt"
                    if output.is_file():
                        calculations.append((case_dir.name, parse_output(output)))
                        valid_count += 1
                    elif excluded.is_file():
                        excluded_count += 1
                    else:
                        raise RuntimeError(f"Missing output or EXCLUDED.txt: {case_dir}")
            else:
                calculations.append((system, parse_output(point_dir / "output.log")))
                valid_count += 1

            if system == "GW100" and metadata["method"] == "AUTO_RI" and len(calculations) != 100:
                raise RuntimeError(f"Incomplete optimized GW100 point: {point_dir}")
            if not calculations:
                raise RuntimeError(f"No valid calculations in {point_dir}")
            if metadata["method"] == "AUTO_RI":
                x_value = float(metadata["requested_ri_ao_ratio"])
            else:
                x_value = statistics.fmean(
                    float(value["n_ri"]) / float(value["n_ao"])
                    for _, value in calculations
                )

            signed_errors = {"homo": [], "lumo": []}
            for case, value in calculations:
                reference = reference_for(references, system, case)
                energy = float(value["total_energy_hartree"])
                energy_by_system[system].append(energy)
                if "total_energy_hartree" in reference:
                    reference_energy_deltas.append(
                        {
                            "system": system,
                            "case": case,
                            "point": point_dir.name,
                            "delta_hartree": energy - float(reference["total_energy_hartree"]),
                        }
                    )
                for orbital in ("homo", "lumo"):
                    signed_errors[orbital].append(
                        1000.0 * (float(value[f"{orbital}_eV"]) - float(reference[f"{orbital}_eV"]))
                    )

            for orbital in ("homo", "lumo"):
                absolute = [abs(value) for value in signed_errors[orbital]]
                error = statistics.fmean(absolute) if system == "GW100" else absolute[0]
                plotted_error = (
                    max(1.0, error)
                    if system == "GW100"
                    else max(1.0, float(round(error)))
                )
                rows.append(
                    {
                        "system": system,
                        "orbital": orbital,
                        "series": metadata["series"],
                        "method": metadata["method"],
                        "neighbor_radius_angstrom": metadata["neighbor_radius_angstrom"],
                        "point": point_dir.name,
                        "x_ri_ao_ratio": x_value,
                        "valid_calculations": len(calculations),
                        "error_raw_meV": error,
                        "error_plotted_meV": plotted_error,
                        "expected_calculations": 100 if system == "GW100" else 1,
                        "coverage": f"{len(calculations)}/{100 if system == 'GW100' else 1}",
                        "p95_abs_error_meV": percentile(absolute, 0.95),
                        "max_abs_error_meV": max(absolute),
                        "worst_case": calculations[max(range(len(absolute)), key=absolute.__getitem__)][0],
                        "worst_signed_error_meV": signed_errors[orbital][max(range(len(absolute)), key=absolute.__getitem__)],
                        "raw_directory": str(point_dir.relative_to(repo)),
                    }
                )

    gw_auto_ratios = {float(row["x_ri_ao_ratio"]) for row in rows
                      if row["system"] == "GW100" and row["method"] == "AUTO_RI"}
    if not {2.0, 3.0, 4.0, 5.0}.issubset(gw_auto_ratios):
        raise RuntimeError("The validated Figure-4 RI/AO=2--5 slice is incomplete")
    expected_valid = 657 + 24 + 100 * len(gw_auto_ratios)
    expected_coordinates = 62 + 2 * len(gw_auto_ratios)
    if valid_count != expected_valid or excluded_count != 43 or len(rows) != expected_coordinates:
        raise RuntimeError(
            f"Unexpected coverage: valid={valid_count}, excluded={excluded_count}, coordinates={len(rows)}"
        )
    worst = max(reference_energy_deltas, key=lambda item: abs(item["delta_hartree"]))
    validation = {
        "valid_calculations": valid_count,
        "excluded_calculations": excluded_count,
        "figure_coordinates": len(rows),
        "reference_paired_calculations": len(reference_energy_deltas),
        "maximum_absolute_reference_energy_delta_hartree": abs(worst["delta_hartree"]),
        "worst_reference_energy_delta": worst,
        "all_reference_pairs_within_1e-6_hartree": all(
            abs(item["delta_hartree"]) <= 1.0e-6 for item in reference_energy_deltas
        ),
        "energy_spread_by_system_hartree": {
            system: max(values) - min(values)
            for system, values in energy_by_system.items()
            if system != "GW100"
        },
    }
    if not validation["all_reference_pairs_within_1e-6_hartree"]:
        raise RuntimeError(f"Reference SCF-state mismatch: {worst}")
    return rows, validation


def percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    index = (len(ordered) - 1) * q
    lo, hi = math.floor(index), math.ceil(index)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (index - lo)


def plot(path: Path, rows: list[dict]) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("Plotting requires matplotlib (python -m pip install matplotlib)") from exc

    panels = (
        ("GW100", "homo", r"$\mathit{GW}100$ $G_0W_0$ HOMO", "MAE (meV)", (0.9, 1300.0)),
        ("GW100", "lumo", r"$\mathit{GW}100$ $G_0W_0$ LUMO", "MAE (meV)", (0.9, 1300.0)),
        ("Si45H56", "homo", r"Si$_{45}$H$_{56}$ $G_0W_0$ HOMO", "Abs. error (meV)", (0.8, 300.0)),
        ("Si45H56", "lumo", r"Si$_{45}$H$_{56}$ $G_0W_0$ LUMO", "Abs. error (meV)", (0.8, 300.0)),
        ("Si293H172", "homo", r"Si$_{293}$H$_{172}$ $G_0W_0$ HOMO", "Abs. error (meV)", (0.8, 300.0)),
        ("Si293H172", "lumo", r"Si$_{293}$H$_{172}$ $G_0W_0$ LUMO", "Abs. error (meV)", (0.8, 300.0)),
    )
    lookup: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for row in rows:
        lookup[(row["system"], row["orbital"], row["series"])].append(row)
    for values in lookup.values():
        values.sort(key=lambda row: float(row["x_ri_ao_ratio"]))

    fig, axes = plt.subplots(3, 2, figsize=(9.0, 10.5), sharex=True)
    for letter, axis, (system, orbital, title, ylabel, limits) in zip("abcdef", axes.flat, panels):
        axis.axhspan(limits[0], 10.0, color="#EAF4EC", zorder=0)
        for series in (("auto_r3", "tabulated") if system == "GW100" else ("auto_r0.5", "tabulated")):
            values = lookup[(system, orbital, series)]
            axis.plot(
                [float(row["x_ri_ao_ratio"]) for row in values],
                [float(row["error_plotted_meV"]) for row in values],
                marker="D" if series == "tabulated" else "o",
                color="#222222" if series == "tabulated" else "#0072B2", lw=1.6, ms=4.5,
                label="tabulated RI" if series == "tabulated" else "optimized RI",
            )
        axis.set_yscale("log")
        axis.set_xlim(0.7, 5.35)
        axis.set_ylim(*limits)
        axis.grid(True, which="both", color="#d5d5d5", lw=0.5)
        axis.set_ylabel(ylabel)
        axis.text(
            0.98, 0.96, f"({letter}) {title}", transform=axis.transAxes, ha="right", va="top",
            bbox={"facecolor": "white", "edgecolor": "#bbbbbb", "pad": 2.0},
        )
    for axis in axes[-1, :]:
        axis.set_xlabel(r"$N_{RI}/N_{AO}$")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False)
    fig.text(0.5, 0.008, "GW100: optimized 100/100 per point; tabulated coverage 100, 100, 100, 100, 91, 89, 77/100.\n"
             "GW100 optimized: RI neighbors 3 Å, RS/AO=7; tabulated: earlier grid setup. Silicon: atom-local RI.\n"
             "Horizontal axis: requested RI/AO for optimized bases; mean actual ratio for tabulated GW100.",
             ha="center", fontsize=9)
    fig.tight_layout(rect=(0, 0.065, 1, 0.965))
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_csv(path: Path, rows: list[dict]) -> None:
    fieldnames = (
        "system",
        "orbital",
        "series",
        "method",
        "neighbor_radius_angstrom",
        "point",
        "x_ri_ao_ratio",
        "valid_calculations",
        "error_raw_meV",
        "error_plotted_meV",
        "expected_calculations", "coverage", "p95_abs_error_meV",
        "max_abs_error_meV", "worst_case", "worst_signed_error_meV", "raw_directory",
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({
                key: format(value, ".12g") if isinstance(value, float) else value
                for key, value in row.items()
            })


def main() -> None:
    support = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=support.parent)
    parser.add_argument("--output-dir", type=Path, default=support)
    args = parser.parse_args()
    repo = args.repo.resolve(strict=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    references = load_references(repo)
    rows, validation = collect(repo, references)
    csv_path = args.output_dir / "Figure_3_created.csv"
    png_path = args.output_dir / "Figure_3_created.png"
    write_csv(csv_path, rows)
    plot(png_path, rows)
    print(
        f"Read {validation['valid_calculations']} valid calculations, "
        f"{validation['excluded_calculations']} exclusions, and "
        f"{validation['reference_paired_calculations']} TensorGW comparison pairs"
    )
    print(f"Wrote {csv_path}")
    print(f"Wrote {png_path}")


if __name__ == "__main__":
    main()
