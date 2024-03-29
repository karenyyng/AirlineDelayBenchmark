# -------------
# Author: Karen Ng <mailto:karen.y.ng@intel.com>
# dependency: wget
# usage:
# source THIS_SCRIPT.sh
# -------------

export CONDA_ENV=airline
export INTEL_PYTHON_VERSION=2018.0.0
export PY_VERSION=35
export PY_DOT_VERSION=3.5 
export PY_MAJOR_VERSION=3
export EDITION=full
if [[  $NERSC_HOST == "cori"  ]]; then
  export ENV_DIR=$SCRATCH
else 
  export DIR=$HOME/miniconda${PY_MAJOR_VERSION}
  export ENV_DIR=$HOME/miniconda${PY_MAJOR_VERSION}
fi
echo "ENV_DIR=$ENV_DIR"

BASH_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"
if [[ ! -f ${BASH_DIR}/setup_conda.sh ]]; then
  wget -O ${BASH_DIR}/setup_conda.sh https://gist.githubusercontent.com/karenyyng/d854662dadd2f1fa027bc87abf0a045c/raw
fi
if [[ ! -f ${BASH_DIR}/load_conda.sh ]]; then
  wget -O ${BASH_DIR}/load_conda.sh https://gist.github.com/karenyyng/692025f1cc8ec753cd44a6cc9f78db6a/raw 
fi  
source ${BASH_DIR}/setup_conda.sh
source ${BASH_DIR}/load_conda.sh

if [[ ! -f ${BASH_DIR}/load_py${PY_MAJOR_VERSION}_${INTEL_PYTHON_VERSION}.sh ]]; then
  echo 'Creating file for reloading the environment'
  echo "export CONDA_ENV=$CONDA_ENV" > ${BASH_DIR}/load_py${PY_MAJOR_VERSION}_${INTEL_PYTHON_VERSION}.sh
  echo "export ENV_DIR=$ENV_DIR" >> ${BASH_DIR}/load_py${PY_MAJOR_VERSION}_${INTEL_PYTHON_VERSION}.sh
  echo "export INTEL_PYTHON_VERSION=$INTEL_PYTHON_VERSION" >> ${BASH_DIR}/load_py${PY_MAJOR_VERSION}_${INTEL_PYTHON_VERSION}.sh
  echo "export PY_VERSION=$PY_VERSION" >> ${BASH_DIR}/load_py${PY_MAJOR_VERSION}_${INTEL_PYTHON_VERSION}.sh
  echo "export PY_DOT_VERSION=$PY_DOT_VERSION" >> ${BASH_DIR}/load_py${PY_MAJOR_VERSION}_${INTEL_PYTHON_VERSION}.sh
  echo "export PY_MAJOR_VERSION=$PY_MAJOR_VERSION" >> ${BASH_DIR}/load_py${PY_MAJOR_VERSION}_${INTEL_PYTHON_VERSION}.sh
  echo "export SPARK_HOME=$ENV_DIR/py35_envs/$CONDA_ENV/lib/python3.6/site-packages/pyspark" >> ${BASH_DIR}/load_py${PY_MAJOR_VERSION}_${INTEL_PYTHON_VERSION}.sh
  cat ${BASH_DIR}/load_conda.sh >> ${BASH_DIR}/load_py${PY_MAJOR_VERSION}_${INTEL_PYTHON_VERSION}.sh
fi 

echo "Using conda at $CONDA"
$CONDA install -y -c intel \
scikit-learn=0.18.2 \
jupyter=1.0.0 \
matplotlib=2.0.2 \
h5py=2.7.0 \
dask=0.15.2 \
psutil=5.2.2 \
paramiko=2.1.2 \
distributed=1.18.1 \
pytables=3.3.0 \
numba=0.34.0 \
mpi4py=2.0.0
$CONDA install -y memory_profiler line_profiler bokeh pysocks=1.6.6 
$CONDA install -y -c conda-forge category_encoders \
  pyspark=2.2.0 \

pip install --no-deps py==1.4.33 \
  pygal==2.0.13 \
  pygaljs==1.0.1 \
  gprof2dot


# pip install pytest==3.0.7 git+ssh://git@github.com/karenyyng/pytest-benchmark.git
# pip install dask-xgboost==0.1.3 
# source ./theano_config/set_theano_optimizations.sh

if [ -f Miniconda3-latest-${OS}-x86_64.sh ]; then 
  rm -f ./Miniconda3-latest-${OS}-x86_64.sh
fi
if [ -f ${BASH_DIR}/load_conda.sh ]; then
  rm -f ${BASH_DIR}/load_conda.sh
fi
if [ -f ${BASH_DIR}/setup_conda.sh ]; then
  rm -f ${BASH_DIR}/setup_conda.sh
fi

if [[  $NERSC_HOST == "cori"  ]]; then
  echo "module load java" >> ${BASH_DIR}/load_py${PY_MAJOR_VERSION}_${INTEL_PYTHON_VERSION}.sh
  echo "module load scala" >> ${BASH_DIR}/load_py${PY_MAJOR_VERSION}_${INTEL_PYTHON_VERSION}.sh
fi
