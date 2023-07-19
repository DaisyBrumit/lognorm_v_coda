import randForest as rf # reference my randForest.py in same directory
import pandas as pd
import os # for directory walkthrough
from skbio.stats.ordination import pcoa, OrdinationResults

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

rootdir = '/Users/dfrybrum/lognorm_v_coda/'
studyList = ['Jones', 'Vangay', 'Noguera-Julian'] # study names, also subdirs for rootdir
transforms = ('alr', 'clr', 'ilr', 'lognorm', 'tss', 'heilinger')

for study in studyList:
    meta = pd.read_table('/Users/dfrybrum/beta_diversity_testing/' + study + '/meta.txt', index_col=0)
    #if study == "Vangay":
        #meta = meta.drop('host_subject_id', axis=1)

    accuracy_df = pd.DataFrame()
    r2_df = pd.DataFrame()
    
    for transform in transforms:
        dat_path = '/Users/dfrybrum/lognorm_v_coda/'+study+'/'+transform+'.csv'
        dat = pd.read_csv(dat_path, index_col=0)
        dat, meta = metaFilter(dat, meta)  # None specifies index join. Inner b/c only want full matches

        print('STUDY: ', study, '\nMETHOD: ', transform)
        #catRF = rf.qualitativeRF(meta, dat)
        quantRF = rf.quantitativeRF(meta, dat)

        # expand dictionary contents
        #acc_expand = pd.DataFrame(catRF[0])  # 0 == dictionary w/ accuracy scores to features
        r2_expand = pd.DataFrame(quantRF)  # 0 == {r2 scores : features}

        length = len(r2_expand)
        trans_expand = pd.DataFrame({'transform': [transform] * length})

        # append contents to dataframes
        #acc_merge = trans_expand.join(acc_expand)
        r2_merge = trans_expand.join(r2_expand)

        #accuracy_df = pd.concat([accuracy_df, acc_merge], ignore_index=True)
        r2_df = pd.concat([r2_df, r2_merge], ignore_index=True)
        
    #accuracy_df.to_csv(rootdir + study + '/' + study + '_accuracy_table.txt', sep='\t', index=False)
    r2_df.to_csv(rootdir + study + '_r2_table.txt', sep='\t', index=False)

print("beam me up, scotty!")