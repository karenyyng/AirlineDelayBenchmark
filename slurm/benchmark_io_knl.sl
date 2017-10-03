#!/bin/bash -l

#SBATCH -N 1         	    # Use 1 nodes
#SBATCH -p regular
#SBATCH -t 01:00:00  	    
#SBATCH -C knl,quad,flat    # Use KNL nodes in quad flat format (usually faster)
#SBATCH --account=dasrepo
#SBATCH -J airlineIO
#SBATCH -o /project/projectdirs/dasrepo/ml_benchmarks/AirlineDelayBenchmark/slurm_logs/%j_haswell.log
#SBATCH -e /project/projectdirs/dasrepo/ml_benchmarks/AirlineDelayBenchmark/slurm_logs/%j_haswell.err
##### SBATCH --license=SCRATCH   # note: specify license need for the file systems your job needs, such as SCRATCH,project

##### modified script according to 
##### https://www.nersc.gov/users/computational-systems/cori/running-jobs/example-batch-scripts-for-knl/

export HOSTNAME=cori
export ARK=knl
source ../config/load_py3_2018.0.0.sh
echo $OMP_NUM_THREADS
srun -N 1 -n $OMP_NUM_THREADS python ../src/experiments/mpi_sklearn_pipeline.py 
# srun -N 1 python ../src/experiments/dask_pipeline.py --n_workers \ 
# $OMP_NUM_THREADS --n_files $OMP_NUM_THREADS --n_threads 1 --output_json 1

