#!/bin/env python
"""
Script for downloading data from RITA
"""
from __future__ import print_function
from urllib import urlretrieve
import os


dataDir = "../data"
if not os.path.exists(dataDir):
    os.mkdir(dataDir)

for year in range(1987, 2009):  # 2009
    print ("downloading data from year {0} to {1}/{0}.csv.bz2".format(
        year, dataDir
    ))
    urlretrieve(
        "http://stat-computing.org/dataexpo/2009/" + str(year) + ".csv.bz2",
        dataDir + "/" + str(year) + ".csv.bz2")
