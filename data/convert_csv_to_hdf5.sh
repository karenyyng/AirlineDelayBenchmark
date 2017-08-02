ls *.csv | xargs -n 1 -P 6 ./convert_csv_to_hdf5.py
