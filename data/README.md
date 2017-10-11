# how to download the data
```
source download_new_rita_files.sh  
source convert csv_to_hdf5.sh
```

# how to verify that the data that you download and converted are secure and complete
```
md5checksum *.h5 > ./downloaded_md5checksum
diff ./md5checksum ./downloaded_md5checksum 
```
there should not be any difference between the two files  
