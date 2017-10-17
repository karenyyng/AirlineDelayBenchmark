"""
A pipeline for analyzing airline delays data
"""


def main():
    import psutil

    # import matplotlib.pyplot as plt
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import GridSearchCV
    from sklearn.ensemble import RandomForestClassifier
    # from sklearn.preprocessing import StandardScaler
    # from sklearn.naive_bayes import GaussianNB
    from sklearn.preprocessing import Imputer
    from sklearn.externals import joblib
    # from sklearn import metrics
    from category_encoders import BinaryEncoder
    from datetime import datetime

    from sklearn.model_selection import TimeSeriesSplit
    import os
    import numpy as np

    import sys
    sys.path.append("../")
    import serial_preprocess_data as preprocess
    import utils

    cpu_count = int(psutil.cpu_count() / 4) - 2
    print("Trying to use {} number of cpu".format(cpu_count))
    data_dir = "../../data/"
    hdf_files = sorted([data_dir + file for file in os.listdir(data_dir)
                        if '.h5' in file])

    columns = ['Year',
               'Cancelled',
               'Distance',
               'Diverted',
               'ArrTime',
               'Dest',
               'FlightNum',
               # 'DepDelay',  ## not using DepDelay
               'ActualElapsedTime',
               'ArrDelay',
               'DayofMonth',
               'UniqueCarrier',
               'Month',
               'DepTime',
               'Origin',
               'DayOfWeek'
               ]
    scoring = 'roc_auc'
    no_of_files = 12

    df = preprocess.readFilesToDf("h5", file_list=hdf_files[:no_of_files],
                                  cols=columns)

    print("Size of file read in is {0:.2f} GB".format(
          utils.getFileSizeInGB(hdf_files[:no_of_files])))
    print("Reading in {0} selected columns only".format(len(columns)))
    print("Columns are:", columns)
    print("Memory usage of the data frame is {0:.2f} GB".format(
          np.sum(df.memory_usage()) / 1e9))

    # preprocess data check the percentage of nans
    _ = preprocess.find_cardinality_of_categorical_variables(df)

    ix = preprocess.clean_data_minimally(df)
    # apply cleaning of the data
    df = df.iloc[ix].reindex()
    df = df.sort_values(by=['DayofMonth', 'Month', 'Year', 'DepTime'])

    feature_cols = list(df.columns)
    feature_cols.remove('ArrDelay')
    feature_cols.remove('Cancelled')

    df['delayCat'] = df.ArrDelay.apply(
        preprocess.convert_delay_into_multiple_categories)
    df['delayBinaryCat'] = df.ArrDelay.apply(
        preprocess.convert_delay_into_two_categories)
    X = df[feature_cols]
    y = df['delayBinaryCat']

    encoder = BinaryEncoder()
    encoder.fit(X)
    transformed_X = encoder.transform(X)

    print("Transformed columns are ", transformed_X.columns)

    df_gpby = df.groupby('delayCat')
    delay_percentage_breakdown = df_gpby.ArrDelay.count() / df.shape[0] * 100
    delay_percentage_breakdown.index = ['very early',
                                        'early',
                                        'on time',
                                        'late',
                                        'very late'
                                        ]
    print("Percentage breakdown of different categories " +
          "of the target variable is: \n",
          delay_percentage_breakdown)

    # the breakdown of delay is pretty balanced.
    # Although a careful study will also look at the correlation with other
    # other features

    tscv = TimeSeriesSplit()
    # cv_ixes = [(train_ix, test_ix)
    #            for train_ix, test_ix in tscv.split(transformed_X)]

    # only put grid search steps into pipeline
    rf_pipeline_steps = [
        # impute missing feature values with median values
        ("imputer", Imputer(strategy="median")),
        ('rf', RandomForestClassifier(n_jobs=cpu_count, oob_score=True)),
    ]

    gridsearch_parameters = dict([
        ("rf__n_estimators", [800]),
        ("rf__max_features", [None]),  # not many featuers to subset from
    ])

    rf_pipeline = Pipeline(rf_pipeline_steps)

    est = GridSearchCV(rf_pipeline,
                       param_grid=gridsearch_parameters,
                       n_jobs=1,
                       scoring=scoring,
                       cv=tscv.split(X),  # this does 3 fold cross-validation
                       )
    print("Fitting the values")
    print("Columns in the training data are ", X.columns)
    est.fit(transformed_X.values, y.values)
    print("Saving the model")
    print("Best score" + scoring + "is", est.best_score_)
    print("Best parameters are ", est.best_params_)

    datetime_stamp = datetime.now().strftime(
        "%D_%X").replace("/", "_").replace(":", "_")
    joblib.dump(est.best_estimator_,
                "./RF_CV_pipeline_" + datetime_stamp + ".pkl")


if __name__ == "__main__":
    main()
