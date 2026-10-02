#!/bin/bash
#SBATCH --job-name=415_c5_a2_r03
#SBATCH --account=hpc-prf-coopfst
#SBATCH --partition=normal
#SBATCH --nodes=1
#SBATCH --ntasks=31
#SBATCH --ntasks-per-node=31
#SBATCH --cpus-per-task=4
#SBATCH --exclusive
#SBATCH --no-requeue
#SBATCH --mem=240000
#SBATCH --time=01:30:00
#SBATCH --chdir=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/415_figure3gl_si45_original_build_eps1e10_20261002/c5_a2_r03
#SBATCH --output=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/415_figure3gl_si45_original_build_eps1e10_20261002/c5_a2_r03/slurm-%j.out
#SBATCH --error=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/415_figure3gl_si45_original_build_eps1e10_20261002/c5_a2_r03/slurm-%j.err
set -euo pipefail
unset HISTFILE
set +o history
ulimit -c 0
module purge
module load mpi/OpenMPI/5.0.7-GCC-14.2.0
source /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/001_CP2K/cp2k/tools/toolchain/install/setup
export OMP_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=1
export OMP_STACKSIZE=128M
export OMP_MAX_ACTIVE_LEVELS=1
export OMP_PLACES=cores
export OMP_PROC_BIND=close
export CP2K_DATA_DIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/096_Si45H56_grid_start_comparison/source/data
export TMPDIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/415_figure3gl_si45_original_build_eps1e10_20261002/c5_a2_r03/tmp
export TMP=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/415_figure3gl_si45_original_build_eps1e10_20261002/c5_a2_r03/tmp
export TEMP=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/415_figure3gl_si45_original_build_eps1e10_20261002/c5_a2_r03/tmp
export XDG_CACHE_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/415_figure3gl_si45_original_build_eps1e10_20261002/c5_a2_r03/cache
export XDG_CONFIG_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/415_figure3gl_si45_original_build_eps1e10_20261002/c5_a2_r03/config
export XDG_DATA_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/415_figure3gl_si45_original_build_eps1e10_20261002/c5_a2_r03/share
export XDG_STATE_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/415_figure3gl_si45_original_build_eps1e10_20261002/c5_a2_r03/state
export OMPI_MCA_orte_tmpdir_base=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/415_figure3gl_si45_original_build_eps1e10_20261002/c5_a2_r03/tmp
export PRTE_MCA_prte_tmpdir_base=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/415_figure3gl_si45_original_build_eps1e10_20261002/c5_a2_r03/tmp
export OMPI_MCA_btl_sm_backing_directory=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/415_figure3gl_si45_original_build_eps1e10_20261002/c5_a2_r03/tmp
export OMPI_MCA_shmem_mmap_backing_file_base_dir=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/415_figure3gl_si45_original_build_eps1e10_20261002/c5_a2_r03/tmp
cd /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/415_figure3gl_si45_original_build_eps1e10_20261002/c5_a2_r03
mpiexec --bind-to core --map-by ppr:31:node:PE=4 -np 31 /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/096_Si45H56_grid_start_comparison/build/bin/cp2k.psmp -i input.inp -o output.log </dev/null
