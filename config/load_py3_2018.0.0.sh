export CONDA_ENV=airline
export ENV_DIR=/global/common/software/bdc
export INTEL_PYTHON_VERSION=2018.0.0
export PY_VERSION=35
export PY_DOT_VERSION=3.5
export PY_MAJOR_VERSION=3
if [[ -z $CONDA_ENV  ]]; then
   echo "CONDA_ENV is not defined. Quitting installation script."
   exit 1
fi

if [[  $NERSC_HOST == "cori"* ]]; then
  DIR=/global/common/cori/software/python/3.5-anaconda
  # ENV_DIR=/global/common/software/bdc/py35_envs
  module load python/3.5-anaconda
  echo 'On Cori: echo finish loading python/3.5-anaconda'
  module load craype-hugepages2M
  echo 'On Cori: loading craype-hugepages2M'
fi

export CONDA=$ENV_DIR/py${PY_VERSION}_envs/${CONDA_ENV}/bin/conda
cp $HOME/.condarc_$CONDA_ENV $HOME/.condarc

echo "Activating conda environment at $ENV_DIR/py35_envs/$CONDA_ENV using"
echo "source ${ENV_DIR}/py${PY_VERSION}_envs/${CONDA_ENV}/bin/activate $CONDA_ENV"
source ${ENV_DIR}/py${PY_VERSION}_envs/${CONDA_ENV}/bin/activate $CONDA_ENV

# echo "Using some recommended settings that may not be the best for your use case"
export NUM_OF_THREADS=$(grep 'model name' /proc/cpuinfo | wc -l)
# # # https://software.intel.com/en-us/node/522691
# export KMP_AFFINITY=granularity=fine,compact
# # # https://software.intel.com/en-us/mkl-macos-developer-guide-mkl-dynamic
# export MKL_DYNAMIC=false

if [[ $(grep 'model name' /proc/cpuinfo ) == *'Xeon Phi'*  ]]; then
  export KMP_AFFINITY=granularity=fine,compact
  export MKL_DYNAMIC=false
  export HPL_LARGEPAGE=1
  export KMP_BLOCKTIME=800
  export OMP_NUM_THREADS=$(( $NUM_OF_THREADS / 4 ))
  export MKL_NUM_THREADS=$(( $NUM_OF_THREADS / 4 ))
  export KMP_HW_SUBSET=${OMP_NUM_THREADS}c,1t  # or use 64c,2t 
  export MKL_VERBOSE=1
  export MKL_FFT_VERBOSE=1
else 
  export KMP_BLOCKTIME=800
  export OMP_NUM_THREADS=$(( $NUM_OF_THREADS / 4  ))
  export MKL_NUM_THREADS=$(( $NUM_OF_THREADS / 4 ))
fi

echo "Setting KMP_BLOCKTIME = $KMP_BLOCKTIME"
echo "Setting KMP_AFFINITY = $KMP_AFFINITY"
echo "Setting MKL_DYNAMIC = $MKL_DYNAMIC"
echo "Setting HPL_LARGEPAGE= $HPL_LARGEPAGE"
echo "Setting OMP_NUM_THREADS=$OMP_NUM_THREADS"
echo "Setting MKL_NUM_THREADS=$MKL_NUM_THREADS"
echo "Setting KMP_HW_SUBSET=$KMP_HW_SUBSET"
echo "Setting MKL_VERBOSE=$MKL_VERBOSE"
echo "Setting MKL_FFT_VERBOSE=$MKL_FFT_VERBOSE"
echo "Setting HUGETLB_DEFAULT_PAGE_SIZE=$HUGETLB_DEFAULT_PAGE_SIZE"
echo "Setting PE_HUGEPAGES_PKGCONFIG_VARIABLES=$PE_HUGEPAGES_PKGCONFIG_VARIABLES"
echo "PE_HUGEPAGES_TEXT_SEGMENT=$PE_HUGEPAGES_TEXT_SEGMENT"
echo "PE_HUGEPAGES_TEXT_SEGMENT=$PE_HUGEPAGES_TEXT_SEGMENT"
echo "PE_HUGEPAGES_PAGE_SIZE=$PE_HUGEPAGES_PAGE_SIZE"
echo "HUGETLB_MORECORE_HEAPBASE=$HUGETLB_MORECORE_HEAPBASE"
echo "HUGETLB_MORECORE=$HUGETLB_MORECORE"
echo "HUGETLB_ELFMAP=$HUGETLB_ELFMAP"
echo "HUGETLB_FORCE_ELFMAP=$HUGETLB_FORCE_ELFMAP"
module load java
module load scala
