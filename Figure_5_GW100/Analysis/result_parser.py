#!/usr/bin/env python3
"""Summarize campaign 418 against molecule-matched TensorGW references."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?"
HOMO = "G0W0 valence band maximum (eV):"
LUMO = "G0W0 conduction band minimum (eV):"
DFT = "ENERGY| Total FORCE_EVAL ( QS ) energy [hartree]"
EXCLUDED_MOLECULES = set()  # Jan restored the complete GW100 dataset on 2026-10-03.


def read_result(path: Path):
    if not path.is_file():
        return None, "missing"
    text = path.read_text(errors="replace")
    if "PROGRAM ENDED AT" not in text:
        return None, "unfinished"
    if "SCF run converged in" not in text or re.search(r"Density guess:\s+RESTART", text) is None:
        return None, "SCF or restart not confirmed"
    values = []
    for label in (HOMO, LUMO, DFT):
        found = re.findall(re.escape(label) + r"\s*(" + NUMBER + r")", text)
        if len(found) != 1:
            return None, f"{label}: expected one value, got {len(found)}"
        value = float(found[0])
        if not math.isfinite(value):
            return None, f"{label}: nonfinite"
        values.append(value)
    return values, None


def summarize(pairs, radius, ri, rs, orbital):
    index = 0 if orbital == "HOMO" else 1
    signed = [(molecule, value[index]) for molecule, value in pairs]
    absolute = sorted(abs(value) for _, value in signed)
    worst_molecule, worst_signed = max(signed, key=lambda row: abs(row[1]))
    return {
        "radius_A": radius,
        "ri_ao_ratio": ri,
        "rs_ao_ratio": rs,
        "orbital": orbital,
        "n": len(pairs),
        "mae_meV": sum(absolute) / len(absolute),
        "p95_meV": absolute[math.ceil(0.95 * len(absolute)) - 1],
        "max_abs_meV": abs(worst_signed),
        "worst_molecule": worst_molecule,
        "worst_signed_meV": worst_signed,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("campaign", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--reference-selection", type=Path,
                        help="Explicit, provenance-tracked replacement Tensor references")
    args = parser.parse_args()
    manifest = json.loads((args.campaign / "manifest.json").read_text())
    selection = None
    if args.reference_selection:
        selection = json.loads(args.reference_selection.read_text())
        manifest["references"] = selection["references"]
    references = {}
    invalid_references = {}
    for item in manifest["references"]:
        output = Path(item.get("output", str(Path(item["run"]) / "output.log")))
        result, problem = read_result(output)
        if item["molecule"] in EXCLUDED_MOLECULES:
            invalid_references[item["molecule"]] = (
                "excluded from Figure 5(a-f) by Jan; "
                + (problem or f"TensorGW HOMO/LUMO={result[0]:.3f}/{result[1]:.3f} eV")
            )
        elif problem:
            invalid_references[item["molecule"]] = problem
        elif result[1] <= result[0]:
            invalid_references[item["molecule"]] = (
                f"nonpositive QP gap: HOMO={result[0]:.3f}, LUMO={result[1]:.3f} eV"
            )
        else:
            references[item["molecule"]] = result

    grouped = defaultdict(list)
    missing = Counter()
    mismatched = []
    for item in manifest["calculations"]:
        result, problem = read_result(Path(item["run"]) / "output.log")
        if problem:
            missing[problem] += 1
            continue
        molecule = item["molecule"]
        if molecule not in references:
            missing["invalid or missing TensorGW reference"] += 1
            continue
        ref = references[molecule]
        if abs(result[2] - ref[2]) > 1e-7:
            mismatched.append((molecule, item["radius_A"], item["ri_ao_ratio"], item["rs_ao_ratio"]))
            missing["DFT state mismatch"] += 1
            continue
        key = item["radius_A"], item["ri_ao_ratio"], item["rs_ao_ratio"]
        grouped[key].append((molecule, ((result[0] - ref[0]) * 1000, (result[1] - ref[1]) * 1000)))

    records = []
    for (radius, ri, rs), pairs in sorted(grouped.items()):
        for orbital in ("HOMO", "LUMO"):
            records.append(summarize(pairs, radius, ri, rs, orbital))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    fields = list(records[0])
    with (args.output_dir / "aggregate.csv").open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    report = {
        "source_campaign": str(args.campaign.resolve()),
        "basis": manifest["basis"],
        "eps_filter": manifest["eps_filter"],
        "expected_calculations": len(manifest["calculations"]),
        "valid_reference_count": len(references),
        "analysis_population": len(references),
        "explicitly_excluded_molecules": sorted(EXCLUDED_MOLECULES),
        "invalid_references": invalid_references,
        "valid_pairs": sum(len(pairs) for pairs in grouped.values()),
        "missing_counts": dict(missing),
        "DFT_state_mismatches": mismatched,
        "aggregate_point_count": len(records),
        "coverage_min": min(record["n"] for record in records),
        "coverage_max": max(record["n"] for record in records),
        "reference_selection": selection,
        "reference_selection_path": str(args.reference_selection) if selection else None,
    }
    (args.output_dir / "provenance.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, separators=(",", ":")))


if __name__ == "__main__":
    main()
