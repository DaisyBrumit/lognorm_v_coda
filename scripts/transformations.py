import pandas as pd
import numpy as np
import composition_stats

studyList = ['Jones', 'Zeller', 'Vangay', 'Noguera-Julian']

for study in studyList:
    meta_path = '/Users/dfrybrum/beta_diversity_testing/'+study+'/meta.txt'
    data_path = '/Users/dfrybrum/beta_diversity_testing/'+study+'/'+study+'_ForwardReads_DADA2.txt'

    meta = pd.read_table(meta_path, index_col=0)
    data = pd.read_table(data_path, index_col=0, header=0).T
    dataCols = data.columns
    data_asNumpy = data.to_numpy()

    # set the alr denominator to be the column with fewest zero counts
    zero_counts = np.sum(data == 0, axis=0)
    denominator = np.argmin(zero_counts)

    # perform transformations
    alr = composition_stats.alr(data_asNumpy+1, denominator)
    clr = composition_stats.clr(data_asNumpy+1)
    ilr = composition_stats.ilr(data_asNumpy+1)

    colnames_alr = dataCols[dataCols!=dataCols[denominator]]
    colnames_ilr = dataCols[dataCols!=dataCols[0]]

    alr_out = pd.DataFrame(alr, columns=colnames_alr, index=data.index)
    clr_out = pd.DataFrame(clr, columns=dataCols, index=data.index)
    ilr_out = pd.DataFrame(ilr, columns=colnames_ilr, index=data.index)

    alr_out.to_csv('/Users/dfrybrum/lognorm_v_coda/' + study + '/alr.csv')
    clr_out.to_csv('/Users/dfrybrum/lognorm_v_coda/' + study + '/clr.csv')
    ilr_out.to_csv('/Users/dfrybrum/lognorm_v_coda/' + study + '/ilr.csv')

