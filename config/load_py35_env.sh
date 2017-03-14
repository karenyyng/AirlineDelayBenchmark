#!/bin/bash

# -------------
# Author: Karen Ng 
# usage: 
# source ./load_py35_env.sh
# -------------
if [[  $HOSTNAME == "cori"* ]]; then
  module load python/3.5-anaconda
  echo 'echo finish loading python/3.5-anaconda'
  source activate $HOME/py35_envs/idp_35
  echo 'activating conda environment at $HOME/py35_envs/idp_35'
else
  source activate idp_35
fi

echo "Using some recommended settings that may not be the best for your use case"
echo "change the settings in this script for the best performance" 
export KMP_BLOCKTIME=1
# export KMP_AFFINITY=verbose, granularity=core,noduplicates,compact,0,0
export KMP_AFFINITY=granularity=core,noduplicates,compact,0,0
export NUM_OF_THREADS=$(grep 'model name' /proc/cpuinfo | wc -l)  
echo "max no. of threads possible: $NUM_OF_THREADS"
# for KNL with bootable OS, the recommended number of OMP_NUM_THREADS = NUM_OF_THREADS / 4 - 1 
export OMP_NUM_THREADS=$(( $NUM_OF_THREADS / 4 - 1 ))
echo "setting OMP_NUM_THREADS=$OMP_NUM_THREADS"
export MKL_DYNAMIC=false

# may be replace /opt/intel/bin with an environmental variable instead?
if [ -d /opt/intel/bin ] && [ ! $PATH == *"/opt/intel/bin"* ]; then
  echo "/opt/intel/bin detected but not in PATH, adding /opt/intel/bin to PATH" 
  export PATH=/opt/intel/bin:$PATH 
fi;
