#!/usr/bin/env python
"""
This uses Python 3
Does not work on Windows
"""

import pandas as pd

data_path = "../data"
year_range = (1987, 2009)
compression = None

for year in range(*year_range):
    if compression is None:
        filename = data_path + "/" + str(year) + '.h5'
    else:
        filename = data_path + "/" + str(year) + '_' + compression + '.h5'

    print("converting the file {0}/{1}.csv.bz2 to {2}".format(
        data_path, year, filename))
    df = pd.read_csv(data_path + "/" + str(year) + ".csv.bz2",
                     encoding="ISO-8859-1")
    df.to_hdf(filename, key="csv", format='table', complib=compression)
