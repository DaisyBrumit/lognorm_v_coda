library(ape)
# LOAD IN SILVA TREE BUILD BLAST DB
tree <- ape::read.tree("SilvaReferenceTree_newick.txt")

# for loop from Aaron's lib/cml_scripts/creat_ref_tree_blst_db/p1_download_seqs.R
for (i in 1:length(tree$tip.label)){
  lab <- tree$tip.label[i]
  id <- strsplit(lab, "_")[[1]][1]
  id <- gsub('^.', '', id)
  tryCatch(
    {myGen = ape::read.GenBank(id, as.character=T, species.names = FALSE)
    myDna = lapply(myGen, function(x) paste0(x, collapse = ''))
    cat(paste0(">", id, "\n", paste0(myDna), "\n"), file = '~/Silva_forBlast.fasta', append=TRUE)
    }, error = function(cond) {message("Encountered a specific error:", cond)}
    )
  Sys.sleep(.45)
}
