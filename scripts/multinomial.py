import sys
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.linear_model import LogisticRegression

def metaFilter(data, meta):
    # are any meta columns void of data?
    empty_cols = meta.columns[meta.isnull().all()]
    meta.drop(empty_cols, axis=1, inplace=True)

    # are any meta columns void of differing data?
    singleValue_cols = meta.columns[meta.nunique() == 1]
    meta.drop(singleValue_cols, axis=1, inplace=True)

    # only keep shared samples, but don't merge
    filtered_meta = meta[meta.index.isin(data.index)]
    filtered_data = data[data.index.isin(meta.index)]

    return [filtered_data, filtered_meta]
def preML_filter(table, column):
    # drop all rows with no data
    noNull_table = table.dropna(axis=0, how='any')

    # drop rows with unique values
    unique_values = table[column].value_counts() == 1
    rowFiltered_table = noNull_table[~noNull_table[column].isin(unique_values[unique_values].index)]

    # check that the table has more than 2 values
    if len(rowFiltered_table) <= 2:
        return 0
    else:
        return rowFiltered_table

# take in args from command line % read metadata
study = 'Vangay'#sys.argv[1]
meta = pd.read_table('~/beta_diversity_testing/'+study+'/meta.txt', index_col=0)#pd.read_table('/users/dfrybrum/fodor_lab/beta_diversity_testing/' + study + '/meta.txt', index_col=0)

# initiate empy df
accuracy_df = pd.DataFrame()

# perform tasks for all transforms
#transforms = ['alr', 'ilr', 'clr', 'tss', 'lognorm', 'heilinger']
transforms = ['alr', 'ilr', 'clr', 'tss', 'lognorm', 'heilinger']
for transform in transforms:
    outDict={}
    dat = pd.read_csv('~/lognorm_v_coda/'+study+'/'+transform+'.csv',index_col=0)#pd.read_table('/users/dfrybrum/fodor_lab/lognorm_v_coda/' + study + '/' + transform + '.csv', index_col=0).T

    dat, meta = metaFilter(dat, meta)  # None specifies index join. Inner b/c only want full matches
    table = meta.join(dat, how='inner')
    for column in meta.columns:
        print(column)
        # join meta and full data
        full_table = preML_filter(table, column)

        if type(full_table) == int:
            print("Not enough post-filter data in ", column, "to proceed. Skipping.")
            pass
        elif full_table[column].dtype != 'object':
            print("Quant column. Skipping.")
            pass
        else:
            X = full_table.loc[:, ~full_table.columns.isin(meta.columns)]
            y = full_table.loc[:, full_table.columns.isin(meta.columns)]

            model = LogisticRegression(multi_class='multinomial', solver='lbfgs', penalty='l2', max_iter=800)
            cv = RepeatedStratifiedKFold(n_splits=2, n_repeats=2, random_state=1)

            # evaluate the model
            try:
                scores = cross_val_score(model, X, y[column], scoring='accuracy', cv=cv)
                outDict[column] = scores
            except Exception as e:
                outDict[column] = '999'
                print(e)

    acc_expand = pd.DataFrame.from_dict(outDict)
    acc_expand = acc_expand.assign(transform=transform)
    accuracy_df = pd.concat([accuracy_df, acc_expand], ignore_index=True)

accuracy_df.to_csv('/Users/dfrybrum/lognorm_v_coda/'+study+'/multinomial_accuracy.txt', sep='\t', index=False)
#accuracy_df.to_csv('/users/dfrybrum/fodor_lab/lognorm_v_coda/' + study + '/multinomial_accuracy.txt', sep='\t',
                   #index=False)