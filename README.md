# Github repo

[link](http://github.intel.com/karenyin/AirlineDelayBenchmark)

# Data source of the Airline delay data
[Data source for year between 1987-2003](http://stat-computing.org/dataexpo/2009/the-data.html)    
[Metadata source](http://stat-computing.org/dataexpo/2009/supplemental-data.html)   

# Goals
This is a non-trivial benchmark to compare 
the predictive performance, timing and memory usage 

* between various machine learning & deep learning algorithms 
* between the same algorithm implemented in different frameworks and languages

The benchmark is not meant to be completely comprehensive due to the large possible configuration space . 
We encourage others to contribute their own implementations.

We hope to illustrate 
1. a few best practises for unit testing machine learning code.  
2. how to setup Intel optimized libraries for the best performances or help push for more performance

To achieve those goals, We perform the following tasks:

1. classification of whether a flight is delayed or not 
	* Boosting from `XGBoost`
	* Random Forest form `Scikit-Learn`
	* Logistic regression from `Scikit-learn` from baseline
2. regression of how long a flight is delayed for 

And we will explore if we can find any natural clusters (subpopulation) that are present in the dataset.

# Target hardware 
* one node of server class Xeon (Haswell / Broadwell), and / or  
* Xeon Phi (KNL) 

# Files 
```
.
|
+---_config  : contains set up script for Intel Python 
+---_src     : contains python scripts for processing the data 
|   +---read_csv_and_print_stat.py runs within 2 mins
+---_results : benchmark results
+---_doc     : other documentation 
+---_data
+---_benchmark : code for benchmarking
```

# One-time software setup 
Go to `config` and `source install_py35_env.sh`` for installing Intel Python to your home directory.
We plan to make the list of software that we use available as 
- [ ] a Conda environment list  
- [ ] possibly a Dockerfile / Docker image 


# Subsequent use of code after the one-time software setup
`$ source ./config/load_py35_env.sh`
Email [Karen](mailto:karen.y.ng@intel.com) for suggestions for improving the setups. Thanks. 


# Credits
Thanks to Duncan Temple Lang who first showed me the dataset.
Please also see his book `XML and Web Technologes for Data Science with R`.
for another use of a dataset from the same source.
