# Github repo

[link](http://github.com/karenyyng/AirlineDelayBenchmark)

# This is a non-trivial benchmark for a classification problem 
[Data source for year between 1987-2003](http://stat-computing.org/dataexpo/2009/the-data.html)    
[Metadata source](http://stat-computing.org/dataexpo/2009/supplemental-data.html)   

# Files 
```
|
+---_config  : contains set up script for Intel Python 
+---_src     : contains python scripts for processing the data 
|		+---read_csv_and_print_stat.py runs within 2 mins
+---_results : benchmark results
+---_doc     : other documentation 
+---_data
```

# One-time setup 
Go to `config` and `source install_py35_env.sh`` for installing Intel Python to your home directoy 

# Subsequent use
`source ./config/load_py35_env.sh`
suggestions for improving the settings are welcomed. 


# Credits
Thanks to Duncan Temple Lang who first showed me the dataset.
Please also see his book `XML and Web Technologes for Data Science with R`.
for another use of the same dataset.
