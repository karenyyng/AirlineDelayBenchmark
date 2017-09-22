# import numpy as np
import pandas as pd
import time
import sys
sys.path.append("../")

# import scripts that Karen wrote
# import serial_preprocess_data as preprocess
import utils
data_dir = "../../data/"
subset = 64
h5list = sorted(utils.getFileList(data_dir, "h5"))

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
start_time = time.time()
df = pd.concat([pd.read_hdf(h5file, columns=columns)
                for h5file in h5list[:subset]])
end_time = time.time()
print("Read and concat df took {0:.0f} s".format(end_time - start_time))
