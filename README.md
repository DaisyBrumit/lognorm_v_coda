# lognorm_v_coda
testing space for transformation comparison paper

## Data Manipulations and Transforms

### filter_90pct.py
Takes in provided DADA2 forward read tables from another project directory (this is just where I store them in general) and filters out all sequences that are present in less than 10% of samples. 

### transforms_*
These scripts all transform the provided abundance tables using whichever methods are listed after the first underscore in the file. The only transformation that requires additional handling before running is `transforms_philr.R`.

## Prepping philr Data
To run philr, we have to make a tree that corresponds to each study. To do this we make fasta files from the study and reference data, create a blast DB, and perform a blast search against the aforementioned DB. After the search we parse the results and filter the reference tree using the matching labels from our search. This study-specific filtered tree is packaged with the original abundance data and corresponding metadada into a phyloseq object and then transformed using philr. 

### To Fasta!
`DADA_to_fasta.py` and `silvaToFasta.*` create fasta files for downstream blastn searches using the original (or filtered) abundance tables or Silva reference tree, respectively. 

### Running blastn
`make_silvaDB.sh` creates a database from the Silva referece for the sebsequent blastn search. This is conducted in `studyBlast.sh`. The results are parsed in `parse_blast.R`. 

### Make the tree
Tree filtering is conducted in `make_ref_tree.R` and all relevant data is packaged as a phyloseq object for use in `transforms_philr.R`

## Machine Learning 
Random forest is conducted through data handling & file creation in `ch.py`, which sends data to supporting file `randForest.py` for actual regression and classification. 

Multinomial regression is conducted entirely within the `multinomial.py` file. 

All output is summarized within `summary_figure_recreation.R`. 

## A Note on Data Storage
Scripts are stored within this github repo. Scripts stored on Charlotte's HPC research cluster are not to be trusted for the most up-to-date scripts and may not be appropriate for use in recreation. *This github repo is where final scripts are stored.* The cluster houses all of the tables and files that are in/output by these scripts due to storage limits on GitHub. That is to say *all non-scripting files associated with this testing repo should be accessible via Charlotte's HPC research cluster as of 9 August 2023.*

## A Personal Note:

Aaron's .R script used for reference when building my .py adaptation of Fodor's lognorm transformation can be found [here](https://github.com/palomnyk/balance_tree_exploration/blob/1420324b5c7a6c94cd95836835dca3e27f4d70db/lib/table_manipulations.R) or by following his repo to path `balance_tree_exploration/lib/table_manipulations.R`
