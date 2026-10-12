#!/usr/bin/env python3
"""Verify current manuscript Figure 4(g--ad) against archived CP2K outputs."""
import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "Plot_Figure_4"))
from plot_figure_4 import calculate

rows = calculate(REPO)
values = {(r['panel'],int(r['ri_ao_ratio']),int(r['rs_ao_ratio'])):float(r['error_meV'])
          for r in rows if r['panel'] not in set('abcdef')}
with (HERE / 'plot_coordinates.csv').open() as f: plotted=list(csv.DictReader(f))
assert len(values)==len(plotted)==864,(len(values),len(plotted))
bad=[]
for r in plotted:
    key=(r['panel'],int(r['ri']),int(r['rs']))
    actual=values[key]
    if abs(actual-float(r['plotted_meV']))>1e-5:bad.append((key,actual,r['plotted_meV']))
print(f"Figure 4(g--ad): {len(values)} points from archived CP2K outputs; {len(bad)} discrepancies")
if bad:
    print(bad[:20]);raise SystemExit(1)
