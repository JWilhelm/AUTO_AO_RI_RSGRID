#!/usr/bin/env python3
"""Verify every current Figure 6 calculation and recompute the manuscript points."""
from collections import defaultdict
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import statistics

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NOCTUA_ROOT = '/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/'
OTUS_PAYLOAD = '/scratch/hpc-prf-metdyn/eprop2d1_Jan/05_Benchmark_RI_opt/gw100_qzvp_fig6_otus_20261017/payload/'
NAMES = ('input.inp', 'output.log', 'bandstructure_SCF_and_G0W0')
MANIFEST = json.loads((HERE/'raw_file_manifest.json').read_text())
ASSETS = json.loads((HERE/'asset_manifest.json').read_text())
ABC = json.loads((HERE/'reference_pbe0_def2_tzvp_gwp36.json').read_text())['molecules']
DEF = json.loads((HERE/'reference_pbe_def2_qzvp_fhi2021si.json').read_text())['molecules']
assert len(MANIFEST) == 6912 and len(ABC) == 92 and len(DEF) == 100
assert len(ASSETS) == 297
for asset in ASSETS:
    data=(HERE/asset['path']).read_bytes()
    if len(data)!=asset['bytes'] or hashlib.sha256(data).hexdigest()!=asset['sha256']:
        raise ValueError(f"asset hash mismatch: {asset['path']}")

def asset_path(remote):
    if remote.startswith(OTUS_PAYLOAD):
        remote = NOCTUA_ROOT + remote[len(OTUS_PAYLOAD):]
    assert remote.startswith(NOCTUA_ROOT),remote
    return HERE/'assets'/remote[len(NOCTUA_ROOT):]

def orbitals(raw):
    found={}
    for line in raw.splitlines():
        match=re.match(r'^\s*(\d+) \((occ|vir)\)\s+1\s+(.*)$',line)
        if match:
            value=float(match[3].split()[-1])
            if not math.isfinite(value):raise ValueError('non-finite QP')
            found[int(match[1])]=(match[2],value)
    return found

by_point=defaultdict(list)
sha_checks=0
source_counts=defaultdict(int)
for record in MANIFEST:
    panel=record['panel'];ratio=record['ratio'];mol=record['molecule']
    d=ROOT/f'Figure_6{panel}'/'calculations'/f'rs{ratio:02d}'/mol
    for name in NAMES:
        b=(d/name).read_bytes()
        if hashlib.sha256(b).hexdigest()!=record['sha256'][name]:
            raise ValueError(f'hash mismatch: {d/name}')
        sha_checks+=1
    inp=(d/'input.inp').read_text(errors='replace')
    out=(d/'output.log').read_text(errors='replace')
    band=(d/'bandstructure_SCF_and_G0W0').read_text(errors='replace')
    if 'PROGRAM ENDED AT' not in out or re.search(r'CP2K aborted|SIGSEGV|SIGABRT|MPI_ABORT',out,re.I):
        raise ValueError(f'abnormal CP2K output: {d}')
    if not re.search(r'Density guess:\s+RESTART',out):raise ValueError(f'SCF WFN not read: {d}')
    vals=re.findall(r'Normalized 3C error:\s+(\S+)',out)
    evals=re.findall(r'RI-RS grid evaluations completed:\s+(\d+)',out)
    if not vals or not evals or not math.isfinite(float(vals[-1])) or int(evals[-1])<1:
        raise ValueError(f'missing fit/evaluation: {d}')
    for key in ('WFN_RESTART_FILE_NAME','BASIS_SET_FILE_NAME','POTENTIAL_FILE_NAME','COORD_FILE_NAME'):
        for path in re.findall(r'(?m)^\s*'+key+r'\s+(\S+)',inp):
            if not asset_path(path).is_file():raise ValueError(f'missing {key}: {path}')
    table=orbitals(band)
    ref=(ABC if panel in 'abc' else DEF)[mol]
    hi=ref['homo_index'];li=ref['lumo_index']
    if hi not in table or li not in table or table[hi][0]!='occ' or table[li][0]!='vir':
        raise ValueError(f'orbital mismatch: {d}, indices {hi}/{li}')
    h=(table[hi][1]-ref['homo_eV'])*1000
    l=(table[li][1]-ref['lumo_eV'])*1000
    by_point[(panel,ratio)].append({'molecule':mol,'homo_error_meV':h,'lumo_error_meV':l,
                                    'homo_in_mae':panel in 'abc' or not ref['homo_excluded'],
                                    'fit_error':float(vals[-1]),'evaluations':int(evals[-1])})
    source_counts[record['source']]+=1

for panel in 'abcdef':
    for ratio in range(2,14):
        rows=by_point[(panel,ratio)]
        expected=92 if panel in 'abc' else 100
        if len(rows)!=expected or len({r['molecule'] for r in rows})!=expected:
            raise ValueError(f'incomplete/duplicate point {panel}/{ratio}: {len(rows)}')

points={}
for panel in 'abcdef':
    for ratio in range(2,14):
        rows=by_point[(panel,ratio)]
        h=[abs(r['homo_error_meV']) for r in rows if r['homo_in_mae']]
        l=[abs(r['lumo_error_meV']) for r in rows]
        points[(panel,ratio)]=(statistics.mean(h),statistics.median(h),statistics.mean(l),statistics.median(l))

tex=(HERE/'figure6_source_snapshot.tex').read_text()
chunks=tex.split('\\nextgroupplot')[1:]
assert len(chunks)==6
compared=0
for panel,chunk in zip('abcdef',chunks):
    lines=re.findall(r'\\addplot\[[^\]]+\] coordinates \{([^}]+)\};',chunk)
    if len(lines)!=4:raise ValueError(f'expected four curves in Figure 6{panel}')
    for curve,line in enumerate(lines):
        coords=[(int(x),float(y)) for x,y in re.findall(r'\((\d+),([-+\d.]+)\)',line)]
        if [x for x,y in coords]!=list(range(2,14)):
            raise ValueError(f'grid size mismatch in Figure 6{panel}')
        for ratio,value in coords:
            actual=points[(panel,ratio)][curve]
            if abs(actual-value)>0.000001:
                raise ValueError(f'Figure 6{panel}, grid {ratio}, curve {curve}: raw {actual:.9f}, TeX {value:.9f}')
            compared+=1

with (HERE/'aggregate.csv').open('w',newline='') as f:
    writer=csv.writer(f,lineterminator='\n')
    writer.writerow(['panel','radius_A','ratio','homo_count','lumo_count','homo_mae_meV','homo_median_meV','lumo_mae_meV','lumo_median_meV'])
    for panel in 'abcdef':
        for ratio in range(2,14):
            vals=points[(panel,ratio)]
            writer.writerow([panel,{'a':0.5,'b':3,'c':5,'d':0.5,'e':3,'f':5}[panel],ratio,
                             92 if panel in 'abc' else 95,92 if panel in 'abc' else 100,*[f'{v:.6f}' for v in vals]])
with (HERE/'molecule_errors.csv').open('w',newline='') as f:
    writer=csv.writer(f,lineterminator='\n')
    writer.writerow(['panel','ratio','molecule','homo_error_meV','lumo_error_meV','homo_in_mae','normalized_3c_error','grid_evaluations'])
    for key in sorted(by_point):
        for row in sorted(by_point[key],key=lambda r:r['molecule']):
            writer.writerow([key[0],key[1],row['molecule'],f"{row['homo_error_meV']:.6f}",
                             f"{row['lumo_error_meV']:.6f}",int(row['homo_in_mae']),
                             f"{row['fit_error']:.9g}",row['evaluations']])
print(f'{len(MANIFEST)} calculations, {sha_checks} raw SHA-256 checks, {len(ASSETS)} asset hashes, {compared} matching manuscript coordinates')
print('Accepted source counts:',dict(source_counts))
