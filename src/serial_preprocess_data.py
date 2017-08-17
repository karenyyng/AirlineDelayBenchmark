"""
Serial version of all the IO and processing steps for a data pipeline
"""
import argparse
import os
import pandas as pd
import pyarrow.parquet as pq


all_cols = ['ArrDelay', 'ActualElapsedTime', 'Dest', 'Cancelled', 'TaxiIn',
            'Distance', 'UniqueCarrier', 'FlightDate', 'DayOfWeek', 'Origin',
            'Month', 'DayofMonth', 'TaxiOut', 'Diverted', 'Year', 'DepDelay',
            'DepTime', 'ArrTime', 'FlightNum']

categorical_cols = ['Origin', 'Dest', 'UniqueCarrier']


def getFileSizeInGB(data_dir, file_list=None):
    """
    :param: fileList, a list of paths to file
    :returns: size of the all the files in GB
    """
    if file_list is not None:
        return sum([os.lstat(data_file).st_size
                    for data_file in file_list]) / 1e9


def getFileList(data_dir, file_format):
    return [data_file for data_file in os.listdir(data_dir)
            if data_file.endswith(file_format)]


def readFiles(file_format, data_dir, file_list=None, cols=None):
    if cols is None:
        cols = all_cols

    if file_list is None:
        file_list = getFileList(data_dir)

    if file_format == "csv":
        return pd.concat([pd.read_csv(data_file) for data_file in file_list
                          ]
                         )
    elif file_format == "h5" or file_format == "hdf5":
        return pd.concat([pd.read_hdf(data_file) for data_file in file_list
                          ]
                         )
    else:
        raise ValueError("file format {} is not accepted.".format(file_format))



if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="run IO and preprocessing operations")
    argparser.add_argument("fileformat", metavar="file_format", type=str,
                           help="Acceptable formats and arguments are: \n" +
                           "*.csv\n" +
                           "*.h5\n" +
                           "*.parquet"
                           )



