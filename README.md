# lognorm_v_coda
testing space for transformation comparison paper

## yerkeTest.py
This R script contains basic code for implementing alr, clr, ilr, and our lognorm transformation

Running this script with provided data is slwo because R loads directly to memory.

**Input**
One DADA2 asv count table (per study)

**Output**
4 .csv files (per study): one table per approach

## yerkeTest.py
This python script contains a workflow for transforming asv counts via alr, clr, ilr, and our lab's lognorm, running these sets indpendently through sklearn's `RandomForestRegressor` and `RandomForestClassifier`. The former is run when quantitative responses from metadata are used as a dependent variable, and the Classifier is used when responses are categorical. R^2 and accuracy scores are recorded for each transformation, for each response in the metadata, and a dictonary is created to store results for comparing approaches. 

##Input##
One DADA2 file per study
One metadata file per study (source of response variables in Random Forest)

##Output##
Four .csv files (per study): one table per approach
Two .csv files (per study): one table for each performance metric (R^2 and accuracy) 
