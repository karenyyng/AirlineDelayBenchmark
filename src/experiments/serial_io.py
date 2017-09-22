# import numpy as np
import pandas as pd
import time

# import scripts that Karen wrote
# import serial_preprocess_data as preprocess
import utils

h5list = utils.getFileList("../data/", "h5")

columns = ['Year',
           'Cancelled',
           'Distance',
           'Diverted',
           'ArrTime',
           'Dest',
           'FlightNum',
           # 'DepDelay',  ## not using DepDelay
           'ActualElapsedTime',
           'ArrDelay',
           'DayofMonth',
           'UniqueCarrier',
           'Month',
           'DepTime',
           'Origin',
           'DayOfWeek'
           ]
rank = 20
start_time = time.time()
df = pd.concat([pd.read_hdf("../data/" + h5file, columns=columns)
                for h5file in h5list])
end_time = time.time()
print("Read and concat df took {0:.0f} s".format(end_time - start_time))
