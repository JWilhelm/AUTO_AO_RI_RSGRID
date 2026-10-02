#!/bin/bash
#SBATCH --job-name=404_base_e12
#SBATCH --account=hpc-prf-coopfst
#SBATCH --partition=normal
#SBATCH --nodes=4
#SBATCH --ntasks=64
#SBATCH --ntasks-per-node=16
#SBATCH --cpus-per-task=8
#SBATCH --distribution=block:block
#SBATCH --exclusive
#SBATCH --no-requeue
#SBATCH --mem=0
#SBATCH --time=01:40:00
#SBATCH --chdir=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/404_h60_reference_20261001/base_e12
#SBATCH --output=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/404_h60_reference_20261001/base_e12/slurm-%j.out
#SBATCH --error=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/404_h60_reference_20261001/base_e12/slurm-%j.err

set -euo pipefail
unset HISTFILE
set +o history
ulimit -c 0

module purge
module load mpi/OpenMPI/5.0.7-GCC-14.2.0
export LD_RUN_PATH=${LD_RUN_PATH:-}
source /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/001_CP2K/cp2k/tools/toolchain/install/setup

export OMP_NUM_THREADS=8
export OPENBLAS_NUM_THREADS=1
export OMP_DYNAMIC=FALSE
export OMP_STACKSIZE=512M
export OMP_MAX_ACTIVE_LEVELS=1
export OMP_PROC_BIND=spread
export OMP_PLACES=cores
export CP2K_DATA_DIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/130_maximin_rank_tests_coopfst/source/data

run_dir=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/404_h60_reference_20261001/base_e12
export TMPDIR="$run_dir/tmp"
export TMP="$run_dir/tmp"
export TEMP="$run_dir/tmp"
export XDG_CACHE_HOME="$run_dir/cache"
export XDG_CONFIG_HOME="$run_dir/config"
export XDG_DATA_HOME="$run_dir/share"
export XDG_STATE_HOME="$run_dir/state"
export OMPI_MCA_orte_tmpdir_base="$run_dir/tmp"
export PRTE_MCA_prte_tmpdir_base="$run_dir/tmp"

test "$SLURM_JOB_NUM_NODES:$SLURM_NTASKS:$OMP_NUM_THREADS" = "4:64:8"

srun --ntasks=64 --ntasks-per-node=16 --cpus-per-task=8 --cpu-bind=cores --distribution=block:block \
  /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/130_maximin_rank_tests_coopfst/build/bin/cp2k.psmp \
  -i "$run_dir/input.inp" -o "$run_dir/output.log" </dev/null
