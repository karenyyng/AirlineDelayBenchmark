"""
Code to perform parallel io via MPI
"""

from mpi4py import MPI
# import numpy as np
import pandas as pd
import numpy as np
import time
from collections import OrderedDict

# import scripts that Karen wrote
# import serial_preprocess_data as preprocess
import utils

h5list = utils.getFileList("../../data/", "h5")
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
subset = 50
files_per_worker = int(len(h5list[:subset]) / workers)
chunk_to_read = 0
if rank == workers - 1:
    chunk_to_read = len(h5list) % workers

print("Rank {0} reading in files from {1} to {2}".format(
    rank, rank * files_per_worker,
    (rank + 1) * files_per_worker + chunk_to_read))
start_time = time.time()
df = [pd.read_hdf("../data/" + h5list[no], columns=columns)
      for no in range(rank * files_per_worker,
                      (rank + 1) * files_per_worker + chunk_to_read)]
end_time = time.time()

print("Worker {0} has finished reading in h5 file in {1:.2f}s".format(
    rank, end_time - start_time))

read_df_time = comm.gather(end_time - start_time, root=0)

start_time = time.time()
df_list = comm.gather(df, root=0)
end_time = time.time()

gather_time = comm.gather(end_time - start_time, root=0)
print("Worker {0} has gathered h5 file in {1:.2f}s".format(
    rank, end_time - start_time))

if rank == 0:
    verbose = True
    save_json = True

    timing_info = OrderedDict({})
    timing_info['git_commit'] = utils.capture_multiline_output(
        'git show | head -1')[0]
    timing_info['git_repo'] = utils.capture_multiline_output(
        'git remote -v ')[0]
    timing_info['conda_env'] = utils.capture_multiline_output(
        'conda list')
    timing_info['conda_env'] = utils.capture_multiline_output(
        'lscpu')[0]
    timing_info['read_hdf_seconds'] = \
        np.array([round(read_time, 2) for read_time in read_df_time])
    timing_info['gather_hdf_seconds'] = \
        np.array([round(read_time, 2) for read_time in gather_time])

    from itertools import chain

    start_time = time.time()
    df = pd.concat(list(chain.from_iterable(df_list)))
    end_time = time.time()

    timing_info['df.concat_seconds'] = round(end_time - start_time, 2)
    timing_info['file_size_GB'] = round(utils.getFileSizeInGB(
            ["../data/" + h5file for h5file in h5list[:workers]]), 2)
    timing_info['df_size_GB'] = round(np.sum(df.memory_usage()) / 1e9, 2)
    timing_info['median_read_gather_concat_time_seconds'] = \
        np.median(timing_info['read_hdf_seconds'] +
                  timing_info['gather_hdf_seconds']
                  ) + timing_info['df.concat_seconds']
    timing_info['file_IO_MB_per_second'] = \
        round(timing_info['file_size_GB'] * 1000 /
              timing_info['median_read_gather_concat_time_seconds'], 2)

    timing_info['df_IO_MB_per_second'] = \
        round(timing_info['df_size_GB'] * 1000 /
              timing_info['median_read_gather_concat_time_seconds'], 2)

    # timing_info['IO_GB_per_second'] =
    timing_info['df_shape'] = df.shape
    timing_info['date'] = time.strftime('%Y-%m-%d-%H-%M-%S')
    timing_info['read_hdf_seconds'] = \
        list(timing_info['read_hdf_seconds'])
    timing_info['gather_hdf_seconds'] = \
        list(timing_info['gather_hdf_seconds'])
    timing_info['no_of_workers'] = workers

    if verbose:
        for k in timing_info:
            print("{0} = {1}".format(k, timing_info[k]))

    if save_json:
        import json
        with open("../slurm_logs/mpi4py_io_perf_{}.json".format(
                timing_info['date']), 'w') as f:
            json.dump(timing_info, f)
