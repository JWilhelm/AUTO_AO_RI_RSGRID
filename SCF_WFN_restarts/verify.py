#!/usr/bin/env python3
"""Check all archived small-system SCF restarts against original input links."""
import hashlib
import json
from pathlib import Path
import re

here=Path(__file__).resolve().parent
root=here.parent
rows=json.loads((here/'manifest.json').read_text())
assert len(rows)==320
for row in rows:
    p=here/row['path']
    data=p.read_bytes()
    if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
        raise ValueError(f'WFN hash mismatch: {p}')
    source=root/row['source_input']
    text=source.read_text(errors='replace')
    old='/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/'+row['path'].removeprefix('noctua/')
    if not re.search(r'(?m)^\s*WFN_RESTART_FILE_NAME\s+'+re.escape(old)+r'\s*$',text):
        raise ValueError(f'Input does not reference WFN: {source}')
print(f'{len(rows)} existing-panel small-system WFN restarts verified')
