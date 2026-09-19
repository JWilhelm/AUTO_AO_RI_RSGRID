#!/usr/bin/env python3
"""Recompute and plot all eighteen panels of Figure 3 from archived outputs.

The calculation outputs and TensorGW reference outputs are parsed directly.
GW100 statistics always use all 100 molecules.  A GW100 point fails instead
of silently dropping a missing, invalid, or state-mismatched molecule.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from pathlib import Path


HOMO_RE = re.compile(r"G0W0 valence band maximum \(eV\):\s+([-+0-9.Ee]+)")
LUMO_RE = re.compile(r"G0W0 conduction band minimum \(eV\):\s+([-+0-9.Ee]+)")
ENERGY_RE = re.compile(
    r"ENERGY\|\s+Total FORCE_EVAL .*?energy \[(?:a\.u\.|hartree)\]\s+([-+0-9.Ee]+)",
    re.I,
)
FATAL_RE = re.compile(
    r"MPI_ABORT|SIGSEGV|Segmentation fault|Abnormal program termination|"
    r"CPASSERT|ASSERTION FAILED|out of memory|oom-kill",
    re.I,
)
POINT_RE = re.compile(r"RI-AO-ratio-([2345])_RS-AO-ratio-(\d+)$")

PANELS = {
    "a": ("GW100", 0.5, "HOMO"), "b": ("GW100", 0.5, "LUMO"),
    "c": ("GW100", 3.0, "HOMO"), "d": ("GW100", 3.0, "LUMO"),
    "e": ("GW100", 5.0, "HOMO"), "f": ("GW100", 5.0, "LUMO"),
    "g": ("Si45H56", 0.5, "HOMO"), "h": ("Si45H56", 0.5, "LUMO"),
    "i": ("Si45H56", 3.0, "HOMO"), "j": ("Si45H56", 3.0, "LUMO"),
    "k": ("Si45H56", 5.0, "HOMO"), "l": ("Si45H56", 5.0, "LUMO"),
    "m": ("Si293H172", 0.5, "HOMO"), "n": ("Si293H172", 0.5, "LUMO"),
    "o": ("Si293H172", 3.0, "HOMO"), "p": ("Si293H172", 3.0, "LUMO"),
    "q": ("Si293H172", 5.0, "HOMO"), "r": ("Si293H172", 5.0, "LUMO"),
}
COLORS = {2: "#E69F00", 3: "#0072B2", 4: "#009E73", 5: "#D55E00"}


def parse_output(path: Path, require_rirs: bool) -> dict[str, float]:
    text = path.read_text(errors="replace")
    if "PROGRAM ENDED AT" not in text or FATAL_RE.search(text):
        raise RuntimeError(f"invalid or incomplete output: {path}")
    if require_rirs and "RI-RS grid optimization completed" not in text:
        raise RuntimeError(f"RI-RS optimization did not complete: {path}")
    homo, lumo, energy = HOMO_RE.findall(text), LUMO_RE.findall(text), ENERGY_RE.findall(text)
    if not homo or not lumo or not energy:
        raise RuntimeError(f"missing HOMO, LUMO, or total energy: {path}")
    return {"HOMO": float(homo[-1]), "LUMO": float(lumo[-1]), "energy": float(energy[-1])}


def percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    lo, hi = math.floor(position), math.ceil(position)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] * (hi - position) + ordered[hi] * (position - lo)


def load_references(repo: Path) -> dict[tuple[str, str], dict[str, float | None]]:
    tensor_root = repo / "TensorGW_Calculations"
    gw_root = tensor_root / "GW100_TensorGW"
    case_dirs = sorted(path for path in gw_root.iterdir() if path.is_dir())
    if len(case_dirs) != 100:
        raise RuntimeError(f"expected 100 GW100 TensorGW calculations; found {len(case_dirs)}")
    references: dict[tuple[str, str], dict[str, float | None]] = {}
    for case_dir in case_dirs:
        references[("GW100", case_dir.name)] = parse_output(
            case_dir / "output.log", require_rirs=False
        )
    references[("Si45H56", "Si45H56")] = parse_output(
        tensor_root / "Si45H56_TensorGW" / "output.log", require_rirs=False
    )
    references[("Si293H172", "Si293H172")] = parse_output(
        repo
        / "Figure_2e"
        / "AUTO-RI_radius-0p5_RI-AO-ratio-3"
        / "output.log",
        require_rirs=True,
    )
    return references


def calculate(repo: Path) -> list[dict]:
    references = load_references(repo)
    expected_points = tuple(
        f"RI-AO-ratio-{ratio}_RS-AO-ratio-{alpha}"
        for ratio in (2, 3, 4, 5) for alpha in range(2, 11)
    )
    rows = []
    cache: dict[Path, dict[str, float]] = {}
    for letter, (system, radius, orbital) in PANELS.items():
        panel_dir = repo / f"Figure_3{letter}"
        actual_points = {p.name for p in panel_dir.iterdir() if p.is_dir()}
        if actual_points != set(expected_points):
            raise RuntimeError(f"Figure_3{letter} point topology mismatch")
        for point_name in expected_points:
            match = POINT_RE.fullmatch(point_name)
            assert match is not None
            ratio, alpha = int(match.group(1)), int(match.group(2))
            point_dir = panel_dir / point_name
            calc_dirs = sorted(p for p in point_dir.iterdir() if p.is_dir()) if system == "GW100" else [point_dir]
            expected_n = 100 if system == "GW100" else 1
            if len(calc_dirs) != expected_n:
                raise RuntimeError(f"Figure_3{letter}/{point_name}: {len(calc_dirs)}/{expected_n} outputs")
            errors, signed = [], []
            worst_molecule = ""
            for calc_dir in calc_dirs:
                output = calc_dir / "output.log"
                if output not in cache:
                    cache[output] = parse_output(output, require_rirs=True)
                value = cache[output]
                molecule = calc_dir.name if system == "GW100" else system
                reference = references[(system, molecule)]
                if reference["energy"] is not None and abs(value["energy"] - reference["energy"]) > 1.0e-6:
                    raise RuntimeError(
                        f"SCF state mismatch: {output} differs from its reference by "
                        f"{value['energy'] - reference['energy']:.3e} hartree"
                    )
                delta = (value[orbital] - reference[orbital]) * 1000.0
                signed.append(delta)
                errors.append(abs(delta))
            worst_index = max(range(len(errors)), key=errors.__getitem__)
            if system == "GW100":
                worst_molecule = calc_dirs[worst_index].name
                recomputed = sum(errors) / 100.0
                display = recomputed
                p95 = percentile(errors, 0.95)
            else:
                worst_molecule = system
                recomputed = errors[0]
                display = max(1.0, float(round(recomputed)))
                p95 = recomputed
            rows.append({
                "panel": letter,
                "system": system,
                "radius_angstrom": radius,
                "orbital": orbital,
                "ri_ao_ratio": ratio,
                "rs_ao_ratio": alpha,
                "coverage": f"{len(errors)}/{expected_n}",
                "raw_error_meV": recomputed,
                "error_meV": display,
                "p95_abs_error_meV": p95,
                "max_abs_error_meV": max(errors),
                "worst_molecule": worst_molecule,
                "worst_signed_error_meV": signed[worst_index],
            })
    return rows


def plot(rows: list[dict], output: Path) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("Plotting requires matplotlib (python -m pip install matplotlib)") from exc
    lookup = {
        (r["panel"], int(r["ri_ao_ratio"]), int(r["rs_ao_ratio"])): float(r["error_meV"])
        for r in rows
    }
    fig, axes = plt.subplots(3, 6, figsize=(15.5, 8.2), sharex=True, sharey=True)
    for ax, (letter, (system, radius, orbital)) in zip(axes.flat, PANELS.items()):
        for ratio in (2, 3, 4, 5):
            x = list(range(2, 11))
            y = [lookup[(letter, ratio, alpha)] for alpha in x]
            ax.plot(x, y, "o-", ms=3.0, lw=1.15, color=COLORS[ratio], label=f"$N_{{RI}}={ratio}N_{{AO}}$")
        ax.set_yscale("log")
        ax.set_ylim(0.9, 1100)
        ax.set_xticks([2, 4, 6, 8, 10])
        ax.grid(True, which="both", alpha=0.25)
        ax.set_title(f"({letter}) {system} {orbital}; $R_{{RS}}={radius:g}$ Å", fontsize=8)
    for ax in axes[:, 0]:
        ax.set_ylabel("error (meV)")
    for ax in axes[-1, :]:
        ax.set_xlabel(r"$N_{RS}/N_{AO}$")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, 0.995))
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_csv(path: Path, rows: list[dict]) -> None:
    fieldnames = (
        "panel",
        "system",
        "radius_angstrom",
        "orbital",
        "ri_ao_ratio",
        "rs_ao_ratio",
        "coverage",
        "raw_error_meV",
        "error_meV",
        "p95_abs_error_meV",
        "max_abs_error_meV",
        "worst_molecule",
        "worst_signed_error_meV",
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
    repo = args.repo.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    rows = calculate(repo)
    gw = [r for r in rows if r["system"] == "GW100"]
    nano = [r for r in rows if r["system"] != "GW100"]
    if len(rows) != 648 or len(gw) != 216 or len(nano) != 432:
        raise RuntimeError(
            f"unexpected Figure 3 coverage: total={len(rows)}, GW100={len(gw)}, nanoclusters={len(nano)}"
        )
    if any(row["coverage"] != "100/100" for row in gw):
        raise RuntimeError("not every GW100 point contains all 100 molecules")
    csv_path = output / "Figure_3_created.csv"
    png_path = output / "Figure_3_created.png"
    write_csv(csv_path, rows)
    plot(rows, png_path)
    print("Read 648 plotted values directly from the archived calculations")
    print("Every GW100 point contains all 100 molecules")
    print(f"Wrote {csv_path}")
    print(f"Wrote {png_path}")


if __name__ == "__main__":
    main()
