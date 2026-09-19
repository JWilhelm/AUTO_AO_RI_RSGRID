#!/usr/bin/env python3
"""Recompute and plot all six panels of Figure 1 from archived CP2K outputs."""

from __future__ import annotations

import argparse
from pathlib import Path
import re


FAMILIES = ("aug-SZV-t1", "aug-SZV-t2", "aug-DZVP-t1", "aug-DZVP-t2")
PANELS = ("a", "b", "c", "d", "e", "f")
FATAL = re.compile(
    r"\[(?:ABORT|ASSERT)\]|CPASSERT|MPI_ABORT|SIGSEGV|segmentation fault|"
    r"out of memory|oom.kill|Killed process|Cannot allocate memory",
    re.I,
)
N4_ROW = re.compile(
    r"^\s*(\d+)\s+\(\s*(occ|vir)\s*\)\s+"
    r"([-+0-9.Ee]+)\s+([-+0-9.Ee]+)\s+([-+0-9.Ee]+)\s+([-+0-9.Ee]+)\s*$",
    re.M,
)
N4_GAP = re.compile(r"G0W0 HOMO-LUMO gap \(eV\)\s+([-+0-9.Ee]+)")


def last_float(pattern: str, text: str) -> float:
    values = re.findall(pattern, text, re.I | re.M)
    if not values:
        raise RuntimeError(f"missing output value matching {pattern!r}")
    return float(values[-1])


def checked_text(path: Path) -> str:
    text = path.read_text(errors="replace")
    if "PROGRAM ENDED AT" not in text or FATAL.search(text):
        raise RuntimeError(f"incomplete or failed calculation: {path}")
    return text


def parse_compact(path: Path) -> dict[str, float]:
    text = checked_text(path)
    pbe_homo = last_float(
        r"(?:PBE|SCF) valence band maximum \(eV\):\s*([-+0-9.Ee]+)", text
    )
    pbe_lumo = last_float(
        r"(?:PBE|SCF) conduction band minimum \(eV\):\s*([-+0-9.Ee]+)", text
    )
    gw_homo = last_float(r"G0W0 valence band maximum \(eV\):\s*([-+0-9.Ee]+)", text)
    gw_lumo = last_float(r"G0W0 conduction band minimum \(eV\):\s*([-+0-9.Ee]+)", text)
    return {
        "pbe_gap_ev": pbe_lumo - pbe_homo,
        "g0w0_gap_ev": gw_lumo - gw_homo,
        "pbe_direct_gap_ev": last_float(
            r"SCF indirect band gap \(eV\):\s*([-+0-9.Ee]+)", text
        ),
        "g0w0_direct_gap_ev": last_float(
            r"G0W0 indirect band gap \(eV\):\s*([-+0-9.Ee]+)", text
        ),
    }


def parse_reference(path: Path) -> dict[str, float]:
    text = checked_text(path)
    marker = text.rfind("G0W0 results")
    if marker < 0:
        raise RuntimeError(f"missing G0W0 results block: {path}")
    block = text[marker:]
    rows = [(m.group(2), float(m.group(3)), float(m.group(6))) for m in N4_ROW.finditer(block)]
    occupied = [row for row in rows if row[0] == "occ"]
    virtual = [row for row in rows if row[0] == "vir"]
    reported_gap = N4_GAP.search(block)
    if not occupied or not virtual or reported_gap is None:
        raise RuntimeError(f"incomplete G0W0 results block: {path}")
    result = {
        "pbe_gap_ev": min(row[1] for row in virtual) - max(row[1] for row in occupied),
        "g0w0_gap_ev": min(row[2] for row in virtual) - max(row[2] for row in occupied),
    }
    if abs(result["g0w0_gap_ev"] - float(reported_gap.group(1))) >= 2.1e-4:
        raise RuntimeError(f"reported/parsed G0W0 gap mismatch: {path}")
    return result


def reference_names(reference_root: Path) -> list[str]:
    excluded = reference_root / "05_Xe" / "EXCLUDED.txt"
    if not excluded.is_file():
        raise RuntimeError(f"missing Xe exclusion marker: {excluded}")
    names = sorted(
        path.name
        for path in reference_root.iterdir()
        if path.is_dir() and (path / "output.log").is_file()
    )
    if len(names) != 99:
        raise RuntimeError(f"expected 99 references in {reference_root}, found {len(names)}")
    return names


def collect(repo: Path) -> list[dict[str, str | float | int]]:
    reference_roots = [
        repo / "Figure_1a" / "Reference_aug-TZVP-t1",
        repo / "Figure_1b" / "Reference_aug-TZVP-t1",
    ]
    names = reference_names(reference_roots[0])
    if reference_names(reference_roots[1]) != names:
        raise RuntimeError("Figure 1(a) and 1(b) reference molecule sets differ")
    references = {
        name: parse_reference(reference_roots[0] / name / "output.log") for name in names
    }
    for name in names:
        if (reference_roots[0] / name / "output.log").read_bytes() != (
            reference_roots[1] / name / "output.log"
        ).read_bytes():
            raise RuntimeError(f"Figure 1(a,b) reference outputs differ for {name}")

    rows: list[dict[str, str | float | int]] = []
    for panel, metric in (("a", "pbe_gap_ev"), ("b", "g0w0_gap_ev")):
        for variant in ("Initial", "Optimized"):
            for basis in FAMILIES:
                directory = repo / f"Figure_1{panel}" / f"{variant}_{basis}"
                values = {
                    name: parse_compact(directory / name / "output.log") for name in names
                }
                mae = sum(
                    abs(values[name][metric] - references[name][metric]) for name in names
                ) / len(names)
                rows.append(
                    {
                        "panel": panel,
                        "system": "GW100",
                        "metric": "PBE gap MAE" if panel == "a" else "G0W0 gap MAE",
                        "basis": basis,
                        "variant": variant.lower(),
                        "sample_count": len(names),
                        "value_ev": mae,
                    }
                )

    for panel, system, metric in (
        ("c", "Si45H56", "pbe_direct_gap_ev"),
        ("d", "Si45H56", "g0w0_direct_gap_ev"),
        ("e", "Si293H172", "pbe_direct_gap_ev"),
        ("f", "Si293H172", "g0w0_direct_gap_ev"),
    ):
        for variant in ("Initial", "Optimized"):
            prefix = "Optimized-for-Si45H56" if panel in "ef" and variant == "Optimized" else variant
            for basis in FAMILIES:
                output = repo / f"Figure_1{panel}" / f"{prefix}_{basis}" / "output.log"
                rows.append(
                    {
                        "panel": panel,
                        "system": system,
                        "metric": "PBE gap" if metric == "pbe_direct_gap_ev" else "G0W0 gap",
                        "basis": basis,
                        "variant": variant.lower(),
                        "sample_count": 1,
                        "value_ev": parse_compact(output)[metric],
                    }
                )
    return rows


def plot(path: Path, rows: list[dict[str, str | float | int]]) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.ticker import AutoMinorLocator
    except ImportError as exc:
        raise RuntimeError("plotting requires matplotlib (python -m pip install matplotlib)") from exc

    values = {
        (str(row["panel"]), str(row["variant"]), str(row["basis"])): float(row["value_ev"])
        for row in rows
    }
    ylabels = {
        "a": "MAE of PBE gap (eV)",
        "b": r"MAE of $G_0W_0$ gap (eV)",
        "c": "PBE gap (eV)",
        "d": r"$G_0W_0$ gap (eV)",
        "e": "PBE gap (eV)",
        "f": r"$G_0W_0$ gap (eV)",
    }
    titles = {
        "a": r"$\mathit{GW}100$",
        "b": r"$\mathit{GW}100$",
        "c": r"Si$_{45}$H$_{56}$",
        "d": r"Si$_{45}$H$_{56}$",
        "e": r"Si$_{293}$H$_{172}$",
        "f": r"Si$_{293}$H$_{172}$",
    }
    limits = {
        "a": (0.0, 0.5), "b": (0.0, 1.0), "c": (3.05, 3.65),
        "d": (5.65, 6.35), "e": (1.55, 2.15), "f": (3.15, 3.85),
    }
    ticks = {
        "a": [0, .1, .2, .3, .4, .5], "b": [0, .2, .4, .6, .8, 1.0],
        "c": [3.1, 3.2, 3.3, 3.4, 3.5, 3.6],
        "d": [5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3],
        "e": [1.6, 1.7, 1.8, 1.9, 2.0, 2.1],
        "f": [3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8],
    }
    plt.rcParams.update({"font.family": "serif", "font.size": 10})
    fig, axes = plt.subplots(3, 2, figsize=(10.6, 7.4), sharex="col")
    x = range(1, 5)
    for panel, axis in zip(PANELS, axes.flat):
        initial = [values[(panel, "initial", basis)] for basis in FAMILIES]
        optimized = [values[(panel, "optimized", basis)] for basis in FAMILIES]
        optimized_color = "#00A6D6" if panel in "ef" else "#0072B2"
        optimized_label = r"Optimized for Si$_{45}$H$_{56}$" if panel in "ef" else "Optimized"
        axis.plot(x, initial, "o--", color="#777777", lw=1.4, ms=4.5, label="Initial")
        axis.plot(x, optimized, "o-", color=optimized_color, lw=1.5, ms=4.5, label=optimized_label)
        axis.set_xlim(0.6, 4.4)
        axis.set_ylim(*limits[panel])
        axis.set_yticks(ticks[panel])
        axis.yaxis.set_minor_locator(AutoMinorLocator(2))
        axis.grid(True, which="major", color="#c7c7c7", lw=0.55, alpha=0.75)
        axis.grid(True, which="minor", color="#dddddd", lw=0.35, alpha=0.55)
        axis.set_ylabel(ylabels[panel])
        axis.text(0.02, 0.95, f"({panel})", transform=axis.transAxes, va="top")
        axis.text(
            0.50, 0.95, titles[panel], transform=axis.transAxes, ha="center", va="top",
            bbox={"boxstyle": "round,pad=0.16", "facecolor": "white", "edgecolor": "#cccccc"},
        )
        if panel == "a":
            axis.legend(loc="upper right", bbox_to_anchor=(0.99, 0.84), ncol=2)
        if panel == "e":
            axis.legend(loc="upper right", bbox_to_anchor=(0.99, 0.72))
    for axis in axes[-1, :]:
        axis.set_xticks(list(x), FAMILIES)
    fig.subplots_adjust(left=0.105, right=0.985, top=0.985, bottom=0.10, wspace=0.26, hspace=0.12)
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    support = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=support.parent)
    parser.add_argument("--output-dir", type=Path, default=support)
    args = parser.parse_args()
    repo = args.repo.resolve(strict=True)
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    rows = collect(repo)
    plot(output / "Figure_1.png", rows)
    print(f"Read {len(rows)} values from the archived calculations")
    print(f"Wrote {output / 'Figure_1.png'}")


if __name__ == "__main__":
    main()
