# Install instructions for GitHub repo:
```
$ git clone https://github.intel.com/karenyin/AirlineDelayIntelBenchmark.git
$ git fetch 
$ git checkout io 
$ cd ./AirlineDelayIntelBenchmark/
$ source config/install_py3_2018.0.0.sh
```

This should install the Conda Python environment and create a script called
```
$SOME_PATH/AirlineDelayIntelBenchmark/config/load_py3_2018.0.0.sh 
```

Do `$source load_py3_2018.0.0.sh` every time you need to load the environment.
You will see your command prompt has `(airline)` prepend to it when the
environment is loaded properly.
And use `source deactivate` to unload the environment when you are done. 

# Downloading the csv data then converting them to HDF5
```
cd $SOME_PATH/AirlineDelayIntelBenchmark/data
source download_new_rita_files.sh
source convert_csv_to_hdf5.sh
```

# To run the benchmark scripts: 
## Running the Dask example
### Haswell 
```
cd  $SOME_PATH/AirlineDelayIntelBenchmark/src/experiments/
python dask_pipeline.py --n_workers 32 --n_threads 1 --n_files 32
```
Then it should print out the timing of the IO script parallelized by Dask.

### KNL
```
cd  $SOME_PATH/AirlineDelayIntelBenchmark/src/experiments/
python -m tbb dask_pipeline.py --n_workers $NWORKERS --n_threads 1 --n_files $NWORKERS
```
in this case `NWORKERS` < 68. 

## Running the MPI4Py example
### Haswell
```
cd  $SOME_PATH/AirlineDelayIntelBenchmark/src/experiments/
mpirun -n 32 python mpi_sklearn_pipeline.py
```
### KNL
