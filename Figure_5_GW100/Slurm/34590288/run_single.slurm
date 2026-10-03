#!/bin/bash
#SBATCH --job-name=418_96_uracil_rc5p0_ri2_rs06
#SBATCH --account=hpc-prf-coopfst
#SBATCH --partition=normal
#SBATCH --nodes=1
#SBATCH --ntasks=12
#SBATCH --ntasks-per-node=12
#SBATCH --cpus-per-task=9
#SBATCH --distribution=block:block
#SBATCH --exclusive
#SBATCH --no-requeue
#SBATCH --mem=0
#SBATCH --time=02:00:00
#SBATCH --chdir=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil
#SBATCH --output=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/slurm-%j.out
#SBATCH --error=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/slurm-%j.err
set -euo pipefail
unset HISTFILE
set +o history
ulimit -c 0
mkdir -p /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/tmp /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/cache /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/config /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/share /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/state
module purge
module load mpi/OpenMPI/5.0.7-GCC-14.2.0
source /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/001_CP2K/cp2k/tools/toolchain/install/setup
export OMP_NUM_THREADS=9 OPENBLAS_NUM_THREADS=1 OMP_DYNAMIC=FALSE
export OMP_STACKSIZE=512M OMP_PROC_BIND=spread OMP_PLACES=cores
export GFORTRAN_UNBUFFERED_ALL=1
export TMPDIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/tmp TMP=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/tmp TEMP=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/tmp
export XDG_CACHE_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/cache XDG_CONFIG_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/config XDG_DATA_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/share XDG_STATE_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/state
export CP2K_DATA_DIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/148_Figure4_augDZVP_T2_metdyn/source/data
export OMPI_MCA_orte_tmpdir_base=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/tmp PRTE_MCA_prte_tmpdir_base=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/tmp
export OMPI_MCA_btl_sm_backing_directory=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/tmp OMPI_MCA_shmem_mmap_backing_file_base_dir=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/tmp
test "$SLURM_JOB_NUM_NODES:$SLURM_NTASKS:$OMP_NUM_THREADS" = '1:12:9'
mpiexec --bind-to core --map-by ppr:12:node:PE=9 -np 12 /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/148_Figure4_augDZVP_T2_metdyn/build/bin/cp2k.psmp -i /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/input.inp -o /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc5p0/ri2_rs06/96_uracil/output.log </dev/null
