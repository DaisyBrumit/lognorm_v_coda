import pandas as pd
import numpy as np

studyList = ['Jones', 'Vangay', 'Noguera-Julian', 'Zeller'] # study names, also subdirs for rootdir

for study in studyList:

    data_path = '/Users/dfrybrum/beta_diversity_testing/' + study + '/' + study + '_ForwardReads_DADA2.txt'
    data = pd.read_table(data_path, index_col=0, header=0).T

    zero_counts = np.sum(data == 0, axis=0)


print('beam me up, Scotty!')