# Imports
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
            X_train, X_test, y_train, y_test = train_test_split(X, y[column], test_size=0.25, train_size=0.75)

            # train the classifier and get an accuracy score
            randForest = RandomForestClassifier()
            randForest.fit(X_train, y_train)
            y_predict = randForest.predict(X_test)
            accuracy = accuracy_score(y_test, y_predict)
            accuracyList.append(accuracy)

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

        accuracyList = []
        for i in range(0,100):

            X_train, X_test, y_train, y_test = train_test_split(X, y[column], test_size=0.25, train_size=0.75)

            # train the classifier and get an accuracy score
            randForest = RandomForestRegressor()
            randForest.fit(X_train, y_train)
            y_predict = randForest.predict(X_test)
            R2 = r2_score(y_test, y_predict)
            accuracyList.append(R2)

        outDict[column] = accuracyList

    return outDict
## RANDOM FOREST FOR CATEGORICAL INPUT

# load in set, generate zero sums
#df = pd.read_table(pathList[0])
df = pd.read_table('Daisy_16S/Jones_ForwardReads_DADA2.txt')

#df_sub = df.iloc[:,0:50]
count_list = []

for col_name in df.columns:
    column = df[col_name]
    count_list.append((column == 0).sum())
zero_counts = pd.DataFrame(data=count_list, index=df.columns)

# import metadata for RF
meta = pd.read_csv('meta/Jones_meta.csv')
meta = meta.set_index(keys=meta['Run']) # Jones
meta = meta.drop(['Run'], axis=1) # for Jones dataset

# Transformations
## A/C/I-LR
name = pd.DataFrame(zero_counts.idxmin()).iloc[0,0]
table = df+1

alr_out = pd.DataFrame(composition.alr(table)).set_index(keys=table.index)
clr_out = pd.DataFrame(composition.clr(table)).set_index(keys=table.index)
ilr_out = pd.DataFrame(composition.ilr(table)).set_index(keys=table.index)

alr_out.to_csv('out/Jones_alr.csv')
clr_out.to_csv('out/Jones_clr.csv')
ilr_out.to_csv('out/Jones_ilr.csv')

## lognorm
avg = sum(table.mean(0))
# ^^ avg same output as math.fsum(table.sum())/len(table.index)
# where math.fsum is used for float summation

rowSums = table.sum(0)
logOut = table.divide(rowSums)
logOut = np.log10(logOut*avg + 1)
logOut.to_csv('out/Jones_logOut.csv')

# implement categorical Rand Forest per approach
alr_cat_results = categoricalRF(meta, alr_out)
clr_cat_results = categoricalRF(meta, clr_out)
ilr_cat_results = categoricalRF(meta, ilr_out)
log_cat_results = categoricalRF(meta, logOut)

alr_RF_out = alr_RandForest_results = pd.DataFrame.from_dict(alr_cat_results).to_csv('out/Jones_alr_RF_Results_100run.csv')
clr_RF_out = clr_RandForest_results = pd.DataFrame.from_dict(clr_cat_results).to_csv('out/Jones_clr_RF_Results_100run.csv')
ilr_RF_out = alr_RandForest_results = pd.DataFrame.from_dict(ilr_cat_results).to_csv('out/Jones_ilr_RF_Results_100run.csv')
log_RF_out = log_RandForest_results = pd.DataFrame.from_dict(log_cat_results).to_csv('out/Jones_log_RF_Results_100run.csv')
dictList = [alr_cat_results, clr_cat_results, ilr_cat_results, log_cat_results]

alr_quant_results = quantitativeRF(meta, alr_out)
clr_quant_results = quantitativeRF(meta, clr_out)
ilr_quant_results = quantitativeRF(meta, ilr_out)
log_quant_results = quantitativeRF(meta, logOut)
dictList = [alr_quant_results, clr_quant_results, ilr_quant_results, log_quant_results]

alr_RF_out = alr_RandForest_results = pd.DataFrame.from_dict(alr_quant_results).to_csv('out/Jones_alr_RFquant_Results_100run.csv')
clr_RF_out = clr_RandForest_results = pd.DataFrame.from_dict(clr_quant_results).to_csv('out/Jones_clr_RFquant_Results_100run.csv')
ilr_RF_out = alr_RandForest_results = pd.DataFrame.from_dict(ilr_quant_results).to_csv('out/Jones_ilr_RFquant_Results_100run.csv')
log_RF_out = log_RandForest_results = pd.DataFrame.from_dict(log_quant_results).to_csv('out/Jones_log_RFquant_Results_100run.csv')

#indexKeys = np.array(['alr','clr','ilr','log'])
#accuracy_table = pd.DataFrame.from_dict(dictList)
#accuracy_table = accuracy_table.set_index(indexKeys)
#accuracy_table.to_csv('~/Documents/FodorLab/out/Jones_RandForest_CatAcc.csv') # categorical files

print("Beam me up, Scotty!")

