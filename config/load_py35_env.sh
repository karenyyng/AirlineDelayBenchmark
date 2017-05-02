#!/bin/bash

# -------------
# Author: Karen Ng 
# usage: 
# source ./load_py35_env.sh
# -------------

if [[  $NERSC_HOST == "cori"* ]]; then
  DIR=/global/common/cori/software/python/3.5-anaconda
  ENV_DIR=$SCRATCH/py35_envs
  module load python/3.5-anaconda
  echo 'on Cori: echo finish loading python/3.5-anaconda'
else
  DIR=$HOME/miniconda3
  ENV_DIR=$HOME/miniconda3/py35_envs
fi

if [[ -f $HOME/.condarc ]]; then
  mv $HOME/.condarc $HOME/.condarc.backup
  echo 'backing up $HOME/.condarc to $HOME/.condarc.backup'
fi

CONDA=$DIR/bin/conda
$CONDA config --add channels intel
echo 'finished adding Intel channel in conda'

if [[ ! $(cat $HOME/.condarc) == *'py35_envs'* ]]; then
  echo $'envs_dirs:' >> ${HOME}/.condarc
  echo "  - ${ENV_DIR}" >> ${HOME}/.condarc
  echo 'appending envs_dirs at $ENV_DIR/py35_envs to ~/.condarc'
fi

if [[ ! $(grep 'PATH' unload_py35_env.sh) ]]; then 
  echo 'backing up PATH variable'
  echo "export PATH=$PATH" >> unload_py35_env.sh
fi

# may be replace /opt/intel/bin with an environmental variable instead?
if [ -d /opt/intel/bin ] && [ ! $PATH == *"/opt/intel/bin"* ]; then
  echo "/opt/intel/bin detected but not in PATH, adding /opt/intel/bin to PATH" 
  export PATH=/opt/intel/bin:$PATH 
fi;

echo "activating conda environment at $DIR/py35_envs/idp_35"
source $DIR/bin/activate idp_35

echo "Using some recommended settings that may not be the best for your use case"
echo "change the settings in this script for the best performance" 
export KMP_BLOCKTIME=1
export KMP_AFFINITY=granularity=core,noduplicates,compact,0,0
export MKL_DYNAMIC=false

# detect specific architecture for setting the number of threads 
export NUM_OF_THREADS=$(grep 'model name' /proc/cpuinfo | wc -l)  
if [[ $(grep 'model name' /proc/cpuinfo ) == *'Xeon Phi'* ]]; then
  export OMP_NUM_THREADS=$(( $NUM_OF_THREADS / 4 ))
else 
  export OMP_NUM_THREADS=$(( $NUM_OF_THREADS ))
fi
echo "$NUM_OF_THREADS threads possible"
echo "setting OMP_NUM_THREADS=$OMP_NUM_THREADS"


