# COMPLETE RANDOM FOREST RUNS ON ALL BETA DIVERSITY METRICS
# IN ACCORDANCE WITH BETA_DIVERSITY_ANALYSIS PROJECT
# AUTHORED BY: DAISY FRY BRUMIT

# Imports
import os
import pandas as pd
import numpy as np
#from skbio.stats import composition
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.metrics import r2_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

# RANDOM FOREST FOR CATEGORICAL METADATA

def qualitativeRF(metadata,dat):
    meta_cat = metadata.select_dtypes(include=['object'])

    # make empty dictionaries for column-wide metrics
    accuracyDict = {}

    # join metadata and full data
    full_table = meta_cat.join(dat, how='left', on=None) # None specifies index join. Inner b/c we only want full matches

    # run RF for w/ each categorical column as 'y'
    for column in meta_cat.columns:
        print("CAT COLUMN: ", column) #, "\nPRE-FILTER Y VALUE COUNTS: ", dict(full_table[column].value_counts()))
        # remove na values from full table FOR THIS COLUMN ONLY
        #full_table = full_table.dropna(subset=[column])
        full_table = full_table.dropna(axis=0, how='any', subset=[column])
        full_table = full_table.dropna(axis=0, how='any', subset=dat.columns)

        # set test and training groups
        x = full_table.loc[:, ~full_table.columns.isin(meta_cat.columns)]  # ~ is a negation operator. Isolate non-meta columns for x
        y = full_table[column]  # Isolate desired metadata column for y
        #print('POST-FILTER Y VALUE COUNTS: ', dict(full_table[column].value_counts()))
        # check that categorical values occur more than once so training can proceed
        if 1 not in dict(y.value_counts()).values():
            if x.shape[0] > 4:
                # perform random forest 100 times with 0.25, 0.75 test train split
                accuracyList = []
                rocList = []
                run = 1  # for the ^^ dictionary keys

                for i in range(0, 10):
                    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, train_size=0.75)

                    # train the classifier, predict y values on test data
                    randForest = RandomForestClassifier()
                    randForest.fit(x_train, y_train)
                    y_predict = randForest.predict(x_test) # predicts classes, good for accuracy and interpretation

                    # generate performance metrics and save
                    accuracy = accuracy_score(y_test, y_predict)

                    # append performance metrics to list
                    accuracyList.append(accuracy)
                    run += 1

                # package performance metrics in a list for output
                accuracyDict[column] = accuracyList
            else:
                print("insufficient data post filter")
                pass
        else:
            pass
            print('insufficient unique values')

    outList = [accuracyDict]
    return outList

# RANDOM FOREST FOR QUANTITATIVE METADATA

def quantitativeRF(metadata, dat):
    # get cat data
    meta_quant = metadata.select_dtypes(include=['float64', 'int64'])

    # make empty dictionaries for column-wide metrics
    r2Dict = {}

    for column in meta_quant.columns:
        print("QUANT COLUMN: ", column)
        # run RF for w/ each quantitative column as 'y'
        r2List = []

        # join meta and full data
        full_table = meta_quant.join(dat, how='inner', on=None)  # None specifies index join. Inner b/c only want full matches
        full_table = full_table.dropna(subset=[column])

        # set test and train groups
        X = full_table.loc[:, ~full_table.columns.isin(meta_quant.columns)]
        y = full_table.loc[:, full_table.columns.isin(meta_quant.columns)]
        
        if X.shape[0] > 4:
            for i in range(0, 100):
                x_train, x_test, y_train, y_test = train_test_split(X, y[column], test_size=0.25, train_size=0.75)
    
                # train the classifier and predict y values
                randForest = RandomForestRegressor()
                randForest.fit(x_train, y_train)
                y_predict = randForest.predict(x_test) # predicts classes, good for R2 and interpretation
    
                # generate performance metrics and save
                R2 = r2_score(y_test, y_predict)
                if (R2 > 1):
                    print("INVALID R2")
                r2List.append(R2)
    
                # package performance metrics in a list for output
                r2Dict[column] = r2List
        else:
            print("insufficient data post filter")
            pass
            
    outList = [r2Dict] #, rocDict, truefalse_aggregates]
    return outList


