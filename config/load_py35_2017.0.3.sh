#!/bin/bash

# -------------
# Author: Karen Ng 
# usage: 
# source ./load_py35_VERSION.sh
# -------------
CONDA_ENV=idp35_201703

BASH_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [[ ! $(grep 'PATH' $BASH_DIR/unload_py35_env.sh) ]]; then 
  echo 'Backing up PATH variable'
  echo "export PATH=$PATH" >> $BASH_DIR/unload_py35_env.sh
fi

if [[  $NERSC_HOST == "cori"* ]]; then
  DIR=/global/common/cori/software/python/3.5-anaconda
  ENV_DIR=$SCRATCH/py35_envs
  module load python/3.5-anaconda
  echo 'On Cori: echo finish loading python/3.5-anaconda'
else
  DIR=$HOME/miniconda3
  ENV_DIR=$HOME/miniconda3/py35_envs
  PATH=$PATH:/opt/intel/vtune_amplifier_xe_2017/bin64/

fi

if [[ -f $HOME/.condarc ]]; then
  mv $HOME/.condarc $HOME/.condarc.backup
  echo 'Backing up $HOME/.condarc to $HOME/.condarc.backup'
fi

CONDA=$DIR/bin/conda
$CONDA config --add channels intel
echo 'Finished adding Intel channel in conda'

if [[ ! $(cat $HOME/.condarc) == *'py35_envs'* ]]; then
  echo $'envs_dirs:' >> ${HOME}/.condarc
  echo "  - ${ENV_DIR}" >> ${HOME}/.condarc
  echo 'Appending envs_dirs at $ENV_DIR/py35_envs to ~/.condarc'
fi

# may be replace /opt/intel/bin with an environmental variable instead?
if [ -d /opt/intel/bin ] && [ ! $PATH == *"/opt/intel/bin"* ]; then
  echo "/opt/intel/bin detected but not in PATH, adding /opt/intel/bin to PATH" 
  export PATH=/opt/intel/bin:$PATH 
fi;

echo "Activating conda environment at $DIR/py35_envs/$CONDA_ENV"
source $DIR/bin/activate $CONDA_ENV

# echo "Using some recommended settings that may not be the best for your use case"
# echo "Change the settings in this script for the best performance" 
export KMP_BLOCKTIME=200
# # # https://software.intel.com/en-us/node/522691
# export KMP_AFFINITY=granularity=fine,compact
# # # https://software.intel.com/en-us/mkl-macos-developer-guide-mkl-dynamic
# export MKL_DYNAMIC=false
# export HPL_LARGEPAGE=1
echo "Setting KMP_BLOCKTIME = $KMP_BLOCKTIME"
echo "Setting KMP_AFFINITY = $KMP_AFFINITY"
echo "Setting MKL_DYNAMIC = $MKL_DYNAMIC"
echo "Setting HPL_LARGEPAGE= $HPL_LARGEPAGE"
# 
export NUM_OF_THREADS=$(grep 'model name' /proc/cpuinfo | wc -l)  
export OMP_NUM_THREADS=$(( $NUM_OF_THREADS / 2 ))
export MKL_NUM_THREADS=$(( $NUM_OF_THREADS / 2 ))
# export KMP_HW_SUBSET=${OMP_NUM_THREADS}c,1t  # or use 64c,2t 
echo "$NUM_OF_THREADS threads possible"
echo "Setting OMP_NUM_THREADS=$OMP_NUM_THREADS"
echo "Setting MKL_NUM_THREADS=$MKL_NUM_THREADS"
echo "Setting KMP_HW_SUBSET=$KMP_HW_SUBSET"
