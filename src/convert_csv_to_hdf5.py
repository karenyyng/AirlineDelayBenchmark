#!/usr/bin/env python
"""
This uses Python 3
Does not work on Windows
"""

import pandas as pd

data_path = "../data"
year_range = (1987, 2009)
compression = 'gzip'

for year in range(*year_range):
    filename = data_path + "/" + str(year) + '_' + compression + '.h5'
    print("converting the file {0}/{1}.csv to {2}".format(
        data_path, year, filename))
    df = pd.read_csv(data_path + "/" + str(year) + ".csv",
                     encoding="ISO-8859-1")
    df.to_hdf(filename, key="csv")
