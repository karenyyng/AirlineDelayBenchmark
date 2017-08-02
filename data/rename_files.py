#!/bin/python
import os
for file in os.listdir("."):
    if '.csv' in file and "On_Time" in file:
        new_name = '_'.join(file.split("_")[5:])
        print("renaming " + new_name)
        os.rename(file, new_name)
