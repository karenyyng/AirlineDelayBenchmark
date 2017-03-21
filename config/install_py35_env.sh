#!/bin/bash

# -------------
# Author: Karen Ng <mailto:karen.y.ng@intel.com>
# -------------

DIR=$HOME/miniconda3
export ACCEPT_INTEL_PYTHON_EULA=yes
echo 'accepting INTEL PYTHON EULA'
if [[  $HOSTNAME == "cori"* ]]; then
  module load python/3.5-anaconda  
  echo 'echo finish loading python/3.5-anaconda'
elif [[ ! $(which conda) ]]; then
  [ -f Miniconda3-latest-Linux-x86_64.sh ] || curl -O https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
  echo "installing miniconda3 at $DIR"
  bash ./Miniconda3-latest-Linux-x86_64.sh -b -p $DIR -f && \
  rm ./Miniconda3-latest-Linux-x86_64.sh
fi

$HOME/miniconda3/bin/conda config --add channels intel
echo 'finished adding Intel channel in conda'

mkdir ~/py35_envs
echo 'creating directory py_35_envs at $HOME'
# See https://www.nersc.gov/assets/Uploads/Intro-to-Python-at-NERSC.pdf page 10
# about the need to append to ~/.condarc on Cori at NERSC 
# we do not have the permission to write at the module file directory for Anaconda
# Python on Cori / Edison
echo $'envs_dirs:\n  - ~/py35_envs' >> ${HOME}/.condarc
echo 'appending envs_dirs to ~/.condarc at ~/py35_envs'
$HOME/miniconda3/bin/conda create -y -c intel -n idp_35 intelpython3_full python=3

echo 'installing additiona packages for functionality'
source load_py35_env.sh
pip install gnureadline
$HOME/miniconda3/bin/conda install -y keras 
# source ./theano_config/set_theano_optimizations.sh
