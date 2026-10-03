#!/bin/bash
#SBATCH --job-name=421_t5_ri4_rs07
#SBATCH --account=hpc-prf-coopfst
#SBATCH --partition=normal
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --ntasks-per-node=16
#SBATCH --cpus-per-task=8
#SBATCH --distribution=block:block
#SBATCH --exclusive
#SBATCH --no-requeue
#SBATCH --mem=0
#SBATCH --time=00:25:00
#SBATCH --chdir=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/421_h24p64_rc0p5_rs07_tikh1e5_20261003/ri4_rs07
#SBATCH --output=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/421_h24p64_rc0p5_rs07_tikh1e5_20261003/ri4_rs07/slurm-%j.out
#SBATCH --error=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/421_h24p64_rc0p5_rs07_tikh1e5_20261003/ri4_rs07/slurm-%j.err
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
export CP2K_DATA_DIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/148_Figure4_augDZVP_T2_metdyn/source/data
export TMPDIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/421_h24p64_rc0p5_rs07_tikh1e5_20261003/ri4_rs07/tmp
export TMP=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/421_h24p64_rc0p5_rs07_tikh1e5_20261003/ri4_rs07/tmp
export TEMP=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/421_h24p64_rc0p5_rs07_tikh1e5_20261003/ri4_rs07/tmp
export XDG_CACHE_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/421_h24p64_rc0p5_rs07_tikh1e5_20261003/ri4_rs07/cache
export XDG_CONFIG_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/421_h24p64_rc0p5_rs07_tikh1e5_20261003/ri4_rs07/config
export XDG_DATA_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/421_h24p64_rc0p5_rs07_tikh1e5_20261003/ri4_rs07/share
export XDG_STATE_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/421_h24p64_rc0p5_rs07_tikh1e5_20261003/ri4_rs07/state
export OMPI_MCA_orte_tmpdir_base=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/421_h24p64_rc0p5_rs07_tikh1e5_20261003/ri4_rs07/tmp
export PRTE_MCA_prte_tmpdir_base=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/421_h24p64_rc0p5_rs07_tikh1e5_20261003/ri4_rs07/tmp
test "$SLURM_JOB_NUM_NODES:$SLURM_NTASKS:$OMP_NUM_THREADS" = "1:16:8"
srun --ntasks=16 --ntasks-per-node=16 --cpus-per-task=8 --cpu-bind=cores --distribution=block:block /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/148_Figure4_augDZVP_T2_metdyn/build/bin/cp2k.psmp -i /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/421_h24p64_rc0p5_rs07_tikh1e5_20261003/ri4_rs07/input.inp -o /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/421_h24p64_rc0p5_rs07_tikh1e5_20261003/ri4_rs07/output.log </dev/null
