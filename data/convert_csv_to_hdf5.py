#!/usr/bin/env python
"""
This uses Python 3
Does not work on Windows
"""

import pandas as pd
import sys

if len(sys.argv) < 2:
    raise ValueError("Please supply one argument as the file path")
csvfile = sys.argv[1]
compression = None

prefix = csvfile.split('.')[0]
if compression is None:
    filename = prefix + '.h5'
else:
    filename = prefix + '_' + compression + '.h5'

print("converting the file {0} to {1}".format(csvfile, filename))
df = pd.read_csv(csvfile, encoding="ISO-8859-1", low_memory=False)
df.to_hdf(filename, key="csv", format='table', complib=compression)
