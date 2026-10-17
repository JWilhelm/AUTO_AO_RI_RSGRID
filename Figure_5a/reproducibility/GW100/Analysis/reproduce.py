#!/usr/bin/env python3
import csv, hashlib, json, math
from collections import defaultdict
from pathlib import Path
from result_parser import read_result, summarize
root = Path(__file__).resolve().parents[1]
for name, expected in json.loads((root / "SHA256SUMS.json").read_text()).items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, name
items = json.loads((root / "Provenance/calculations.json").read_text())
refs = {}
for item in items:
    if item["kind"] != "TensorGW":
        continue
    value, problem = read_result(root / item["archive_run"] / "output.log")
    assert problem is None, (item["molecule"], problem)
    assert value[1] > value[0]
    refs[item["molecule"]] = value
assert len(refs) == 100, len(refs)
groups = defaultdict(list)
for item in items:
    if item["kind"] != "RI_RS":
        continue
    value, problem = read_result(root / item["archive_run"] / "output.log")
    assert problem is None, (item["molecule"], problem)
    ref = refs[item["molecule"]]
    assert abs(value[2] - ref[2]) <= 1e-7
    key = item["radius_A"], item["ri_ao_ratio"], item["rs_ao_ratio"]
    groups[key].append((item["molecule"], tuple((value[i] - ref[i])*1000 for i in (0,1))))
assert len(groups) == 108
computed = {}
for key, pairs in groups.items():
    assert len(pairs) == len(set(m for m,v in pairs)) == 100
    for orbital in ("HOMO", "LUMO"):
        computed[(*key, orbital)] = summarize(pairs, *key, orbital)
rows = list(csv.DictReader((root / "Analysis/aggregate.csv").open()))
assert len(rows) == 216
for row in rows:
    key = float(row["radius_A"]), int(row["ri_ao_ratio"]), int(row["rs_ao_ratio"]), row["orbital"]
    calc = computed[key]
    for field in ("n", "mae_meV", "p95_meV", "max_abs_meV"):
        assert math.isclose(float(row[field]), calc[field], abs_tol=1e-9), (key,field)
print("Verified raw checksums, 100 references, 10,800 pairs and 216 aggregate rows (100/100 each).")
