
# Imports
import pandas as pd
import numpy as np
from skbio.stats import composition

# Establish sets for testing
pathList = ['C:/Users/Perry/Documents/fodor_lab/Daisy_16S/Daisy_16S/Jones_ForwardReads_DADA2.txt', 'C:/Users/Perry/Documents/fodor_lab/Daisy_16S/Daisy_16S/Vangay_ForwardReads_DADA2.txt','C:/Users/Perry/Documents/fodor_lab/Daisy_16S/Daisy_16S/Zeller_ForwardReads_DADA2.txt']

# load in set, generate zero sums
df = pd.read_table(pathList[0])
df_sub = df.iloc[:,0:50]
count_list = []

for col_name in df_sub.columns:
    column = df_sub[col_name]
    count_list.append((column == 0).sum())
zero_counts = pd.DataFrame(data=count_list, index=df_sub.columns)

# Transformations
## ALR
D = zero_counts.idxmin().to_numpy
table = df_sub.to_numpy

# Random Forest
