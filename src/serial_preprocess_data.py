"""
Serial version of all the IO and processing steps for a data pipeline
"""
import pandas as pd
import numpy as np
# import pyarrow.parquet as pq
# import logger
import utils


def readFilesToDf(file_format, data_dir=None, file_list=None, cols=None):
    if file_list is None:
        file_list = utils.getFileList(data_dir)

    print("Reading {} files".format(len(file_list))
          )
    if file_format == "csv":
        return pd.concat([pd.read_csv(data_file, usecols=cols)
                          for data_file in file_list
                          ]
                         )
    elif file_format == "h5" or file_format == "hdf5":
        return pd.concat([pd.read_hdf(data_file, columns=cols)
                          for data_file in file_list]
                         )
    else:
        raise ValueError("File format {} is not accepted.".format(file_format))


def clean_data_minimally(df, verbose=True,
                         invalid_values=[("Cancelled", 1.0)]):
    """remove records with nan values for the target variable (ArrDelay)
    and remove canceled flights from the dataframe

    :invalid_values: list of key-value tuple pairs,
        key is the column string in the df,
        value is a certain invalid value.
    :return: the indices of the valid entries in the dataframe

    should actually examine if the invalid values below to a certain
    population
    """
    original_df_size = df.shape[0]
    nan_numbers = np.sum(np.isnan(df.ArrDelay))

    ix = df.ArrDelay.dropna().index

    valid_ixes = np.ones(len(ix))
    for col, invalid_val in invalid_values:
        valid_ixes = np.logical_and(valid_ixes, df.iloc[ix][col] != invalid_val)

    ix = ix[valid_ixes]
    if verbose:
        print("Removed {0:.2f}% of records with NaN in target variable.".format(
            nan_numbers / df.shape[0] * 100))
        print("Removed {0} of additional invalid records which is ".format(
                  original_df_size - df.iloc[ix].shape[0]) +
              "{0:.2f}% of total records".format(
                  (original_df_size - df.iloc[ix].shape[0]) / original_df_size * 100)
              )
    return ix


def find_cardinality_of_categorical_variables(df):
    """
    :return: list of column names for categorical variables
    """
    cat_variables = np.array(df.columns)[~(df.dtypes == np.float64)]
    for cat in cat_variables:
        print("Cardinality of {0} is {1}".format(
            cat, len(df[cat].unique())))
    return list(cat_variables)


def convert_delay_into_multiple_categories(delay):
    """
    >>> delays = np.array([-31, -30, -6, -5, 0, 5, 6, 30, 31])
    >>> [convert_delay_into_multiple_categories(delay)
         for delay in delays]
    """
    if delay >= 30:
        # very late if delay > 30 mins
        return 2
    elif delay <= -30:
        # very early if arrive earlier than 30 min
        return -2
    elif delay >= -5 and delay <= 5:
        # on time if within 5 minutes of scheduled arrival time
        return 0
    elif delay >= 5 and delay < 30:
        # late if later than 5 minutes of scheduled arrival time
        # but not later than 30 minutes of scheduled arrival time
        return 1
    elif delay <= -5 and delay > -30:
        # late if later than 5 minutes of scheduled arrival time
        return -1


def convert_delay_into_two_categories(delay):
    return delay > 5

# if __name__ == "__main__":
#     argparser = argparse.ArgumentParser(
#         description="run IO and preprocessing operations")
#     argparser.add_argument("fileformat", metavar="file_format", type=str,
#                            help="Acceptable formats and arguments are: \n" +
#                            "*.csv\n" +
#                            "*.h5\n" +
#                            "*.parquet"
#                            )
