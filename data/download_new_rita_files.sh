#!/usr/bin/bash
# requires: unzip, wget  
# we download the raw data from 
# https://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time

n_process=6
cat ./rita_file_paths.txt | xargs -n 1 -P $n_process wget 
ls *.zip | xargs -n 1 -P $n_process unzip
rm *.zip 
python rename_files.py
