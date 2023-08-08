
# IMPORTS
if (!require("BiocManager", quietly = TRUE))
  install.packages("BiocManager")

BiocManager::install("phyloseq")

library(phyloseq)
library(tidyverse)
library(ape)

# LIST ALL STUDIES AND SET PATHS
study.list <- c('Zeller', 'Jones', 'Noguera-Julian', 'Vangay')
genPath.in <- '~/beta_diversity_testing/'
genPath.out <- '~/lognorm_v_coda/'

for (study in study.list) {
  # READ IN METADATA AND SET INDICES
  meta <- readr::read_tsv(paste0(genPath.in,study,'/meta.txt'))
  meta <- as.data.frame(meta)
  row.names(meta) <- meta$sampleid
  meta <- dplyr::select(meta, !sampleid)
  
  # READ IN DATA AND SET INDICES
  df <- readr::read_tsv(paste0(genPath.in,study,'/',study,'_ForwardReads_DADA2.txt'))
  df <- as.data.frame(df)
  row.names(df) <- df[[1]]
  df <-df %>% dplyr::select(-1)
  df<- t(df)
  
  # READ IN PREMADE SILVA TREE
  tree <- ape::read.tree(paste0(genPath.out,'viFy10M5J2nvIBpCLM-QMQ_newick.txt'))
  
  # READ IN BLAST OUTPUT FROR CURRENT STUDY
  tree_key <- read.table(paste0(genPath.out,study,"/parsed_output.csv"),
                         sep = ",",
                         row.names = 1,
                         header = T)
  
  # INIT FOR SEQ (MIS)MATCHES/LABELS
  match_df <- data.frame(
    seqs=character(),
    num_seqs=integer(),
    stringsAsFactors=FALSE)
  
  unmatched_ids <- c()
  
  new_labels <- c()
  
  # FOR EVERY TIP ON THE TREE...
  for (i in 1:length(tree$tip.label)){
    
    # grab slixe out of og labels 
    old_lab = gsub("'", "", tree$tip.label[i]) 
    id = unlist(strsplit(old_lab, "_"))[1]
    if (substr(id, 1, 1) == '\'') {id <- gsub('^.', '', id)}
    
    # check if that label is in the k=blast output
    if (id %in% tree_key$sseqid){
      
      # make new label
      index = which(tree_key$sseqid == id)[1]
      new_lab = row.names(tree_key)[index]
      tree$tip.label[i] = new_lab
      
      # count duplicates
      if (id %in% row.names(match_df)){
        print("in if")
        seqs = match_df[id,"seqs"]
        count = match_df[id,"num_seqs"]
        new_seqs = paste(seqs, new_lab)
        match_df[id,"seqs"] = new_seqs
        match_df[id,"num_seqs"] = count + 1
      }
      
      # record novel labels
      else{
        new_row = data.frame(
          seqs=new_lab,
          num_seqs=1,
          stringsAsFactors=FALSE)
        row.names(new_row) = c(id)
        match_df = rbind(match_df, new_row)
      }
    }
    
    # note unmatched labels
    else{
      unmatched_ids = c(unmatched_ids, id)
    }
  }
  
  # print sanity checks
  print(paste("unmatched ids:", length(unmatched_ids)))
  print(paste("num tree tips pre pruning:", length(tree$tip.label)))
  
  # make a new filtered tree
  tree <- phyloseq::prune_taxa(row.names(tree_key), tree)
  
  # more sanity checks
  print(paste("num tree tip.label post pruning:", length(tree$tip.label)))
  
  pdf(file = 'plotted_reduced_tree.pdf')
  phyloseq::plot_tree(tree, nodelabf=nodeplotblank, label.tips="taxa_names", ladderize="left")
  dev.off()
  
  print(paste("num duplicated tips:", sum(duplicated(tree$tip.label))))
  print(paste("duplicated tips:", tree$tip.label[duplicated(tree$tip.label)]))
  
  # remove straggling duplicate labels
  if( sum(duplicated(tree$tip.label)) > 0){
    print("removing duplicated tip")
    tree <- ape::drop.tip(tree, tree$tip.label[duplicated(tree$tip.label)], trim.internal = TRUE, subtree = FALSE,
                          root.edge = 0, rooted = is.rooted(tree), collapse.singles = TRUE,
                          interactive = FALSE)
  }

  # bundle new tree, otu table, and metadata as a phyloseq object for easy use in philr transform
  ps <- phyloseq::phyloseq(otu_table(df, taxa_are_rows=FALSE),
                           sample_data(meta),
                           phy_tree(tree))

  saveRDS(ps, file = paste0(genPath.out,study,'/silva_ref_phyloseq.robj'))
}
