"""
Code to perform parallel io via MPI
"""

from mpi4py import MPI
# import numpy as np
import pandas as pd
import numpy as np
import time

# import scripts that Karen wrote
# import serial_preprocess_data as preprocess
import utils

h5list = utils.getFileList("../data/", "h5")
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
workers = comm.Get_size()

columns = ['Year',
           'Cancelled',
           'Distance',
           'Diverted',
           'ArrTime',
           'Dest',
           'FlightNum',
           # 'DepDelay',  ## not using DepDelay
           'ActualElapsedTime',
           'ArrDelay',
           'DayofMonth',
           'UniqueCarrier',
           'Month',
           'DepTime',
           'Origin',
           'DayOfWeek'
           ]


# divide up the workload
subset = 100
files_per_worker = int(len(h5list[:subset]) / workers)
chunk_to_read = 0
if rank == workers - 1:
    chunk_to_read = len(h5list) % workers

print("Rank {0} reading in files from {1} to {2}".format(
    rank, rank * files_per_worker,
    (rank + 1) * files_per_worker + chunk_to_read))

df = [pd.read_hdf("../data/" + h5list[no], columns=columns)
      for no in range(rank * files_per_worker,
                      (rank + 1) * files_per_worker + chunk_to_read)]

print("Rank {} has finished reading in h5 file".format(rank))
if len(df) > 0:
    start_time = time.time()
    df_list = comm.gather(df, root=0)
    end_time = time.time()

if rank == 0:
    from itertools import chain
    print("Each worker will read in {} files".format(files_per_worker))
    print("Last worker has {} more files to read in".format(chunk_to_read))
    print("Size of files going through IO is {0:.2f} GB".format(
        utils.getFileSizeInGB(
            ["../data/" + h5file for h5file in h5list[:workers]])))
    print("Reading in {0} selected columns only".format(len(columns)))
    print("Gathering read df took {0:.0f} s".format(end_time - start_time))
    start_time = time.time()
    df_list = list(chain.from_iterable(df_list))
    df = pd.concat(df_list)
    end_time = time.time()
    print("Concatenating df took {0:.0f} s".format(end_time - start_time))
    print("Memory usage of the data frame is {0:.2f} GB".format(
        np.sum(df.memory_usage()) / 1e9))
    print("Shape of df is ", df.shape)
    print("Dtype of df is ", df.dtypes)
