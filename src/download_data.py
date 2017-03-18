#!/usr/bin/env python
"""
Script for downloading data from RITA
"""
from urllib.request import urlretrieve
import os


dataDir = "../data"
if not os.path.exists(dataDir):
    os.mkdir(dataDir)
year_range = (1987, 2009)

for year in range(*year_range):  # 2009
    print ("range of years of files to download = ", year_range)
    print ("downloading data from year {0} to {1}/{0}.csv.bz2".format(
        year, dataDir
    ))
    urlretrieve(
        "http://stat-computing.org/dataexpo/2009/" + str(year) + ".csv.bz2",
        dataDir + "/" + str(year) + ".csv.bz2")
