
# coding: utf-8

# In[1]:

get_ipython().magic('matplotlib inline')


# In[2]:

get_ipython().magic('load_ext autoreload')


# In[3]:

get_ipython().magic('autoreload 2')


# In[4]:

import psutil


# In[5]:

import gc


# In[6]:

import sklearn


# In[7]:

import matplotlib.pyplot as plt


# In[8]:

from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler,     LabelEncoder,     LabelBinarizer
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import Imputer
from sklearn import metrics 
from sklearn.ensemble import VotingClassifier
from category_encoders import BinaryEncoder


# In[9]:

from sklearn.model_selection import TimeSeriesSplit


# In[10]:

sklearn.__version__


# In[11]:

import pandas as pd
import numpy as np 
import os
import sys
import h5py


# In[12]:

# cpu_count = int(psutil.cpu_count() / 6)


# In[13]:

cpu_count = 8


# In[14]:

import sys
sys.path.append("../")
import serial_preprocess_data as preprocess


# In[15]:

data_dir = "../../data/"


# In[16]:

hdf_files = sorted([data_dir + file for file in os.listdir(data_dir) 
                    if '.h5' in file])


# pick out unique columns from the data. There are not that many relevant features for use. 

# In[17]:

columns = ['Year',
        'Cancelled',
        'Distance',
        'Diverted',
        'ArrTime',
        'Dest',
        'FlightNum',
        'DepDelay',
        'ActualElapsedTime',
        'ArrDelay',
        'DayofMonth',
        'UniqueCarrier',
        'Month',
        'DepTime',
        'Origin',
        'DayOfWeek'
        ]


# In[18]:

no_of_files = 12


# In[19]:

get_ipython().system('echo $OMP_NUM_THREADS')


# In[20]:

get_ipython().magic('time df = preprocess.readFilesToDf("h5", file_list=hdf_files[:no_of_files], cols=columns)')


# In[21]:

preprocess.getFileSizeInGB(hdf_files[:no_of_files])


# In[22]:

df.dtypes


# # preprocess data

# check the percentage of nans 

# In[23]:

def clean_data_minimally(df, verbose=True):
    """remove records with nan values for the target variable (ArrDelay)
    and remove canceled flights from the dataframe
    
    :return: the indices of the valid entries in the dataframe 
    """
    original_df_size = df.shape[0]
    nan_numbers = np.sum(np.isnan(df.ArrDelay)) 
    
    ix = df.ArrDelay.dropna().index
    not_canceled_ix = df.iloc[ix].Cancelled != 1.0
    ix = ix[not_canceled_ix]
    if verbose: 
        print("nan percentage is {0:.2f}".format(
            nan_numbers / df.shape[0] * 100))
        print("removed {} of entries".format(
            original_df_size - df.iloc[ix].shape[0]))
    return ix 


# In[24]:

len(df.Dest.unique())


# In[25]:

df


# In[26]:

def find_cardinality_of_categorical_variables(df):
    """
    :return: list of column names for categorical variables 
    """
    cat_variables = np.array(df.columns)[~(df.dtypes == np.float64)]
    for cat in cat_variables:
        print("Cardinality of {0} is {1}".format(
            cat, len(df[cat].unique())))
    return list(cat_variables)


# In[27]:

cat_variables = find_cardinality_of_categorical_variables(df)


# In[28]:

cat_variables


# In[29]:

ix = clean_data_minimally(df)


# In[30]:

df.iloc[ix].Cancelled.describe()


# In[31]:

df = df.iloc[ix].reindex()


# In[32]:

_ = plt.hist(df.ArrDelay, bins=100, range=(-500, 500))
plt.xlabel("Delay (in min)")
plt.ylabel("No. of flights")


# In[33]:

df = df.sort_values(by=['DayofMonth', 'Month', 'Year', 'DepTime'])


# In[34]:

feature_cols = list(df.columns)
feature_cols.remove('ArrDelay')


# In[35]:

def convert_delay_into_multiple_categories(delay):
    if delay >= 30: 
        # very late if delay > 30 mins 
        return 2
    elif delay <= -30: 
        # very early if arrive earlier than 30 min
        return -2 
    elif delay >= -5 and delay <= 5:
         # on time if within 5 minutes of scheduled arrival time 
        return 0
    elif delay >= 5 and delay < 30:
        # late if later than 5 minutes of scheduled arrival time
        # but not later than 30 minutes of scheduled arrival time
        return 1 
    elif delay <= -5 and delay > -30:
        # late if later than 5 minutes of scheduled arrival time
        return -1


# In[36]:

def convert_delay_into_two_categories(delay):
    return delay > 5


# In[37]:

delays = np.array([-31, -30, -6, -5, 0, 5, 6, 30, 31])


# In[38]:

cat_variables


# In[39]:

df['delayCat'] = df.ArrDelay.apply(convert_delay_into_multiple_categories)


# In[40]:

df['delayBinaryCat'] = df.ArrDelay.apply(convert_delay_into_two_categories)
X = df[feature_cols]
y = df['delayBinaryCat']


# In[41]:

encoder = BinaryEncoder()


# In[42]:

get_ipython().magic('time encoder.fit(X)')


# In[43]:

X.shape


# In[44]:

get_ipython().magic('time transformed_X = encoder.transform(X)')


# In[45]:

transformed_X


# In[46]:

len(transformed_X.columns)


# In[47]:

df_gpby = df.groupby('delayCat')


# In[48]:

delay_percentage_breakdown = df_gpby.ArrDelay.count() / df.shape[0] * 100


# In[49]:

delay_percentage_breakdown.index = ['very early', 
                                    'early',
                                    'on time',
                                    'late',
                                    'very late'
                                   ]


# In[50]:

delay_percentage_breakdown


# the breakdown of delay is pretty balanced. Although a careful study will also look at the correlation with other features and the 

# In[51]:

tscv = TimeSeriesSplit()


# In[52]:

cv_ixes = [(train_ix, test_ix) 
           for train_ix, test_ix in tscv.split(transformed_X)]


# only put grid search steps into pipeline

# In[53]:

rf_pipeline_steps = [
    # impute missing feature values with median values 
    ("imputer", Imputer(strategy="median")),  
    ('rf', RandomForestClassifier()),
]

gridsearch_parameters = dict([
    ("rf__n_estimators", [500, 1000]),
    ("rf__max_features", [None, 'auto']),  # not many featuers to subset from
])


# In[54]:

rf_pipeline = Pipeline(rf_pipeline_steps)


# In[55]:

est = GridSearchCV(rf_pipeline,
             param_grid=gridsearch_parameters,
             n_jobs=cpu_count, 
             # use accuracy for scoring for comparing to another benchmark
             scoring=None,  
             cv=tscv.split(X),
            )


# In[ ]:

get_ipython().magic('time stuff = est.fit(transformed_X.values, y.values)')


# In[ ]:



