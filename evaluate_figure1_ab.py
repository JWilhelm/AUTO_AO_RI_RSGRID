#!/usr/bin/env python3
"""Reproduce the mean absolute errors plotted in Figure 1(a,b).

The script uses only Python's standard library and reads the archived CP2K
outputs directly.  Figure 1(a) is the PBE gap error and Figure 1(b) is the
G0W0 gap error, both relative to the 99 aug-TZVP-t1 reference calculations.
"""

from __future__ import annotations

import csv
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
REFERENCE = "Reference_aug-TZVP-t1"
FAMILIES = ("aug-SZV-t1", "aug-SZV-t2", "aug-DZVP-t1", "aug-DZVP-t2")
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
        raise ValueError(f"missing output value matching {pattern!r}")
    return float(values[-1])


def checked_text(path: Path) -> str:
    text = path.read_text(errors="replace")
    if "PROGRAM ENDED AT" not in text or FATAL.search(text):
        raise ValueError(f"incomplete or failed calculation: {path}")
    return text


def parse_compact(path: Path) -> dict[str, float]:
    text = checked_text(path)
    pbe_h = last_float(r"(?:PBE|SCF) valence band maximum \(eV\):\s*([-+0-9.Ee]+)", text)
    pbe_l = last_float(r"(?:PBE|SCF) conduction band minimum \(eV\):\s*([-+0-9.Ee]+)", text)
    gw_h = last_float(r"G0W0 valence band maximum \(eV\):\s*([-+0-9.Ee]+)", text)
    gw_l = last_float(r"G0W0 conduction band minimum \(eV\):\s*([-+0-9.Ee]+)", text)
    return {"pbe_gap_ev": pbe_l - pbe_h, "g0w0_gap_ev": gw_l - gw_h}


def parse_reference(path: Path) -> dict[str, float]:
    text = checked_text(path)
    marker = text.rfind("G0W0 results")
    if marker < 0:
        raise ValueError(f"missing G0W0 results block: {path}")
    block = text[marker:]
    rows = [
        (match.group(2), float(match.group(3)), float(match.group(6)))
        for match in N4_ROW.finditer(block)
    ]
    occupied = [row for row in rows if row[0] == "occ"]
    virtual = [row for row in rows if row[0] == "vir"]
    gap_match = N4_GAP.search(block)
    if not occupied or not virtual or gap_match is None:
        raise ValueError(f"incomplete G0W0 results block: {path}")
    pbe_gap = min(row[1] for row in virtual) - max(row[1] for row in occupied)
    gw_gap = min(row[2] for row in virtual) - max(row[2] for row in occupied)
    if abs(gw_gap - float(gap_match.group(1))) >= 2.1e-4:
        raise ValueError(f"reported/parsed G0W0 gap mismatch: {path}")
    return {"pbe_gap_ev": pbe_gap, "g0w0_gap_ev": gw_gap}


def molecule_names(reference_root: Path) -> list[str]:
    excluded = reference_root / "05_Xe" / "EXCLUDED.txt"
    if not excluded.is_file():
        raise ValueError(f"missing Xe exclusion marker: {excluded}")
    names = sorted(
        directory.name
        for directory in reference_root.iterdir()
        if directory.is_dir() and (directory / "output.log").is_file()
    )
    if len(names) != 99:
        raise ValueError(f"expected 99 references in {reference_root}, found {len(names)}")
    return names


def main() -> None:
    reference_roots = [ROOT / "Figure_1a" / REFERENCE, ROOT / "Figure_1b" / REFERENCE]
    names = molecule_names(reference_roots[0])
    if molecule_names(reference_roots[1]) != names:
        raise ValueError("Figure 1(a) and 1(b) reference molecule sets differ")

    references = {
        molecule: parse_reference(reference_roots[0] / molecule / "output.log")
        for molecule in names
    }
    for molecule in names:
        if (reference_roots[0] / molecule / "output.log").read_bytes() != (
            reference_roots[1] / molecule / "output.log"
        ).read_bytes():
            raise ValueError(f"Figure 1(a,b) reference outputs differ for {molecule}")

    rows: list[dict[str, str]] = []
    for label in FAMILIES:
        for variant in ("Initial", "Optimized"):
            directory = f"{variant}_{label}"
            for panel, metric in (("a", "pbe_gap_ev"), ("b", "g0w0_gap_ev")):
                values = {
                    molecule: parse_compact(
                        ROOT / f"Figure_1{panel}" / directory / molecule / "output.log"
                    )
                    for molecule in names
                }
                mae = sum(
                    abs(values[molecule][metric] - references[molecule][metric])
                    for molecule in names
                ) / len(names)
                rows.append(
                    {
                        "panel": panel,
                        "basis": label,
                        "variant": variant.lower(),
                        "n": str(len(names)),
                        "mae_ev": f"{mae:.12f}",
                    }
                )

    csv_path = ROOT / "FIGURE_1_AB_VALUES.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("panel", "basis", "variant", "n", "mae_ev"))
        writer.writeheader()
        writer.writerows(rows)

    print("panel basis         variant     n  MAE/eV")
    for row in rows:
        print(
            f"{row['panel']:>5} {row['basis']:<13} {row['variant']:<9} "
            f"{row['n']:>3}  {float(row['mae_ev']):.6f}"
        )
    print(f"\nWrote {csv_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
