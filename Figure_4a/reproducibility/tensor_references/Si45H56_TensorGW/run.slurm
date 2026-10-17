#!/bin/bash
#SBATCH --job-name=409_si45_t_eps10
#SBATCH --account=hpc-prf-coopfst
#SBATCH --partition=normal
#SBATCH --nodes=4
#SBATCH --ntasks=64
#SBATCH --ntasks-per-node=16
#SBATCH --cpus-per-task=8
#SBATCH --exclusive
#SBATCH --time=01:40:00
#SBATCH --output=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/409_si45h56_tensor_epsfilter_20261002/eps1e-10/slurm-%j.out
#SBATCH --error=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/409_si45h56_tensor_epsfilter_20261002/eps1e-10/slurm-%j.err
#SBATCH --chdir=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/409_si45h56_tensor_epsfilter_20261002/eps1e-10

set -euo pipefail
set +o history
unset HISTFILE
export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8
export OMP_STACKSIZE=256M OMP_MAX_ACTIVE_LEVELS=1
export OMP_PROC_BIND=true OMP_PLACES=cores
export TMPDIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/409_si45h56_tensor_epsfilter_20261002/eps1e-10/tmp TMP=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/409_si45h56_tensor_epsfilter_20261002/eps1e-10/tmp TEMP=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/409_si45h56_tensor_epsfilter_20261002/eps1e-10/tmp
export XDG_CACHE_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/409_si45h56_tensor_epsfilter_20261002/eps1e-10/cache
export XDG_CONFIG_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/409_si45h56_tensor_epsfilter_20261002/eps1e-10/config
export XDG_DATA_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/409_si45h56_tensor_epsfilter_20261002/eps1e-10/share
export XDG_STATE_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/409_si45h56_tensor_epsfilter_20261002/eps1e-10/state
export OMPI_MCA_orte_tmpdir_base=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/409_si45h56_tensor_epsfilter_20261002/eps1e-10/tmp
export PRTE_MCA_prte_tmpdir_base=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/409_si45h56_tensor_epsfilter_20261002/eps1e-10/tmp
export CP2K_DATA_DIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/096_Si45H56_grid_start_comparison/source/data
module purge
module load mpi/OpenMPI/5.0.7-GCC-14.2.0
export LD_RUN_PATH=${LD_RUN_PATH:-}
source /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/001_CP2K/cp2k/tools/toolchain/install/setup
set -u
mkdir -p "$TMPDIR" "$XDG_CACHE_HOME"
srun --cpu-bind=cores /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/096_Si45H56_grid_start_comparison/build/bin/cp2k.psmp -i /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/409_si45h56_tensor_epsfilter_20261002/eps1e-10/input.inp -o /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/409_si45h56_tensor_epsfilter_20261002/eps1e-10/output.log
