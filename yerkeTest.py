
# Imports
import pandas as pd
import numpy as np
from skbio.stats import composition
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score

## RANDOM FOREST FOR CATEGORICAL INPUT
def categoricalRF(metadata, dat):
    # join meta and full data
    full_table = metadata.join(dat, how='inner', on=None)  # None specifies index join. Inner b/c only want full matches

    # set test and train groups
    X = full_table.loc[:, ~full_table.columns.isin(metadata.columns)]
    y = full_table.loc[:, full_table.columns.isin(metadata.columns)]
    y_cat = y.select_dtypes(include=['object'])

    outDict = {}
    for column in y_cat.columns:
        X_train, X_test, y_train, y_test = train_test_split(X, y[column], test_size=0.25, train_size=0.75,
                                                            random_state=1)

        ## train the classifier for CATEGORICAL input
        randForest = RandomForestClassifier(n_estimators=50, random_state=1)
        randForest.fit(X_train, y_train)
        y_predict = randForest.predict(X_test)
        accuracy = accuracy_score(y_test, y_predict)
        outDict[column] = accuracy

    return outDict


# Establish sets for testing
pathList = ['Daisy_16S/Jones_ForwardReads_DADA2.txt', 'Daisy_16S/Vangay_ForwardReads_DADA2.txt','Daisy_16S/Zeller_ForwardReads_DADA2.txt']

# load in set, generate zero sums
#df = pd.read_table(pathList[0])
df = pd.read_table('/Users/dfrybrum/Documents/FodorLab/gemelli/Jones/Jones_ForwardReads_DADA2.txt')

#df_sub = df.iloc[:,0:50]
count_list = []

for col_name in df.columns:
    column = df[col_name]
    count_list.append((column == 0).sum())
zero_counts = pd.DataFrame(data=count_list, index=df.columns)

# Transformations
## A/C/I-LR
name = pd.DataFrame(zero_counts.idxmin()).iloc[0,0]
table = df+1

alr_out = pd.DataFrame(composition.alr(table)).set_index(keys=table.index)
clr_out = pd.DataFrame(composition.clr(table)).set_index(keys=table.index)
ilr_out = pd.DataFrame(composition.ilr(table)).set_index(keys=table.index)

## lognorm
avg = sum(table.mean(0))
# ^^ avg same output as math.fsum(table.sum())/len(table.index)
# where math.fsum is used for float summation

rowSums = table.sum(0)
logOut = table.divide(rowSums)
logOut = np.log10(logOut*avg + 1)

# import metadata for RF
meta = pd.read_csv('/Users/dfrybrum/Documents/FodorLab/gemelli/Jones/jones_meta.csv')
meta = meta.set_index(keys=meta['Run'])
meta = meta.drop(['Run'], axis=1) # for Jones dataset

alr_cat_results = categoricalRF(meta, alr_out)
clr_cat_results = categoricalRF(meta, clr_out)
ilr_cat_results = categoricalRF(meta, ilr_out)
log_cat_results = categoricalRF(meta, logOut)

dictList = [alr_cat_results, clr_cat_results, ilr_cat_results, log_cat_results]
indexKeys = np.array(['alr','clr','ilr','log'])
accuracy_table = pd.DataFrame.from_dict(dictList)

print("Beam me up, Scotty!")
