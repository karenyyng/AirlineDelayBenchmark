from dask_preprocess_data import *
from dask_EDA import *
import logging
# import os

# logger = logging.getLogger("DebugInfo")
# logger.setLevel(logging.DEBUG)


def run():
    data_dir = "../data/"

    predict_col = ["ArrDelay"]
    cols = ['Year',
            'Cancelled',
            'Distance',
            'Diverted',
            'ArrTime',
            'Dest',
            'FlightNum',
            'DepDelay',
            'ActualElapsedTime',
            'ArrDelay',
            'TaxiOut',
            'DayofMonth',
            'UniqueCarrier',
            'Month',
            'DepTime',
            'Origin',
            'TaxiIn',
            'DayOfWeek'
            ]
    df = readFiles(data_dir, fileExt="h5", noOfFiles=11, cols=cols)
    df = removeNaNs(df)
    print("\n\nmean of ArrDelay is {}\n\n".format(dask.compute(df.ArrDelay.mean())))

if __name__ == "__main__":
    n_workers = 2
    threads_per_worker = 1
    cluster = LocalCluster(n_workers=n_workers,
                           threads_per_worker=threads_per_worker)
    client = Client(cluster)
    executor = Executor(cluster)
    run()
