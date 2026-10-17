#!/usr/bin/env python3
"""Verify 216 cluster calculations and all 432 Figure 5(g--r) data points."""
import csv
import hashlib
import pathlib
import re

DATA = pathlib.Path(__file__).resolve().parent
REPO = DATA.parents[2]
ROW = re.compile(r"^\s*\d+\s+\((occ|vir|unocc)\)\s+\d+\s+.*?(-?\d+\.\d+)\s*$")


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def orbitals(path):
    occ,vir=[],[]
    for line in path.read_text().splitlines():
        m=ROW.match(line)
        if m:(occ if m[1]=='occ' else vir).append(float(m[2]))
    if not occ or not vir:raise ValueError(f"Incomplete orbital table: {path}")
    return max(occ),min(vir)


def main():
    with (DATA/'points.csv').open() as f:rows=list(csv.DictReader(f))
    assert len(rows)==216,len(rows)
    seen=set()
    for r in rows:
        key=(r['system'],r['radius_A'],r['ri_ao'],r['rs_ao'])
        assert key not in seen,key
        seen.add(key)
        d=REPO/r['calculation']
        for file,column in [('input.inp','input_sha256'),('output.log','output_sha256'),('bandstructure_SCF_and_G0W0','orbitals_sha256')]:
            assert sha(d/file)==r[column],(key,file)
        assert 'PROGRAM ENDED AT' in (d/'output.log').read_text(),key
        inp=(d/'input.inp').read_text()
        eps=re.search(r'EPS_FILTER\s+([\d.Ee+-]+)',inp)
        tik=re.search(r'TIKHONOV\s+([\d.Ee+-]+)',inp)
        assert eps and tik and eps[1]==r['eps_filter'] and tik[1]==r['tikhonov'],key
        h,l=orbitals(d/'bandstructure_SCF_and_G0W0')
        assert abs(h-float(r['qp_homo_ev']))<1e-6 and abs(l-float(r['qp_lumo_ev']))<1e-6,key
        ref=REPO/f"Figure_5{r['homo_panel']}/TensorGW_reference/bandstructure_SCF_and_G0W0"
        rh,rl=orbitals(ref)
        assert abs(rh-float(r['ref_homo_ev']))<1e-6 and abs(rl-float(r['ref_lumo_ev']))<1e-6,key
        assert abs(max(1,round(abs(h-rh)*1000,6))-float(r['plotted_homo_meV']))<1e-5,key
        assert abs(max(1,round(abs(l-rl)*1000,6))-float(r['plotted_lumo_meV']))<1e-5,key
        counterpart=REPO/f"Figure_5{r['lumo_panel']}/calculations/ri{r['ri_ao']}_rs{int(r['rs_ao']):02d}"
        assert sha(counterpart/'output.log')==r['output_sha256'],key
    print('Figure 5(g--r): 216 calculations, 432 plotted values, all inputs/outputs/references verified.')


if __name__=='__main__':main()
