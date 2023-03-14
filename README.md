# lognorm_v_coda
testing space for transformation comparison paper

## yerkeTest.R
This R script contains basic code for implementing alr, clr, ilr, and our lognorm transformation

Running this script with provided data is slow because R loads directly to memory.

**Input**

- 1 DADA2 asv count table (per study)

**Output**

- 4 .csv files (per study): one table per approach

## yerkeTest.py
This python script contains a workflow for transforming asv counts via alr, clr, ilr, and our lab's lognorm, running these sets indpendently through sklearn's `RandomForestRegressor` and `RandomForestClassifier`. The former is run when quantitative responses from metadata are used as a dependent variable, and the Classifier is used when responses are categorical. R^2 and accuracy scores are recorded for each transformation, for each response in the metadata, and a dictonary is created to store results for comparing approaches. 

**Input**

- 1 DADA2 file per study
- 1 metadata file per study (source of response variables in Random Forest)

**Output**

- 4 .csv files (per study): one table per approach
- 2 .csv files (per study): one table for each performance metric (R^2 and accuracy) 

#### A Personal Note:

Aaron's .R script used for reference when building my .py adaptation of Fodor's lognorm transformation can be found [here](https://github.com/palomnyk/balance_tree_exploration/blob/1420324b5c7a6c94cd95836835dca3e27f4d70db/lib/table_manipulations.R) or by following his repo to path `balance_tree_exploration/lib/table_manipulations.R`
