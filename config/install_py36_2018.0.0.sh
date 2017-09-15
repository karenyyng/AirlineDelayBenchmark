# -------------
# Author: Karen Ng <mailto:karen.y.ng@intel.com>
# dependency: curl wget
# usage:
# source THIS_SCRIPT.sh
# -------------

export CONDA_ENV=airline
export INTEL_PYTHON_VERSION=2018.0.0
export PY_VERSION=36
export PY_DOT_VERSION=3.6
export PY_MAJOR_VERSION=3
export EDITION=core

BASH_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"
if [[ ! -f ${BASH_DIR}/setup_conda.sh ]]; then
  wget -O ${BASH_DIR}/setup_conda.sh https://gist.githubusercontent.com/karenyyng/d854662dadd2f1fa027bc87abf0a045c/raw/6da28836adce9b4d5c751599299ed5227504455a/setup_conda.sh 
fi
if [[ ! -f ${BASH_DIR}/load_conda.sh ]]; then
  wget -O ${BASH_DIR}/load_conda.sh https://gist.githubusercontent.com/karenyyng/692025f1cc8ec753cd44a6cc9f78db6a/raw/c9df0d8c348632748b2af96d4c55d1ab14cc0927/load_conda.sh 

fi  
source ${BASH_DIR}/setup_conda.sh
source ${BASH_DIR}/load_conda.sh

if [[ ! -f ${BASH_DIR}/load_py${PY_VERSION}_${INTEL_PYTHON_VERSION}.sh ]]; then
  echo 'Creating file for reloading the environment'
  echo 'export CONDA_ENV=airline' > ${BASH_DIR}/load_py${PY_VERSION}_${INTEL_PYTHON_VERSION}.sh
  echo 'export INTEL_PYTHON_VERSION=2018.0.0' >> ${BASH_DIR}/load_py${PY_VERSION}_${INTEL_PYTHON_VERSION}.sh
  echo 'export PY_VERSION=35' >> ${BASH_DIR}/load_py${PY_VERSION}_${INTEL_PYTHON_VERSION}.sh
  echo 'export PY_DOT_VERSION=3.5' >> ${BASH_DIR}/load_py${PY_VERSION}_${INTEL_PYTHON_VERSION}.sh
  echo 'export PY_MAJOR_VERSION=3' >> ${BASH_DIR}/load_py${PY_VERSION}_${INTEL_PYTHON_VERSION}.sh
  cat ${BASH_DIR}/load_conda.sh >> ${BASH_DIR}/load_py${PY_VERSION}_${INTEL_PYTHON_VERSION}.sh
fi 

echo "Using conda at $CONDA"
$CONDA install -y -c intel \
category_encoders \
scikit-learn=0.18.2 \
jupyter=1.0.0 \
matplotlib \
h5py=2.7.0 \
pysocks=1.6.6 \
dask=0.15.2 \
psutil=5.2.2 
graphviz=2.38.0 \
# python-graphviz=0.5.2=py35_0 \
paramiko=2.1.2=py35_0 \
distributed=1.18.1 \
pytables=3.3.0 \
numba
$CONDA install -y memory_profiler line_profiler
# $CONDA install -y -c conda-forge category_encoders 

pip install --no-deps py==1.4.33 \
  gnureadline==6.3.3 \
  # keras==2.0.2 \
  pygal==2.0.13 \
  pygaljs==1.0.1 \
  category_enconders=1.2.4
  # xgboost==0.6a2 \
# pip install pytest==3.0.7 git+ssh://git@github.com/karenyyng/pytest-benchmark.git
# pip install dask-xgboost==0.1.3 
# source ./theano_config/set_theano_optimizations.sh

if [ -f Miniconda3-latest-${OS}-x86_64.sh ]; then 
  rm ./Miniconda3-latest-${OS}-x86_64.sh
fi
if [ -f ${BASH_DIR}/load_conda.sh ]; then
  rm ${BASH_DIR}/load_conda.sh
fi
if [ -f ${BASH_DIR}/setup_conda.sh ]; then
  rm ${BASH_DIR}/setup_conda.sh
fi
