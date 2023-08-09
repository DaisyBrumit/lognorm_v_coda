# ADAPTED FROM AARON YERKE'S BALANCE TREE PROJECT
if (!requireNamespace("BiocManager", quietly = TRUE)){
  install.packages("BiocManager")
  BiocManager::install("phyloseq")
  BiocManager::install("philr")
  BiocManager::install("ape")
}
library(philr)

con <- file('silva_ref_phyloseq.robj')
ps <- readRDS(con)
ps <- transform_sample_counts(ps, function(x) x+1)

##-Test for reqs----------------------------------------------------##
print("rooted tree?")
is.rooted(phy_tree(ps)) # Is the tree Rooted?
print('All multichotomies resolved?')
is.binary.tree(phy_tree(ps)) # All multichotomies resolved?

## ---- message=FALSE, warning=FALSE-----------------------------------------
phy_tree(ps) <- ape::makeNodeLabel(phy_tree(ps), method="number", prefix='n')

##-philr transform--------------------------------------------------##
ps.philr <- philr(ps@otu_table, ps@phy_tree,
                  part.weights='enorm.x.gm.counts',
                  ilr.weights='blw.sqrt')

write.table(ps.philr, file.path('filtered_philr.csv'),sep = ",",row.names = TRUE, col.names = FALSE)
