# Github repo

[link](http://github.intel.com/karenyin/AirlineDelayBenchmark)

# Data source of the airline delay data
[Data source for year between 1987-2003](http://stat-computing.org/dataexpo/2009/the-data.html)    
[Metadata source](http://stat-computing.org/dataexpo/2009/supplemental-data.html)   

# Goals
This is a non-trivial benchmark with (> 12 GB of data) to compare 
the predictive performance, timing, memory usage and __scalability__

* between various machine learning & deep learning algorithms 
* between the same algorithm implemented in different frameworks and languages

We understand similar examples have been performed before, such as
[1](https://github.com/szilard/benchm-ml),
[2](http://www.springer.com/us/book/9781461478997) and 
[3](https://jcrist.github.io/dask-sklearn-part-3.html)
We do not claim to have the original idea but wish to provide a completely
reproducible, realistic example to showcase the best practises for benchmarking ML code.
The main goal is provide an assessment of the amount of compute resources
needed to process a certain amount of data.
The benchmark is also not meant to be completely comprehensive due to the large possible configuration space. 
We pick a few algorithms that are popular and the author is familiar with.
We encourage others to contribute their own implementations in a
__reproducible__ way for comparisons.

We hope to illustrate:

1. realistic data preprocessing steps
2. a few best practises for unit testing and benchmarking machine learning code in Python 
3. best practises to allow a reproducible ML software stack to be setup on different machines 
4. how to setup Intel optimized ML libraries for the best performances or help push for more performance

To achieve those goals, We perform the following tasks:

1. classification of whether a flight is delayed or not 
	* - [ ] Boosting from 
		- [ ] `XGBoost`
		- [ ] `PyDAAL`
	* - [ ] Random Forest from 
		- [ ] `Scikit-Learn`
		- [ ] `Spark ML` 
	* - [ ] SVM with non-linear kernel from (linear kernel is almost the same as Logistic regression)
		- [ ] `Scikit-Learn`
		- [ ] `Spark ML` 
	* - [ ] Logistic regression from `Scikit-learn` for baseline comparison
		- [ ] `Scikit-Learn`
		- [ ] `Spark ML` 
	* - [ ] an appropriate neural network topology, possibly a deep feed forward network 

2. regression of how long a flight is delayed for (within the delayed population) 
	* - [ ] Boosting from `XGBoost` 
	* - [ ] Random Forest 
		- [ ] `Scikit-Learn`
		- [ ] `Spark ML` 
	* - [ ] Linear regression from `Scikit-learn` for baseline comparison
	* - [ ] an appropriate neural network topology, possibly a deep feed forward network 


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
Go to `config` and `source install_py35_env.sh` for installing Intel Python to your home directory.
Other possible dependencies 

We plan to make the list of software that we use available as 
- [x] a Conda environment `yaml` list within `config`
- [ ] a Dockerfile / Docker image for the best setup instructions 

# Subsequent use of code after the one-time software setup
Email [Karen](mailto:karen.y.ng@intel.com) for suggestions for improving the setups. Thanks. 

# notes about data 
Processing `2003.csv.bz2` gives a warning message during ETL.
```
sys:1: DtypeWarning: Columns (22) have mixed types. Specify dtype option on
import or set low_memory=False.
```

# Restoring the original environment
`$ source ./config/unload_ipy35_env.sh`
This restores the PATH variable to the original state.

# Credits
Thanks to Duncan Temple Lang who first showed me the dataset.
Please also see his book `XML and Web Technologes for Data Science with R`.
for another use of a dataset from the same source.
