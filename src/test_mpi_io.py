"""
Code to perform parallel io via MPI
"""

from mpi4py import MPI
# import numpy as np
import pandas as pd
import time

# import scripts that Karen wrote
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

df = pd.read_hdf(h5list[rank], columns=columns)
print("Rank {} has finished reading in h5 file".format(rank))
if rank == 0:
    start_time = time.time()
    df_list = comm.gather(df, root=0)
    end_time = time.time()
    print("Gathering read df took {} s".format(start_time - end_time))
