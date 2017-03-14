#!/usr/bin/env python

import pandas as pd

data_path = "../data"
year_range = (1987, 2009)

# for year in range(2000, 2009):
for year in range(*year_range):
    print("converting the file {0}/{1}.csv to {0}/{1}.h5".format(data_path, year) )
    df = pd.read_csv(data_path + "/" + str(year) + ".csv", encoding="ISO-8859-1")
    df.to_hdf(data_path + "/" + str(year) + ".h5", key="csv")
