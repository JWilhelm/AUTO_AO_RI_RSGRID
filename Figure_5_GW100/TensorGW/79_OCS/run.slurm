#!/bin/bash
#SBATCH --job-name=424_ref_79_OCS_reg6_m32
#SBATCH --account=hpc-prf-coopfst
#SBATCH --partition=normal
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --ntasks-per-node=32
#SBATCH --cpus-per-task=4
#SBATCH --exclusive
#SBATCH --mem=0
#SBATCH --no-requeue
#SBATCH --time=00:10:00
#SBATCH --chdir=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS
#SBATCH --output=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/slurm-%j.out
#SBATCH --error=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/slurm-%j.err
set -eo pipefail
unset HISTFILE
set +o history
ulimit -c 0
module purge
module load mpi/OpenMPI/5.0.7-GCC-14.2.0
source /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/001_CP2K/cp2k/tools/toolchain/install/setup
export LD_LIBRARY_PATH=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/ri_regularization_build:$LD_LIBRARY_PATH
ldd /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/148_Figure4_augDZVP_T2_metdyn/build/bin/cp2k.psmp > /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/linked_libraries.txt
grep -F "/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/ri_regularization_build/libcp2k.so.2026.2" /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/linked_libraries.txt
set -u
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=1 OMP_DYNAMIC=FALSE
export OMP_STACKSIZE=512M OMP_PROC_BIND=spread OMP_PLACES=cores
export GFORTRAN_UNBUFFERED_ALL=1
export TMPDIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/tmp TMP=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/tmp TEMP=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/tmp
export XDG_CACHE_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/cache XDG_CONFIG_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/config XDG_DATA_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/share XDG_STATE_HOME=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/state
export CP2K_DATA_DIR=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/148_Figure4_augDZVP_T2_metdyn/source/data
export OMPI_MCA_orte_tmpdir_base=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/tmp PRTE_MCA_prte_tmpdir_base=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/tmp
export OMPI_MCA_btl_sm_backing_directory=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/tmp OMPI_MCA_shmem_mmap_backing_file_base_dir=/scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/tmp
test "$SLURM_JOB_NUM_NODES:$SLURM_NTASKS:$OMP_NUM_THREADS" = '1:32:4'
srun --ntasks=32 --ntasks-per-node=32 --cpus-per-task=4 --cpu-bind=cores --distribution=block:block /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/148_Figure4_augDZVP_T2_metdyn/build/bin/cp2k.psmp -i /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/input.inp -o /scratch/hpc-prf-metdyn/eprop2d1_Jan/53_benchmark_RI_opt/424_gw100_tensor_diagnostics_eps15_20261003/validated_reference_sweep/reg6_m32/79_OCS/output.log </dev/null
