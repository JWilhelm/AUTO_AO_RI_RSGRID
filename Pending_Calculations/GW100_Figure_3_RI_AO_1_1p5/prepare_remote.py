from pathlib import Path
import hashlib,json,math,re,subprocess,xml.etree.ElementTree as ET
ROOT=Path('/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt').resolve(strict=True)
DEST=ROOT/'419_gw100_fig3_riao1_1p5_20261002'
EXE=ROOT/'096_Si45H56_grid_start_comparison/build-auto-ri-diagnostic/bin/cp2k.psmp'
DATA=ROOT/'096_Si45H56_grid_start_comparison/source/data'
SETUP=ROOT/'001_CP2K/cp2k/tools/toolchain/install/setup'

def safe(p):
 p=Path(p).resolve(strict=False); assert p.is_relative_to(ROOT),p;return p

def mkdir(p):safe(p).mkdir(exist_ok=True,parents=True)
def write(p,s):
 p=safe(p)
 if p.exists():assert p.read_text()==s,p
 else:p.write_text(s)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def one(s,p,r):
 s,n=re.subn(p,r,s,flags=re.M);assert n==1,(p,n);return s

def normalize(s):
 # Only differences authorized for the same scientific series are ignored.
 s=re.sub(r'^\s*(PROJECT|WFN_RESTART_FILE_NAME|SCF_GUESS|RI_AO_RATIO|NEIGHBOR_RADIUS)\s+[^\n]*\n','',s,flags=re.M)
 s=re.sub(r'\s*&PRINT\s*&RESTART OFF\s*&END RESTART\s*&END PRINT','',s)
 return ' '.join(s.split())

def main():
 assert DEST.is_dir() and EXE.is_file()
 schema=DEST/'cp2k_input.xml'
 if not schema.exists():schema=DEST/'CP2K_INPUT.xml'
 tree=ET.parse(schema).getroot()
 sec=tree
 for name in ['FORCE_EVAL','PROPERTIES','BANDSTRUCTURE','GW','PRINT','RESTART']:
  sec=next(x for x in sec.findall('SECTION') if name in [n.text for n in x.findall('NAME')])
 print('Original executable schema supports GW/PRINT/RESTART')
 source=json.loads((DEST/'sources.json').read_text());assert len(source)==100
 tasks=[];warnings={};missing=[]
 for row in source:
  name=row['molecule'];origin=safe(row['source_input']);output=safe(row['source_output'])
  assert sha(origin)==row['input_sha256'],origin
  assert sha(output)==row['output_sha256'],output
  inp=origin.read_text();txt=output.read_text()
  assert inp==row['input'],name
  assert 'PROGRAM ENDED AT' in txt and 'SCF run converged' in txt
  assert not re.search(r'MPI_ABORT|SIGSEGV|\[ABORT\]|\[ASSERT\]|CPASSERT',txt)
  warnings[name]=[l for l in txt.splitlines() if 'WARNING' in l or 'number of warnings' in l]
  # Prefer the final restart produced by the exact source calculation.
  project=re.search(r'^\s*PROJECT\s+(\S+)',inp,re.M).group(1)
  candidates=[output.parent/(project+'-RESTART.wfn'),origin.parent/(project+'-RESTART.wfn')]
  oldwfn=re.search(r'^\s*WFN_RESTART_FILE_NAME\s+(\S+)',inp,re.M)
  if oldwfn:candidates.append(Path(oldwfn.group(1)))
  wfn=next((safe(p) for p in candidates if p.is_file() and p.stat().st_size>0),None)
  if wfn is None:missing.append(name);continue
  nat=row['natoms'];ranks=2**int(math.log2(min(nat,16)));threads=16 if ranks<=8 else 8
  # Same-molecule RI/AO=2 complete timing, with a 35% margin plus five minutes.
  minutes=max(10,5*math.ceil((row['source_elapsed_s']*1.35+300)/300))
  wall=f'{minutes//60:02d}:{minutes%60:02d}:00'
  for ratio,tag in [(1.,'1'),(1.5,'1p5')]:
   run=DEST/'runs'/f'{name}_ri{tag}_rs7';mkdir(run)
   for d in ['tmp','cache','config','state','share']:mkdir(run/d)
   newproj=f'f3_{name.lower()}_ri{tag}_rs7'
   s=one(inp,r'^(\s*PROJECT)\s+\S+\s*$',rf'\1 {newproj}')
   s=one(s,r'^(\s*RI_AO_RATIO)\s+\S+\s*$',rf'\1 {ratio:g}')
   s=re.sub(r'^\s*WFN_RESTART_FILE_NAME\s+[^\n]*\n','',s,flags=re.M)
   s=one(s,r'^([ \t]*&DFT)[ \t]*$',r'\1\n    WFN_RESTART_FILE_NAME '+str(wfn))
   s=one(s,r'^(\s*SCF_GUESS)\s+\S+\s*$',r'\1 RESTART')
   if 'NEIGHBOR_RADIUS' not in s:s=s.replace('        &END AUTO_RI','          NEIGHBOR_RADIUS [angstrom] 3.0\n        &END AUTO_RI')
   if '&RESTART OFF' not in s:s=s.replace('      &END GW','        &PRINT\n          &RESTART OFF\n          &END RESTART\n        &END PRINT\n      &END GW')
   assert normalize(s)==normalize(inp),name
   required=['aug-SZV-MOLOPT-GTH-tier-2','EPS_FILTER 1.0E-7','INITIAL_GRID CHOLESKY','CHOLESKY_MATRIX D_PRIME','CHOLESKY_CANDIDATE_DOMAIN FULL_ATOM','RADIAL_QUADRATURE GAPW_LOG','RS_AO_RATIO_INITIAL 30','L_ADDITIONAL 2','RS_AO_RATIO 7','MAX_ITER 300','LBFGS_HISTORY 7','LBFGS_FACTR 0.0','LBFGS_PGTOL 1.0E-9','CUTOFF_ATOMIC_CLUSTER [angstrom] 3.0','TIKHONOV 1.0E-4','HEDIN_SHIFT F','NUM_TIME_FREQ_POINTS 30','REGULARIZATION_MINIMAX 1.0E-6','CUTOFF_RADIUS_RI [angstrom] 7','&RESTART OFF','SCF_GUESS RESTART']
   assert all(x in s for x in required),(name,[x for x in required if x not in s])
   assert 'MEMORY_PER_PROC' not in s
   write(run/'input.inp',s)
   jobname=f'419__{name}_ri{tag}_rs7'
   script=f'''#!/bin/bash
#SBATCH --job-name={jobname}
#SBATCH --account=hpc-prf-coopfst
#SBATCH --partition=normal
#SBATCH --nodes=1
#SBATCH --ntasks={ranks}
#SBATCH --ntasks-per-node={ranks}
#SBATCH --cpus-per-task={threads}
#SBATCH --exclusive
#SBATCH --no-requeue
#SBATCH --time={wall}
#SBATCH --chdir={run}
#SBATCH --output={run}/slurm-%j.out
#SBATCH --error={run}/slurm-%j.err
set -euo pipefail
unset HISTFILE
set +o history
ulimit -c 0
module purge
module load mpi/OpenMPI/5.0.7-GCC-14.2.0
source {SETUP}
export OMP_NUM_THREADS={threads}
export OPENBLAS_NUM_THREADS=1 OMP_STACKSIZE=128M OMP_MAX_ACTIVE_LEVELS=1
export OMP_PLACES=cores OMP_PROC_BIND=close
export CP2K_DATA_DIR={DATA}
export TMPDIR={run}/tmp TMP={run}/tmp TEMP={run}/tmp
export XDG_CACHE_HOME={run}/cache XDG_CONFIG_HOME={run}/config XDG_STATE_HOME={run}/state XDG_DATA_HOME={run}/share
export OMPI_MCA_orte_tmpdir_base={run}/tmp PRTE_MCA_prte_tmpdir_base={run}/tmp
export OMPI_MCA_btl_sm_backing_directory={run}/tmp OMPI_MCA_shmem_mmap_backing_file_base_dir={run}/tmp
cd {run}
mpiexec --bind-to core --map-by ppr:{ranks}:node:PE={threads} -np {ranks} {EXE} -i {run}/input.inp -o {run}/output.log </dev/null
'''
   write(run/'run.slurm',script)
   tasks.append(dict(molecule=name,ri_ao_ratio=ratio,rs_ao_ratio=7,run=str(run),script=str(run/'run.slurm'),job_name=jobname,nodes=1,mpi_ranks=ranks,omp_threads=threads,walltime=wall,source_elapsed_s=row['source_elapsed_s'],source_input=str(origin),source_output=str(output),input_sha256=sha(run/'input.inp'),wfn=str(wfn),wfn_sha256=sha(wfn),source_scf_energy=re.findall(r'ENERGY\|\s+Total FORCE_EVAL .*?energy \[.*?\]\s+([-+\d.Ee]+)',txt)[-1]))
 assert not missing,('MISSING_WFN',missing)
 assert len(tasks)==200
 manifest=dict(campaign=str(DEST),account='hpc-prf-coopfst',cp2k=str(EXE),cp2k_sha256=sha(EXE),source_campaign='111_GW100_GTH_Lebedev_riao245_rc3',requested='Extend Figure 3(a,b) with RI/AO 1 and 1.5 using Figure 4(c,d) settings at RS/AO 7',tasks=tasks,source_warnings=warnings)
 write(DEST/'manifest.json',json.dumps(manifest,indent=2)+'\n')
 print('PREPARED',len(tasks),'independent jobs; exact source input/output hashes checked; all full inputs reviewed; all source WFN restarts available.')
 print('WALLTIMES',sorted(set(t['walltime'] for t in tasks)))
 print('CP2K_SHA256',manifest['cp2k_sha256'])
if __name__=='__main__':main()
