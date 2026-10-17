#!/bin/bash
#SBATCH --job-name=418_90_C6H5NH2_rc0p5_ri3_rs02
#SBATCH --account=hpc-prf-coopfst
#SBATCH --partition=normal
#SBATCH --nodes=1
#SBATCH --ntasks=14
#SBATCH --ntasks-per-node=14
#SBATCH --cpus-per-task=8
#SBATCH --distribution=block:block
#SBATCH --exclusive
#SBATCH --no-requeue
#SBATCH --mem=0
#SBATCH --time=02:00:00
#SBATCH --chdir=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2
#SBATCH --output=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/slurm-%j.out
#SBATCH --error=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/slurm-%j.err
set -euo pipefail
unset HISTFILE
set +o history
ulimit -c 0
mkdir -p /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/tmp /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/cache /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/config /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/share /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/state
module purge
module load mpi/OpenMPI/5.0.7-GCC-14.2.0
source /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/001_CP2K/cp2k/tools/toolchain/install/setup
export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=1 OMP_DYNAMIC=FALSE
export OMP_STACKSIZE=512M OMP_PROC_BIND=spread OMP_PLACES=cores
export GFORTRAN_UNBUFFERED_ALL=1
export TMPDIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/tmp TMP=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/tmp TEMP=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/tmp
export XDG_CACHE_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/cache XDG_CONFIG_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/config XDG_DATA_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/share XDG_STATE_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/state
export CP2K_DATA_DIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/148_Figure4_augDZVP_T2_metdyn/source/data
export OMPI_MCA_orte_tmpdir_base=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/tmp PRTE_MCA_prte_tmpdir_base=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/tmp
export OMPI_MCA_btl_sm_backing_directory=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/tmp OMPI_MCA_shmem_mmap_backing_file_base_dir=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/tmp
test "$SLURM_JOB_NUM_NODES:$SLURM_NTASKS:$OMP_NUM_THREADS" = '1:14:8'
mpiexec --bind-to core --map-by ppr:14:node:PE=8 -np 14 /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/148_Figure4_augDZVP_T2_metdyn/build/bin/cp2k.psmp -i /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/input.inp -o /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/418_gw100_fig5_full_epsfilter_1e12_20261002/calculations/rc0p5/ri3_rs02/90_C6H5NH2/output.log </dev/null
