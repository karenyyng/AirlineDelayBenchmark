#!/usr/bin/bash

### if you only use n_process = 8 and you have 16 files, 
# only 8 of them will be processed with this script...
n_process=6
cat ./rita_file_paths.txt | xargs -n 1 -P $n_process wget 
