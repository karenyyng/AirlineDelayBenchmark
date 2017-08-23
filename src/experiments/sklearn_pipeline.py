
import psutil

import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder, LabelBinarizer
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import Imputer
from sklearn import metrics
from sklearn.ensemble import VotingClassifier
from category_encoders import BinaryEncoder


from sklearn.model_selection import TimeSeriesSplit
import pandas as pd
import numpy as np
import os
import sys
import h5py



# cpu_count = int(psutil.cpu_count() / 6)
cpu_count = 8
import sys
sys.path.append("../")
import serial_preprocess_data as preprocess

data_dir = "../../data/"
hdf_files = sorted([data_dir + file for file in os.listdir(data_dir)
                    if '.h5' in file])

# pick out unique columns from the data. There are not that many relevant features for use.
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

no_of_files = 12
os.system('echo $OMP_NUM_THREADS')

df = preprocess.readFilesToDf("h5", file_list=hdf_files[:no_of_files],
                              cols=columns)'

preprocess.getFileSizeInGB(hdf_files[:no_of_files])

df.dtypes


# # preprocess data
# check the percentage of nans

cat_variables = find_cardinality_of_categorical_variables(df)

ix = clean_data_minimally(df)
# apply cleaning of the data
df = df.iloc[ix].reindex()


df = df.sort_values(by=['DayofMonth', 'Month', 'Year', 'DepTime'])

feature_cols = list(df.columns)
feature_cols.remove('ArrDelay')


df['delayCat'] = df.ArrDelay.apply(convert_delay_into_multiple_categories)
df['delayBinaryCat'] = df.ArrDelay.apply(convert_delay_into_two_categories)
X = df[feature_cols]
y = df['delayBinaryCat']

encoder.fit(X)
transformed_X = encoder.transform(X)


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



