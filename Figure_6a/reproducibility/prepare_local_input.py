#!/usr/bin/env python3
"""Write a local copy of one archived input with its asset paths relocated."""
import argparse
import re
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
NOCTUA='/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/'
OTUS='/scratch/hpc-prf-metdyn/eprop2d1_Jan/05_Benchmark_RI_opt/gw100_qzvp_fig6_otus_20261017/payload/'

parser=argparse.ArgumentParser()
parser.add_argument('panel',choices=list('abcdef'))
parser.add_argument('ratio',type=int,choices=range(2,14),metavar='2..13')
parser.add_argument('molecule')
parser.add_argument('output',type=Path)
args=parser.parse_args()
source=ROOT/f'Figure_6{args.panel}'/'calculations'/f'rs{args.ratio:02d}'/args.molecule/'input.inp'
text=source.read_text()
keys=('WFN_RESTART_FILE_NAME','COORD_FILE_NAME','BASIS_SET_FILE_NAME','POTENTIAL_FILE_NAME')
pattern=re.compile(r'(?m)^(\s*(?:'+ '|'.join(keys)+r')\s+)(\S+)')
def replace(match):
    path=match[2]
    if path.startswith(OTUS):path=NOCTUA+path[len(OTUS):]
    if not path.startswith(NOCTUA):raise ValueError(f'Unexpected source path: {path}')
    target=HERE/'assets'/path[len(NOCTUA):]
    if not target.is_file():raise FileNotFoundError(target)
    return match[1]+str(target.resolve())
localized=pattern.sub(replace,text)
if localized==text:raise ValueError('No external input paths were relocated')
args.output.write_text(localized)
print(args.output)
