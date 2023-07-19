import pandas as pd
import numpy as np
from skbio.stats import composition
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.metrics import r2_score

## RANDOM FOREST FOR CATEGORICAL INPUT
def categoricalRF(metadata, dat):
    #get cat data
    meta_cat = metadata.select_dtypes(include=['object'])

    # run RF for w/ each categorical column as 'y'
    outDict = {}
    for column in meta_cat.columns:
        # join meta and full data
        full_table = meta_cat.join(dat, how='inner', on=None)  # None specifies index join. Inner b/c only want full matches
        full_table = full_table.dropna(subset=[column])

        # set test and train groups
        X = full_table.loc[:, ~full_table.columns.isin(meta_cat.columns)]
        y = full_table.loc[:, full_table.columns.isin(meta_cat.columns)]

        accuracyList = []
        for i in range(0,100):
            try:
                X_train, X_test, y_train, y_test = train_test_split(X, y[column], test_size=0.25, train_size=0.75)
            
                # train the classifier and get an accuracy score
                randForest = RandomForestClassifier()
                randForest.fit(X_train, y_train)
                y_predict = randForest.predict(X_test)
                accuracy = accuracy_score(y_test, y_predict)
                accuracyList.append(accuracy)
            
            except Exception as e:
                print("ERROR IN COLUMN ", column, " RUN ", i)
                print(repr(e))
                pass

        outDict[column] = accuracyList

    return outDict

def quantitativeRF(metadata, dat):
    #get cat data
    meta_quant = metadata.select_dtypes(include=['float64'])

    # run RF for w/ each quantitative column as 'y'
    outDict = {}
    for column in meta_quant.columns:
        # join meta and full data
        full_table = meta_quant.join(dat, how='inner', on=None)  # None specifies index join. Inner b/c only want full matches
        full_table = full_table.dropna(subset=[column])

        # set test and train groups
        X = full_table.loc[:, ~full_table.columns.isin(meta_quant.columns)]
        y = full_table.loc[:, full_table.columns.isin(meta_quant.columns)]

        r2List = []
        for i in range(0,100):

            try:
                X_train, X_test, y_train, y_test = train_test_split(X, y[column], test_size=0.25, train_size=0.75)

            # train the classifier and get an accuracy score
                randForest = RandomForestRegressor()
                randForest.fit(X_train, y_train)
                y_predict = randForest.predict(X_test)
                R2 = r2_score(y_test, y_predict)
                r2List.append(R2)

            except Exception as e:
                print("ERROR IN COLUMN ", column, " RUN ", i)
                print(repr(e))
                pass

            outDict[column] = r2List



    return outDict

transforms = ('alr', 'clr', 'ilr', 'lognorm', 'tss', 'heilinger')
studies = ('Jones', 'Zeller', 'Vangay', 'Noguera-Julian')

for transform in transforms:
    accuracy_df = pd.DataFrame()
    r2_df = pd.DataFrame()

    for study in studies:
        # read in data per study
        dat_path = '/Users/dfrybrum/lognorm_v_coda/'+study+'_'+transform+'.csv'
        meta_path = '/Users/dfrybrum/beta_diversity_testing/'+study+'/meta.txt'
        dat = pd.read_csv(dat_path, index_col=0).T
        meta = pd.read_table(meta_path, index_col=0)

        # get RF output and save as df
        catRF = pd.DataFrame(categoricalRF(meta, dat))
        quantRF = pd.DataFrame(quantitativeRF(meta, dat))

        # append new values to main df
        accuracy_df = accuracy_df.append(catRF)
        r2_df = r2_df.append(quantRF)

    accuracy_df.to_csv('/Users/dfrybrum/lognorm_v_coda/' + transform + 'accuracy_0.csv')  # categorical files
    r2_df.to_csv('/Users/dfrybrum/lognorm_v_coda/' + transform + 'r2_0.csv')



