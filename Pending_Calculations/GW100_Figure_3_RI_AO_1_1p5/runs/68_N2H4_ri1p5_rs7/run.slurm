#!/bin/bash
#SBATCH --job-name=419__68_N2H4_ri1p5_rs7
#SBATCH --account=hpc-prf-coopfst
#SBATCH --partition=normal
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=16
#SBATCH --exclusive
#SBATCH --no-requeue
#SBATCH --time=00:20:00
#SBATCH --chdir=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7
#SBATCH --output=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7/slurm-%j.out
#SBATCH --error=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7/slurm-%j.err
set -euo pipefail
unset HISTFILE
set +o history
ulimit -c 0
module purge
module load mpi/OpenMPI/5.0.7-GCC-14.2.0
source /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/001_CP2K/cp2k/tools/toolchain/install/setup
export OMP_NUM_THREADS=16
export OPENBLAS_NUM_THREADS=1 OMP_STACKSIZE=128M OMP_MAX_ACTIVE_LEVELS=1
export OMP_PLACES=cores OMP_PROC_BIND=close
export CP2K_DATA_DIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/096_Si45H56_grid_start_comparison/source/data
export TMPDIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7/tmp TMP=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7/tmp TEMP=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7/tmp
export XDG_CACHE_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7/cache XDG_CONFIG_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7/config XDG_STATE_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7/state XDG_DATA_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7/share
export OMPI_MCA_orte_tmpdir_base=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7/tmp PRTE_MCA_prte_tmpdir_base=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7/tmp
export OMPI_MCA_btl_sm_backing_directory=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7/tmp OMPI_MCA_shmem_mmap_backing_file_base_dir=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7/tmp
cd /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7
mpiexec --bind-to core --map-by ppr:4:node:PE=16 -np 4 /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/096_Si45H56_grid_start_comparison/build-auto-ri-diagnostic/bin/cp2k.psmp -i /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7/input.inp -o /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/419_gw100_fig3_riao1_1p5_20261002/runs/68_N2H4_ri1p5_rs7/output.log </dev/null
