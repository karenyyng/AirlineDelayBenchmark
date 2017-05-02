#!/bin/bash

# -------------
# Author: Karen Ng <mailto:karen.y.ng@intel.com>
# depedency: curl
# usage:
# source install_py35_env.sh
# -------------

export ACCEPT_INTEL_PYTHON_EULA=yes
if [[ -f $HOME/.condarc ]]; then
  mv $HOME/.condarc $HOME/.condarc.backup
  echo 'backing up $HOME/.condarc to $HOME/.condarc.backup'
fi

echo 'accepting INTEL PYTHON EULA'
if [[  $NERSC_HOST == "cori" ]]; then
  DIR=/global/common/cori/software/python/3.5-anaconda
  ENV_DIR=$SCRATCH
  module load python/3.5-anaconda  
  echo 'echo finish loading python/3.5-anaconda'
elif [[ ! $(which conda) ]]; then
  [ -f Miniconda3-latest-Linux-x86_64.sh ] || curl -O https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
  DIR=$HOME/miniconda3
  ENV_DIR=$DIR
  echo "installing miniconda3 at $DIR"
  bash ./Miniconda3-latest-Linux-x86_64.sh -b -p $DIR -f &&
  rm ./Miniconda3-latest-Linux-x86_64.sh
fi

CONDA=$DIR/bin/conda
$CONDA config --add channels intel
echo 'finished adding Intel channel in conda'

if [[ ! -d $ENV_DIR/py35_envs ]]; then
  mkdir $ENV_DIR/py35_envs
  echo 'creating directory py35_envs at $HOME'
fi
# See https://www.nersc.gov/assets/Uploads/Intro-to-Python-at-NERSC.pdf page 10
# about the need to append to ~/.condarc on Cori at NERSC 
# we do not have the permission to write at the module file directory for Anaconda
# Python on Cori / Edison
if [[ ! $(cat $HOME/.condarc) == *'py35_envs'* ]]; then
  echo $'envs_dirs:' >> ${HOME}/.condarc
  echo "  - ${ENV_DIR}/py35_envs" >> ${HOME}/.condarc
  echo 'appending envs_dirs at $ENV_DIR/py35_envs to ~/.condarc'
fi

### cannot reinstall exact package versions from intel channel using a yaml file 
### $CONDA env create -f=./conda_py35_env.yaml -p $ENV_DIR/py35_envs
$CONDA create -y -c intel -n idp_35 intelpython3_full=2017.0.2 python=3.5
echo 'installing additiona packages for functionality'
source load_py35_env.sh
pip install --no-deps gnureadline==6.3.3 keras==2.0.2
# source ./theano_config/set_theano_optimizations.sh

