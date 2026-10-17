#!/usr/bin/env python3
"""Check all 50 current Figure 3 coordinates from archived CP2K outputs."""
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
from plot_figure_3 import collect,load_references

rows,validation=collect(ROOT,load_references(ROOT))
assert validation['all_reference_pairs_within_1e-6_hartree']
sources=(HERE/'compact_data_snapshot.tex').read_text()+'\n'+(HERE/'gw100_figure4_slice_snapshot.tex').read_text()
macros={name:[(float(x),float(y)) for x,y in re.findall(r'\(([-+\d.]+),([-+\d.]+)\)',body)]
        for name,body in re.findall(r'\\def\\(\w+)\{([^}]+)\}',sources)}
expected={
 ('GW100','auto_r3','homo'):'riBasisGwFigureFourHomo',
 ('GW100','auto_r3','lumo'):'riBasisGwFigureFourLumo',
 ('GW100','tabulated','homo'):'riBasisGwTabulatedHomo',
 ('GW100','tabulated','lumo'):'riBasisGwTabulatedLumo',
 ('Si45H56','auto_r0.5','homo'):'riBasisSiFortyFiveRcZeroFiveHomo',
 ('Si45H56','auto_r0.5','lumo'):'riBasisSiFortyFiveRcZeroFiveLumo',
 ('Si45H56','tabulated','homo'):'riBasisSiFortyFiveTabulatedHomo',
 ('Si45H56','tabulated','lumo'):'riBasisSiFortyFiveTabulatedLumo',
}
matched=0
for key,macro in expected.items():
    actual=sorted((float(r['x_ri_ao_ratio']),float(r['error_plotted_meV'])) for r in rows if
                  (r['system'],r['series'],r['orbital'])==key)
    target=sorted(macros[macro])
    if len(actual)!=len(target):raise ValueError(f'{macro} coverage: {len(actual)} != {len(target)}')
    for (ax,ay),(tx,ty) in zip(actual,target):
        if abs(ax-tx)>0.000001 or abs(ay-ty)>0.000001:
            raise ValueError(f'{macro}: raw ({ax},{ay}) != manuscript ({tx},{ty})')
        matched+=1
assert matched==50,matched
print(f'Figure 3: {matched} coordinates match raw CP2K outputs and manuscript source')
