#!/usr/bin/env python3
"""Recompute the current 32 Figure 1 and 64 Figure 2 coordinates from CP2K."""
import csv
import hashlib
import math
from pathlib import Path
import re
import statistics
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
from plot_figure_1 import FAMILIES,N4_ROW,checked_text,collect,last_float,reference_names

X=[1,2,3,4]
POS=[0.55,1.95,3.45,4.85]
fig1=(HERE/'figure1_source_snapshot.tex').read_text()
fig2=(HERE/'figure2_source_snapshot.tex').read_text()

def compact_edges(path):
    text=checked_text(path)
    return {
      'pbe_homo':last_float(r'(?:PBE|SCF) valence band maximum \(eV\):\s*([-+0-9.Ee]+)',text),
      'pbe_lumo':last_float(r'(?:PBE|SCF) conduction band minimum \(eV\):\s*([-+0-9.Ee]+)',text),
      'gw_homo':last_float(r'G0W0 valence band maximum \(eV\):\s*([-+0-9.Ee]+)',text),
      'gw_lumo':last_float(r'G0W0 conduction band minimum \(eV\):\s*([-+0-9.Ee]+)',text),
    }

def reference_edges(path):
    text=checked_text(path)
    block=text[text.rfind('G0W0 results'):]
    rows=[(m.group(2),float(m.group(3)),float(m.group(6))) for m in N4_ROW.finditer(block)]
    occ=[r for r in rows if r[0]=='occ'];vir=[r for r in rows if r[0]=='vir']
    if not occ or not vir:raise ValueError(f'no frontier reference: {path}')
    return {'pbe_homo':max(r[1] for r in occ),'pbe_lumo':min(r[1] for r in vir),
            'gw_homo':max(r[2] for r in occ),'gw_lumo':min(r[2] for r in vir)}

def values_from_figure1():
    rows=collect(ROOT)
    by={(r['panel'],r['variant'],r['basis']):float(r['value_ev']) for r in rows}
    chunks=fig1.split('\\nextgroupplot')[1:]
    if len(chunks)!=4:raise ValueError('Figure 1 panel count')
    compared=0
    for panel,chunk in zip('abcd',chunks):
        plots=re.findall(r'\\addplot\[[\s\S]*?\] coordinates \{([^}]+)\}',chunk)
        if len(plots)!=2:raise ValueError(f'Figure 1{panel} plot count')
        for variant,plot in zip(('initial','optimized'),plots):
            coords=[(int(x),float(y)) for x,y in re.findall(r'\((\d+),([-+\d.]+)\)',plot)]
            if [x for x,y in coords]!=X:raise ValueError(f'Figure 1{panel} x coordinates')
            for index,value in coords:
                actual=by[(panel,variant,FAMILIES[index-1])]
                if abs(actual-value)>0.000001:raise ValueError(f'Figure 1{panel}, {variant}, {index}: {actual} != {value}')
                compared+=1
    return compared

def values_from_figure2():
    names=reference_names(ROOT/'Figure_2a'/'Reference_aug-TZVP-t1')
    refs={name:reference_edges(ROOT/'Figure_2a'/'Reference_aug-TZVP-t1'/name/'output.log') for name in names}
    by={}
    for panel,prefix in [('a','pbe'),('b','gw')]:
        for variant in ('Initial','Optimized'):
            for basis in FAMILIES:
                values={name:compact_edges(ROOT/f'Figure_2{panel}'/f'{variant}_{basis}'/name/'output.log') for name in names}
                for side in ('homo','lumo'):
                    key=prefix+'_'+side
                    by[(panel,side,variant.lower(),basis)]=statistics.mean(abs(values[name][key]-refs[name][key]) for name in names)
    for panel,prefix in [('c','pbe'),('d','gw')]:
        for variant in ('Initial','Optimized'):
            for basis in FAMILIES:
                values=compact_edges(ROOT/f'Figure_2{panel}'/f'{variant}_{basis}'/'output.log')
                for side in ('homo','lumo'):
                    by[(panel,side,variant.lower(),basis)]=values[prefix+'_'+side]
    compared=0
    for panel in 'abcd':
        for side,label in [('homo','left'),('lumo','right')]:
            for variant in ('initial','optimized'):
                macro='ao'+label+variant+panel
                m=re.search(r'\\def\\'+macro+r'\{([^}]+)\}',fig2)
                if not m:raise ValueError(f'Figure 2 macro {macro} missing')
                coords=[(float(x),float(y)) for x,y in re.findall(r'\(([-+\d.]+),([-+\d.]+)\)',m[1])]
                if [x for x,y in coords]!=POS:raise ValueError(f'Figure 2{panel} x coordinates')
                for basis,(_,value) in zip(FAMILIES,coords):
                    actual=by[(panel,side,variant,basis)]
                    if abs(actual-value)>0.000001:raise ValueError(f'Figure 2{panel}, {side}, {variant}, {basis}: {actual} != {value}')
                    compared+=1
    return compared

one=values_from_figure1();two=values_from_figure2()
print(f'Figure 1: {one} matching gap coordinates; Figure 2: {two} matching HOMO/LUMO coordinates')
