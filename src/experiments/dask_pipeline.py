"""
Use Python 3.5
"""
import argparse
from distributed import Executor, Client, LocalCluster
import dask.dataframe as ddf
import numpy as np
import os
import psutil
import time

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
    # default values of parameters
    data_dir = "../../data/"
    log_dir = "../../slurm_logs/"
    no_of_files = 64
    default_no_of_threads = 1
    cpu_count = psutil.cpu_count()
    if cpu_count // 4 - 2 > 1:
        default_no_of_workers = cpu_count // 4 - 2
    else:
        default_no_of_workers = 2
    print("Max thread count from python is", cpu_count)
    dec_pt = 2

    parser = argparse.ArgumentParser(
        description="Launch dask workers on one node to read files."
    )
    parser.add_argument("--n_workers", default=default_no_of_workers, type=int,
                        help="number of dask workers "
                        )
    parser.add_argument("--n_threads", default=default_no_of_threads, type=int,
                        help="number of threads per worker"
                        )
    parser.add_argument("--n_files", default=no_of_files, type=int,
                        help="number of files in total to read in"
                        )
    parser.add_argument("--data_dir", default=data_dir, type=str,
                        help="path to the data dir, do not include file name"
                        )
    parser.add_argument("--output_json", default=True, type=bool,
                        help="bool, whether to save a log for timing"
                        )
    parser.add_argument("--script_dir", required=True, type=str,
                        help="str, the dir path of this script, do not included" +
                        "the actual script name. Needed for SLURM jobs"
                        )



    args = parser.parse_args()
    n_workers = args.n_workers
    n_threads = args.n_threads
    data_dir = args.data_dir
    no_of_files = args.n_files
    script_dir = args.script_dir
    data_dir = args.data_dir
    log_dir = script_dir + "/" + log_dir

    import sys
    sys.path.append(script_dir + "/../")
    # import my utils
    import utils

    if no_of_files < n_workers:
        raise ValueError("n_files = {0} > n_workers {1}".format(
            no_of_files, n_workers))

    # start script
    h5filelist = sorted(utils.getFileList(data_dir, 'h5'))
    # print(h5filelist[:no_of_files])
    file_size = utils.getFileSizeInGB(h5filelist[:no_of_files])
    print("File size to read in is {0:.0f} GB".format(file_size))

    cluster = LocalCluster(n_workers=n_workers, threads_per_worker=n_threads)
    client = Client(cluster)
    print("Using {0} workers and {1} thread(s) per worker".format(
        n_workers, n_threads))
    df = ddf.read_hdf(h5filelist[:no_of_files], 'csv', columns=columns)
    start_time = time.time()
    df = client.persist(df)
    print(df.index.compute())
    end_time = time.time()
    read_time = end_time - start_time
    # print("lines read in =", df.shape)
    print("Reading in {0} files in {1:.0f}s ".format(no_of_files, read_time))

    df_size = np.sum(df.memory_usage().compute()) / 1e9

    if args.output_json:
        from collections import OrderedDict
        import json
        timing_info = OrderedDict({})

        timing_info['git_commit'] = utils.capture_multiline_output(
            'git show | head -1')[0]
        timing_info['git_repo'] = utils.capture_multiline_output(
            'git remote -v ')[0]
        timing_info['conda_env'] = utils.capture_multiline_output(
            'conda list')
        timing_info['lscpu'] = utils.capture_multiline_output(
            'lscpu')
        timing_info['date'] = time.strftime('%Y-%m-%d-%H-%M-%S')
        timing_info['hostname'] = os.environ['HOSTNAME']
        timing_info['read_hdf_seconds'] = round(read_time, dec_pt)
        timing_info['file_size_GB'] = round(file_size, dec_pt)
        timing_info['file_IO_MB_per_second'] = \
            round(file_size * 1000 / read_time, dec_pt)
        timing_info['df_IO_MB_per_second'] = \
            round(df_size * 1000 / read_time, dec_pt)
        timing_info['df_size_GB'] = round(df_size, dec_pt)
        json_file = log_dir + "dask_io_perf_{}.json".format(
                timing_info['date'])
        print("outputting timing to ", json_file)
        with open(json_file, 'w') as f:
            json.dump(timing_info, f)
        for k in timing_info.keys():
            print("{0} = {1}".format(k, timing_info[k]))

    # df = df.dropna()
