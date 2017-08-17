#!/usr/bin/env python
"""
routines to preprocess data using dask
"""

import logging
from distributed import Executor, Client, LocalCluster
import os
import psutil
import dask.dataframe as ddf


allCols = ['ArrDelay', 'ActualElapsedTime', 'Dest', 'Cancelled', 'TaxiIn',
           'Distance', 'UniqueCarrier', 'FlightDate', 'DayOfWeek', 'Origin',
           'Month', 'DayofMonth', 'TaxiOut', 'Diverted', 'Year', 'DepDelay',
           'DepTime', 'ArrTime', 'FlightNum']

categorical_cols = ['Origin', 'Dest', 'UniqueCarrier']


def startLocalCluster(n_workers=int((psutil.cpu_count())//4) - 1,
                      threads_per_worker=1):
    """
    start a cluster with n_workers and each worker can run with ncores
    This is only an example code, don't use for starting a cluster
    This should be coded inside the __name__ == "__main__" section
    """
    if n_workers < 1:
        n_workers = 1
    cluster = LocalCluster(n_workers=n_workers,
                           threads_per_worker=threads_per_worker)
    client = Client(cluster)
    executor = Executor(cluster)
    return client, executor


def readFiles(data_dir="../data/", noOfFiles=None, fileExt="csv", cols=None):
    dataFiles = [data_dir + file for file in os.listdir(data_dir)
                 if fileExt in file]

    print("Reading in {} files".format(noOfFiles))
    print("Total size of files to read in is {} GB".format(
        fileSizeInGB(dataFiles[:noOfFiles])))
    files = sorted(dataFiles[:noOfFiles])
    print("processing files {}".format(files))

    if noOfFiles is None:
        noOfFiles = len(dataFiles)

    if cols is None:
        cols = allCols

    if fileExt == "csv":
        return ddf.read_csv(files, usecols=cols)
    elif fileExt == "h5":
        # less memory efficient since we read in all the columns in this
        # approach
        return ddf.read_hdf(files, key='csv')[cols]
    else:
        raise NotImplementedError("Can only read fileExt csv or hdf5")


def convertDataToHdf5(data_dir="../data"):
    pass


def repartitionData():
    """
    Repartition data according to Dask performance tips
    [http://dask.pydata.org/en/latest/dataframe-performance.html#repartition-to-reduce-overhead]
    :parallelism:
    """
    pass


def createNumericalDate():
    """

    :parallelism:
    """
    return


def featureEncoder(cols=[]):
    """
    if we want to use distance based clustering / classification algorithms"""
    return


def standardScaler(cols=[]):
    """

    :parallelism:
    """
    return


def removeNaNs(df, col=["ArrDelay"]):
    return df.dropna(subset=col)


def removeCanceled():
    """

    :parallelism:
    """
    return


def removeDiverted():
    """

    :parallelism:
    """
    return


def stratifyKFoldWithDask():
    return


def randomSearchPipeline():
    return
