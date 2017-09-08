# -------------
# Author: Karen Ng <mailto:karen.y.ng@intel.com>
# depedency: curl
# usage:
# source install_py35_env.sh
# -------------
CONDA_ENV=airlinedelay
if echo "$(uname -a)" | grep Linux ; then
  OS=Linux
else
  OS=MacOSX 
fi
echo "Running on the OS = ${OS}"

export ACCEPT_INTEL_PYTHON_EULA=yes
if [[ -f $HOME/.condarc ]]; then
  mv $HOME/.condarc $HOME/.condarc.backup
  echo 'backing up $HOME/.condarc to $HOME/.condarc.backup'
fi

echo 'accepting INTEL PYTHON EULA'
if [[  $NERSC_HOST == "cori" ]]; then
  DIR=/global/common/cori/software/python/3.5-anaconda
  ENV_DIR=/global/common/software/bdc
  module load python/3.5-anaconda  
  echo 'echo finish loading python/3.5-anaconda'
elif [[ ! $(which conda) ]]; then
  [ -f Miniconda3-latest-${OS}-x86_64.sh ] || curl -O "https://repo.continuum.io/miniconda/Miniconda3-latest-${OS}-x86_64.sh"
  DIR=$HOME/miniconda3
  ENV_DIR=$DIR
  echo "installing miniconda3 at $DIR"
  bash ./Miniconda3-latest-${OS}-x86_64.sh -b -p $DIR -f 
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
$CONDA create -y -c intel -n $CONDA_ENV intelpython3_full=2017.0.3 python=3.5
echo 'installing additiona packages for functionality'

BASH_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $BASH_DIR/load_py35_2017.0.3.sh
$CONDA install -y pysocks=1.6.6 \
  # dask=0.15.0=py35_0 \
  psutil=5.2.2=py35_0 \
  graphviz=2.38.0 \
  python-graphviz=0.5.2=py35_0 \
  memory_profiler=0.43=py35_0 \ 
  paramiko=2.1.2=py35_0 \
  line_profiler
$CONDA install -c conda-forge category_encoders 

pip install --no-deps py==1.4.33 \
  gnureadline==6.3.3 \
  # keras==2.0.2 \
  pygal==2.0.13 \
  pygaljs==1.0.1 \
  # xgboost==0.6a2 \
  dask-searchcv==0.0.2 
pip install pytest==3.0.7 git+ssh://git@github.com/karenyyng/pytest-benchmark.git
# pip install dask-xgboost==0.1.3 
# source ./theano_config/set_theano_optimizations.sh

if [ -f Miniconda3-latest-${OS}-x86_64.sh ]; then 
  rm ./Miniconda3-latest-${OS}-x86_64.sh
fi
