
# Imports
import pandas as pd
import numpy as np
from skbio.stats import composition
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Establish sets for testing
pathList = ['Daisy_16S/Jones_ForwardReads_DADA2.txt', 'Daisy_16S/Vangay_ForwardReads_DADA2.txt','Daisy_16S/Zeller_ForwardReads_DADA2.txt']

# load in set, generate zero sums
#df = pd.read_table(pathList[0])
df = pd.read_table('/Users/dfrybrum/Documents/FodorLab/gemelli/Jones/Jones_ForwardReads_DADA2.txt')

df_sub = df.iloc[:,0:50]
count_list = []

for col_name in df_sub.columns:
    column = df_sub[col_name]
    count_list.append((column == 0).sum())
zero_counts = pd.DataFrame(data=count_list, index=df_sub.columns)

# Transformations
## A/C/I-LR
name = pd.DataFrame(zero_counts.idxmin()).iloc[0,0]
table = df_sub+1

print("MIN ZERO_COUNT\n", name)
alr_out = composition.alr(table)
clr_out = composition.clr(table)
ilr_out = composition.ilr(table)

## lognorm
avg = sum(table.mean(0))
# ^^ avg same output as math.fsum(table.sum())/len(table.index)
# where math.fsum is used for float summation

rowSums = table.sum(0)
logOut = table.divide(rowSums)
logOut = np.log10(logOut*avg + 1)

# import metadata for RF
meta = pd.read_csv('/Users/dfrybrum/Documents/FodorLab/gemelli/Jones/jones_meta.csv')
meta_sub = meta[meta.iloc[:,0].isin(table.index)]
meta_sub.set_index(keys=meta_sub['Run'], drop=True)
## sanity check
if len(meta_sub.index) != len(table.index): print("Metadata and table data do not include same sample count!")
else: print("Metadata/data sample check passed")

# Random Forest

print("Beam me up, Scotty!")
