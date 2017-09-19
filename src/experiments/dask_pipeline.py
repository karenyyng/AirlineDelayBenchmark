"""
Use Python 3.5
"""
import sys
sys.path.append("../")
import argparse
from distributed import Executor, Client, LocalCluster
import dask
import dask.dataframe as ddf
import os
import psutil

# import my utils
import utils
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Launch dask workers on one single node to read files."
    )
    cpu_count = psutil.cpu_count()
    print("Max thread count from python is", cpu_count)
    default_no_of_threads = 1
    if cpu_count // 4 - 2 > 1:
        default_no_of_workers = cpu_count // 4 - 2
    else:
        default_no_of_workers = 2
    h5filelist = utils.getFileList("../../data/", 'h5')
    no_of_files = 20
    print("File size to read in is {0:.0f} GB".format(
          utils.getFileSizeInGB(h5filelist[:no_of_files])))
    parser.add_argument("--n_workers", default=default_no_of_workers, type=int,
                        help="number of dask workers "
                        )
    parser.add_argument("--n_threads", default=default_no_of_threads, type=int,
                        help="number of threads per workers "
                        )
    parser.add_argument("--n_file", default=no_of_files, type=int,
                        help="number of files in total to read in"
                        )

    args = parser.parse_args()
    n_workers = args.n_workers
    n_threads = args.n_threads
    cluster = LocalCluster(n_workers=n_workers, threads_per_worker=n_threads)
    client = Client(cluster)
    print("Using {0} workers and {1} thread(s) per worker".format(
        n_workers, n_threads))
    print("Reading in {} files".format(no_of_files))
    df = ddf.read_hdf(h5filelist[:no_of_files], 'csv', columns=columns)
    print(df.compute().shape)



    # df = df.dropna()
    # print(df.describe().compute())
