# FILTER OUT COLUMNS WITH MORE THAN 90% ZEROS 
# IN KEEPING WITH SAME METHOD USED BY AARON YERKE
# INPUT: DADA2 TABLE
# OUTPUT: FILTERED DADA2 TABLE


library(tidyverse)

study.list <- c('Zeller', 'Jones', 'Noguera-Julian', 'Vangay')
genPath.in <- '~/beta_diversity_testing/'
genPath.out <- '~/lognorm_v_coda/'

for (study in study.list) {
  
  in_path <- paste0(genPath.in,study,'/',study,'_ForwardReads_DADA2.txt') # set path for original DADA2
  setwd(paste0(genPath.out,study))
  
  raw.table <- read.table(in_path, header=TRUE, row.names = 1)
  
  # FILTER SEQUENCES WITH 90% THRESHOLD 
  # LONG WAY TO CHECK SANITY
  zero.row <- as.data.frame(rowSums(raw.table == 0))
  zero.row <- zero.row / ncol(raw.table)
  zero.row <- zero.row %>% filter(`rowSums(raw.table == 0)` < 0.9)
  rows.to.keep <- rownames(zero.row)
  
  # A MUCH MORE EFFICIENT METHOD, WILL BE TRANSPOSED
  # df1 <- as.data.frame(t(raw.table))
  # df2 <- df1[,sapply(df1, function(x) mean(x == 0) < 0.9)]
  
  rowfiltered.table <- raw.table %>% filter(row.names(.) %in% rows.to.keep) %>% rownames_to_column(var='rownames')
  write_tsv(rowfiltered.table, 'rowFiltered90_DADA2.txt')
}
