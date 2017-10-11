#!/bin/bash -l

#SBATCH -N 1         	    # Use 1 nodes
#SBATCH -t 01:00:00  	    # Set 30 minute time limit
#SBATCH -p debug 	        # Submit to the debug 'partition'
#SBATCH -C haswell   # Use KNL nodes in quad cache format (default, recommended)
#SBATCH -J airlineIO
#SBATCH -o /project/projectdirs/dasrepo/ml_benchmarks/AirlineDelayBenchmark/slurm_logs/%j_haswell.log
#SBATCH -e /project/projectdirs/dasrepo/ml_benchmarks/AirlineDelayBenchmark/slurm_logs/%j_haswell.err
#SBATCH --account=dasrepo
##### SBATCH --license=SCRATCH   # note: specify license need for the file systems your job needs, such as SCRATCH,project

export HOSTNAME=cori
export ARK=haswell
source ../config/load_py3_2018.0.0.sh
echo $OMP_NUM_THREADS
srun -N 1 -n $OMP_NUM_THREADS python ../src/experiments/mpi_sklearn_pipeline.py 