import randForest as rf # reference my randForest.py in same directory
import pandas as pd
import os # for directory walkthrough
from skbio.stats.ordination import pcoa, OrdinationResults

rootdir = '/Users/dfrybrum/lognorm_v_coda/'
studyList = ['Zeller', 'Jones', 'Vangay', 'Noguera-Julian'] # study names, also subdirs for rootdir
transforms = ('alr', 'clr', 'ilr', 'lognorm', 'tss', 'heilinger')

for study in studyList:
    meta = pd.read_table('/Users/dfrybrum/beta_diversity_testing/' + study + '/meta.txt', index_col=0)

    accuracy_df = pd.DataFrame()
    r2_df = pd.DataFrame()
    
    for transform in transforms:
        dat_path = '/Users/dfrybrum/lognorm_v_coda/'+study+'_'+transform+'.csv'
        dat = pd.read_csv(dat_path, index_col=0).T

        print('STUDY: ', study, '\nMETHOD: ', transform)
        catRF = rf.qualitativeRF(meta, dat)
        quantRF = rf.quantitativeRF(meta, dat)

        try:
            # expand dictionary contents
            acc_expand = pd.DataFrame(catRF[0])  # 0 == dictionary w/ accuracy scores to features
            r2_expand = pd.DataFrame(quantRF[0])  # 0 == {r2 scores : features}

            length = len(r2_expand)
            trans_expand = pd.DataFrame({'transform': [transform] * length})

            # append contents to dataframes
            acc_merge = trans_expand.join(acc_expand)
            r2_merge = trans_expand.join(r2_expand)

            accuracy_df = pd.concat([accuracy_df, acc_merge], ignore_index=True)
            r2_df = pd.concat([r2_df, r2_merge], ignore_index=True)
        except:
            pass
        
    accuracy_df.to_csv(rootdir + study + '_accuracy_table.txt', sep='\t', index=False)
    r2_df.to_csv(rootdir + study + '_r2_table.txt', sep='\t', index=False)

print("beam me up, scotty!")