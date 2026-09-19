#!/usr/bin/env python3
"""Recreate all numerical data and a standalone SVG for Figure 2.

The script uses only Python's standard library.  Run it from the repository
root after cloning the complete repository.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import csv
import html
import json
import math
from pathlib import Path
import re
import statistics


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
    ("GW100", "Figure_2a"),
    ("Si45H56", "Figure_2c"),
    ("Si293H172", "Figure_2e"),
)
RADII = {"0p5": 0.5, "3": 3.0, "5": 5.0}
SERIES = ("auto_r0.5", "auto_r3", "auto_r5", "tabulated")
COLORS = {
    "auto_r0.5": "#0072B2",
    "auto_r3": "#E69F00",
    "auto_r5": "#009E73",
    "tabulated": "#222222",
}
LABELS = {
    "auto_r0.5": "R_RI = 0.5 A",
    "auto_r3": "R_RI = 3 A",
    "auto_r5": "R_RI = 5 A",
    "tabulated": "tabulated RI",
}


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
    raise RuntimeError(f"Unexpected Figure 2 point directory: {name}")


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
                        "error_plotted_meV": max(1.0, error),
                    }
                )

    if valid_count != 2505 or excluded_count != 43 or len(rows) != 146:
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


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def svg_marker(x: float, y: float, series: str) -> str:
    color = COLORS[series]
    if series == "auto_r0.5":
        return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="{color}" stroke="white"/>'
    if series == "auto_r3":
        return f'<rect x="{x-5:.2f}" y="{y-5:.2f}" width="10" height="10" fill="{color}" stroke="white"/>'
    if series == "auto_r5":
        points = f"{x:.2f},{y-6:.2f} {x-6:.2f},{y+5:.2f} {x+6:.2f},{y+5:.2f}"
        return f'<polygon points="{points}" fill="{color}" stroke="white"/>'
    points = f"{x:.2f},{y-7:.2f} {x-7:.2f},{y:.2f} {x:.2f},{y+7:.2f} {x+7:.2f},{y:.2f}"
    return f'<polygon points="{points}" fill="{color}" stroke="white"/>'


def render_svg(path: Path, rows: list[dict]) -> None:
    width, height = 1400, 1800
    left, top, right, bottom = 120, 160, 65, 115
    gap_x, gap_y = 80, 90
    panel_w = (width - left - right - gap_x) / 2
    panel_h = (height - top - bottom - 2 * gap_y) / 3
    xmin, xmax = 0.70, 5.35
    panels = (
        ("GW100", "homo", "(a) GW100 — G0W0 HOMO", "MAE (meV)", 6.0, 1300.0),
        ("GW100", "lumo", "(b) GW100 — G0W0 LUMO", "", 6.0, 1300.0),
        ("Si45H56", "homo", "(c) Si45H56 — G0W0 HOMO", "Abs. error (meV)", 0.8, 300.0),
        ("Si45H56", "lumo", "(d) Si45H56 — G0W0 LUMO", "", 0.8, 300.0),
        ("Si293H172", "homo", "(e) Si293H172 — G0W0 HOMO", "Abs. error (meV)", 0.8, 300.0),
        ("Si293H172", "lumo", "(f) Si293H172 — G0W0 LUMO", "", 0.8, 300.0),
    )
    lookup: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for row in rows:
        lookup[(row["system"], row["orbital"], row["series"])].append(row)
    for values in lookup.values():
        values.sort(key=lambda row: float(row["x_ri_ao_ratio"]))

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:DejaVu Sans,Arial,sans-serif;fill:#111}.tick{font-size:18px}.label{font-size:22px}.title{font-size:20px;font-weight:bold}.legend{font-size:19px}</style>',
        '<defs>',
    ]
    for index in range(6):
        row_index, col_index = divmod(index, 2)
        x0 = left + col_index * (panel_w + gap_x)
        y0 = top + row_index * (panel_h + gap_y)
        out.append(f'<clipPath id="clip{index}"><rect x="{x0:.2f}" y="{y0:.2f}" width="{panel_w:.2f}" height="{panel_h:.2f}"/></clipPath>')
    out.append('</defs>')

    legend_x = 135
    for series in SERIES:
        color = COLORS[series]
        out.append(f'<line x1="{legend_x}" y1="72" x2="{legend_x+45}" y2="72" stroke="{color}" stroke-width="4"/>')
        out.append(svg_marker(legend_x + 22.5, 72, series))
        out.append(f'<text class="legend" x="{legend_x+55}" y="79">{html.escape(LABELS[series])}</text>')
        legend_x += 310

    for index, (system, orbital, title, ylabel, ymin, ymax) in enumerate(panels):
        panel_row, panel_col = divmod(index, 2)
        x0 = left + panel_col * (panel_w + gap_x)
        y0 = top + panel_row * (panel_h + gap_y)
        x1, y1 = x0 + panel_w, y0 + panel_h

        def map_x(value: float) -> float:
            return x0 + (value - xmin) / (xmax - xmin) * panel_w

        def map_y(value: float) -> float:
            return y1 - (math.log10(value) - math.log10(ymin)) / (math.log10(ymax) - math.log10(ymin)) * panel_h

        for tick in range(1, 6):
            px = map_x(tick)
            out.append(f'<line x1="{px:.2f}" y1="{y0:.2f}" x2="{px:.2f}" y2="{y1:.2f}" stroke="#d7d7d7"/>')
            if panel_row == 2:
                out.append(f'<text class="tick" x="{px:.2f}" y="{y1+27:.2f}" text-anchor="middle">{tick}</text>')
        for decade in range(math.floor(math.log10(ymin)), math.ceil(math.log10(ymax)) + 1):
            for multiplier in range(1, 10):
                value = multiplier * 10**decade
                if not ymin <= value <= ymax:
                    continue
                py = map_y(value)
                major = multiplier == 1
                out.append(
                    f'<line x1="{x0:.2f}" y1="{py:.2f}" x2="{x1:.2f}" y2="{py:.2f}" '
                    f'stroke="{"#c5c5c5" if major else "#e8e8e8"}" stroke-width="{"1.5" if major else "1"}"/>'
                )
                if panel_col == 0 and major:
                    label = "1" if decade == 0 else f"10^{decade}"
                    out.append(f'<text class="tick" x="{x0-12:.2f}" y="{py+6:.2f}" text-anchor="end">{label}</text>')

        out.append(f'<g clip-path="url(#clip{index})">')
        for series in SERIES:
            values = lookup[(system, orbital, series)]
            coords = [(map_x(float(row["x_ri_ao_ratio"])), map_y(float(row["error_plotted_meV"]))) for row in values]
            coordinate_text = " ".join(f"{x:.2f},{y:.2f}" for x, y in coords)
            out.append(f'<polyline points="{coordinate_text}" fill="none" stroke="{COLORS[series]}" stroke-width="4"/>')
            out.extend(svg_marker(x, y, series) for x, y in coords)
        out.append('</g>')
        out.append(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{panel_w:.2f}" height="{panel_h:.2f}" fill="none" stroke="#222" stroke-width="2"/>')
        out.append(f'<rect x="{x1-325:.2f}" y="{y0+12:.2f}" width="313" height="34" rx="4" fill="white" fill-opacity="0.92"/>')
        out.append(f'<text class="title" x="{x1-20:.2f}" y="{y0+36:.2f}" text-anchor="end">{html.escape(title)}</text>')
        if ylabel:
            cy = (y0 + y1) / 2
            out.append(f'<text class="label" x="{x0-82:.2f}" y="{cy:.2f}" text-anchor="middle" transform="rotate(-90 {x0-82:.2f} {cy:.2f})">{html.escape(ylabel)}</text>')

    out.append(f'<text class="label" x="{width/2:.2f}" y="{height-42}" text-anchor="middle">alpha_RI in N_RI = alpha_RI N_AO</text>')
    out.append('</svg>')
    path.write_text("\n".join(out) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument(
        "--references",
        type=Path,
        default=Path(__file__).resolve().with_name("FIGURE_2_REFERENCE_VALUES.json"),
    )
    args = parser.parse_args()
    repo = args.repo.resolve(strict=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    references = json.loads(args.references.read_text())
    if len(references["gw100"]) != 100:
        raise RuntimeError("FIGURE_2_REFERENCE_VALUES.json must contain 100 GW100 references")
    rows, validation = collect(repo, references)
    write_csv(args.output_dir / "FIGURE_2_VALUES.csv", rows)
    render_svg(args.output_dir / "FIGURE_2_RECREATED.svg", rows)
    summary = {
        "reference_file": args.references.name,
        "figure_file": "FIGURE_2_RECREATED.svg",
        "values_file": "FIGURE_2_VALUES.csv",
        "display_floor_meV": 1.0,
        "validation": validation,
        "si293h172_reference_note": references["si293h172"]["note"],
    }
    (args.output_dir / "FIGURE_2_REPRODUCTION.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
