#!/bin/bash
#SBATCH --job-name=408_p4x4_t_eps10
#SBATCH --account=hpc-prf-coopfst
#SBATCH --partition=normal
#SBATCH --nodes=4
#SBATCH --ntasks=128
#SBATCH --ntasks-per-node=32
#SBATCH --cpus-per-task=4
#SBATCH --distribution=block:block
#SBATCH --exclusive
#SBATCH --no-requeue
#SBATCH --mem=0
#SBATCH --time=01:40:00
#SBATCH --chdir=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/408_h24p64_tensor_epsfilter_20261002/eps1e-10
#SBATCH --output=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/408_h24p64_tensor_epsfilter_20261002/eps1e-10/slurm-%j.out
#SBATCH --error=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/408_h24p64_tensor_epsfilter_20261002/eps1e-10/slurm-%j.err
set -euo pipefail
unset HISTFILE
set +o history
ulimit -c 0
module purge
module load mpi/OpenMPI/5.0.7-GCC-14.2.0
export LD_RUN_PATH=${LD_RUN_PATH:-}
source /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/001_CP2K/cp2k/tools/toolchain/install/setup
export OMP_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=1
export OMP_DYNAMIC=FALSE
export OMP_STACKSIZE=512M
export OMP_MAX_ACTIVE_LEVELS=1
export OMP_PROC_BIND=spread
export OMP_PLACES=cores
export CP2K_DATA_DIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/130_maximin_rank_tests_coopfst/source/data
export TMPDIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/408_h24p64_tensor_epsfilter_20261002/eps1e-10/tmp
export TMP=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/408_h24p64_tensor_epsfilter_20261002/eps1e-10/tmp
export TEMP=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/408_h24p64_tensor_epsfilter_20261002/eps1e-10/tmp
export XDG_CACHE_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/408_h24p64_tensor_epsfilter_20261002/eps1e-10/cache
export XDG_CONFIG_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/408_h24p64_tensor_epsfilter_20261002/eps1e-10/config
export XDG_DATA_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/408_h24p64_tensor_epsfilter_20261002/eps1e-10/share
export XDG_STATE_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/408_h24p64_tensor_epsfilter_20261002/eps1e-10/state
export OMPI_MCA_orte_tmpdir_base=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/408_h24p64_tensor_epsfilter_20261002/eps1e-10/tmp
export PRTE_MCA_prte_tmpdir_base=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/408_h24p64_tensor_epsfilter_20261002/eps1e-10/tmp
test "$SLURM_JOB_NUM_NODES:$SLURM_NTASKS:$OMP_NUM_THREADS" = "4:128:4"
srun --ntasks=128 --ntasks-per-node=32 --cpus-per-task=4 --cpu-bind=cores --distribution=block:block /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/130_maximin_rank_tests_coopfst/build/bin/cp2k.psmp -i /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/408_h24p64_tensor_epsfilter_20261002/eps1e-10/input.inp -o /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/408_h24p64_tensor_epsfilter_20261002/eps1e-10/output.log </dev/null
