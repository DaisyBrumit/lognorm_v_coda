import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.linear_model import LogisticRegression

transforms = ('alr', 'clr', 'ilr', 'lognorm', 'tss', 'hielinger')
#studies = ('Jones', 'Zeller', 'Vangay', 'Noguera-Julian')
studies = ('Zeller', 'Vangay')

def multiReg(dat, meta):
    outDict = {}
    for column in meta.columns:
        # join meta and full data
        full_table = meta.join(dat, how='inner', on=None)  # None specifies index join. Inner b/c only want full matches
        full_table = full_table.dropna(subset=[column])

        X = full_table.loc[:, ~full_table.columns.isin(meta.columns)]
        y = full_table.loc[:, full_table.columns.isin(meta.columns)]

        model = LogisticRegression(multi_class='multinomial', solver='lbfgs', penalty='l2', max_iter=200)
        cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=2, random_state=1)
        # evaluate the model
        try:
            scores = cross_val_score(model, X, y[column], scoring='accuracy', cv=cv)
            outDict[column] = scores
        except:
            outDict[column] = '999'

    return outDict

for transform in transforms:
    accuracy_df = pd.DataFrame()

    for study in studies:
        # read in data per study
        dat_path = '/Users/dfrybrum/lognorm_v_coda/'+study+'_'+transform+'.csv'
        meta_path = '/Users/dfrybrum/beta_diversity_testing/'+study+'/meta.txt'
        dat = pd.read_csv(dat_path, index_col=0).T
        meta = pd.read_table(meta_path, index_col=0)

        # get reg output and save as df
        regOut = pd.DataFrame.from_dict(multiReg(dat,meta))
        regOut['study'] = study

        # append new values to main df
        accuracy_df = accuracy_df.append(regOut)

    accuracy_df.to_csv('/Users/dfrybrum/lognorm_v_coda/' + transform + 'accuracy.csv')  # categorical files