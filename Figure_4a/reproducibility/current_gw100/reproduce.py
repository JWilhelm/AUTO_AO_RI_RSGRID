#!/usr/bin/env python3
"""Verify current Figure 4(a--f) from CP2K inputs and outputs."""
import csv
import hashlib
import pathlib
import re
from collections import defaultdict

BASE=pathlib.Path(__file__).resolve().parent
DATA=BASE
REPO=BASE.parents[2]
ROW=re.compile(r'^\s*\d+\s+\((occ|vir|unocc)\)\s+\d+\s+.*?(-?\d+\.\d+)\s*$')
COORD=re.compile(r'\((\d+),([\d.]+)\)')

def orbitals(path):
    occupied=[]; virtual=[]
    for line in path.read_text().splitlines():
        m=ROW.match(line)
        if m: (occupied if m[1]=='occ' else virtual).append(float(m[2]))
    if not occupied or not virtual: raise ValueError(path)
    return max(occupied),min(virtual)

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    with (DATA/'molecule_errors.csv').open() as f: rows=list(csv.DictReader(f))
    with (DATA/'aggregate.csv').open() as f: aggregate=list(csv.DictReader(f))
    with (DATA/'missing.csv').open() as f: missing=list(csv.DictReader(f))
    with (DATA/'references.csv').open() as f: references=list(csv.DictReader(f))
    with (DATA/'plot_coordinates.csv').open() as f: plot=list(csv.DictReader(f))
    assert len(rows)==10800, len(rows)
    assert len(missing)==0, len(missing)
    assert len(references)==100 and len(plot)==216
    issues=[]; sums=defaultdict(list)
    for r in references:
        source=REPO/r['source']
        if not source.is_file() or sha(source)!=r['sha256']:
            issues.append(('reference',r['molecule'],source))
    for i,r in enumerate(rows):
        src=(REPO/r['output']).parent
        inp,out,orb=(src/name for name in ('input.inp','output.log','bandstructure_SCF_and_G0W0'))
        if not (inp.is_file() and out.is_file() and orb.is_file()): issues.append((i,'missing raw',src)); continue
        if sha(inp)!=r['input_sha256'] or sha(out)!=r['output_sha256']:
            issues.append((i,'sha256 mismatch',src));continue
        output=out.read_text()
        if 'PROGRAM ENDED AT' not in output: issues.append((i,'CP2K end absent',src))
        if not re.search(r'EPS_FILTER\s+1(?:\.0)?E-12',inp.read_text(),re.I):
            issues.append((i,'filter differs',src))
        h,l=orbitals(orb)
        if abs(h-float(r['homo']))>1e-5 or abs(l-float(r['lumo']))>1e-5:
            issues.append((i,'frontier mismatch',src,h,l))
        for name,val in [('homo',h),('lumo',l)]:
            err=(val-float(r['ref_'+name]))*1000
            if abs(err-float(r[name+'_error_meV']))>1e-5:
                issues.append((i,'error mismatch',src,name,err))
            sums[(r['panel'],r['ri'],r['rs'],name)].append(abs(err))
    for r in aggregate:
        source_panel={'a':'a','b':'a','c':'c','d':'c','e':'e','f':'e'}[r['panel']]
        k=(source_panel,r['ri'],r['rs'],r['orbital'])
        values=sums[k]
        if len(values)!=int(r['n']) or abs(sum(values)/len(values)-float(r['mae_meV']))>1e-5:
            issues.append(('aggregate',k,len(values),r['n']))
    for r in plot:
        panel=r['panel'];ri=r['ri'];rs=r['rs'];y=float(r['plotted_meV'])
        source_panel={'a':'a','b':'a','c':'c','d':'c','e':'e','f':'e'}[panel]
        orbital='homo' if panel in 'ace' else 'lumo'
        v=sums[(source_panel,ri,rs,orbital)]
        mean=sum(v)/len(v)
        if abs(y-mean)>1e-5:issues.append(('plot',panel,ri,rs,y,mean))
    print(f'Figure 4 GW100: {len(rows)} raw records, {len(aggregate)} aggregates, {len(missing)} documented gaps, {len(issues)} discrepancies')
    for issue in issues[:30]: print(issue)
    if issues: raise SystemExit(1)

if __name__=='__main__':main()
