# imports as needed
library(ape)
library(compositions)
library(dplyr)


study.list <- c('Zeller', 'Jones', 'Noguera-Julian', 'Vangay')
genPath.in <- '~/beta_diversity_testing/'
genPath.out <- '~/lognorm_v_coda/'

for (study in studies)
{
  data <- read.table(paste0(genPath.in, study,'/',study,'_ForwardReads_DADA2.txt'), sep='\t', header=TRUE, row.names = 1) # read in dada2 out
  data <- as.data.frame(t(data))
  
  zero_counts <- apply(data, 2, function(x) 
    {
    return(sum(x ==0)) 
    }) # per sample, how many zeros counted for each taxon
  
  # LOGNORM
  # Dr. Fodor's lognorm
  lognorm <- function(table) 
  {
    avg <- sum(rowSums(table))/nrow(table)
    table <- sweep(table,1,rowSums(table),"/")
    table <- log10(table*avg + 1)
    return(table)
  }
  
  lognorm_out <- lognorm(data) # fodor's lognorm
  tss_out <- sweep(data,1,rowSums(data),"/") # simple proportions
  heilinger_out <- sqrt(sweep(data,1,rowSums(data),"/")) # heilinger transform
  
  write.csv(lognorm_out, paste0(genPath.out,study,"/lognorm.csv"))
  write.csv(tss_out, paste0(genPath.out,study,"/tss.csv"))
  write.csv(heilinger_out, paste0(genPath.out,study,"/heilinger.csv"))
}

