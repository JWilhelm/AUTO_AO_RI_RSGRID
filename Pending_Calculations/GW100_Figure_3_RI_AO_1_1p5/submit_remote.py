from pathlib import Path
import json,subprocess,hashlib,time
from datetime import datetime,timezone
ROOT=Path('/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt').resolve(strict=True)
D=ROOT/'419_gw100_fig3_riao1_1p5_20261002'
m=json.loads((D/'manifest.json').read_text());assert len(m['tasks'])==200
state=D/'submissions.json';assert state.resolve().is_relative_to(ROOT)
s=json.loads(state.read_text()) if state.exists() else {'jobs':{},'errors':{}}
for t in m['tasks']:
 if t['run'] in s['jobs']:continue
 path=Path(t['run']);assert path.resolve().is_relative_to(ROOT)
 assert hashlib.sha256((path/'input.inp').read_bytes()).hexdigest()==t['input_sha256']
 script=Path(t['script']).read_text()
 assert '--account=hpc-prf-coopfst' in script and '--array' not in script and '--dependency' not in script
 r=subprocess.run(['sbatch','--parsable',t['script']],capture_output=True,text=True)
 if r.returncode:
  s['errors'][t['run']]=r.stderr
 else:
  jid=r.stdout.strip().split(';')[0];assert jid.isdigit(),r.stdout
  s['jobs'][t['run']]={'job_id':int(jid),'molecule':t['molecule'],'ri_ao_ratio':t['ri_ao_ratio'],'name':t['job_name'],'submitted_at':datetime.now(timezone.utc).isoformat()};s['errors'].pop(t['run'],None)
 tmp=D/'submissions.tmp';assert tmp.resolve().is_relative_to(ROOT);tmp.write_text(json.dumps(s,indent=2)+'\n');tmp.replace(state)
print('SUBMITTED',len(s['jobs']),'ERRORS',len(s['errors']))
print('JOB_ID_RANGE',min(x['job_id'] for x in s['jobs'].values()),max(x['job_id'] for x in s['jobs'].values()))
if s['errors']:print('ERROR_DETAILS',s['errors'])
