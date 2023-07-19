# Data Transformations/Normalization Schemes for Compositional Sets
# Code Testing for Aaron Yerke
# Written by Daisy Fry Brumit

# imports as needed
library(ape)
#library(phyloseq)
library(compositions)
library(dplyr)

path <- '/Users/dfrybrum/beta_diversity_testing/'

studies <- c('Jones', 'Zeller', 'Vangay', 'Noguera-Julian')

for (study in studies)
{
  data <- read.table(paste0(path,study,'/',study,'_ForwardReads_DADA2.txt'), sep='\t', header=TRUE, row.names = 1) # read in dada2 out
  data <- as.data.frame(t(data))
  
  zero_counts <- apply(data, 2, function(x) 
    {
    return(sum(x ==0)) 
    }) # per sample, how many zeros counted for each taxon
  
  # ALR
  #D <- which(zero_counts == min(zero_counts))[1] # return name of col with fewest zero counts, denominator for ALR
  #alr_out <- as.matrix(compositions::alr(x=as.matrix(data + 1), ivar=D)) # add 1 to table for log functions, use D as denom
  
  # CLR
  #clr_out <- as.matrix(compositions::clr(x=as.matrix(data + 1)))
  
  # ILR
  #ilr_out <- as.matrix(compositions::ilr(x=as.matrix(data + 1)))
  #colnames(ilr_out) <- colnames(data)
  
  # LOGNORM
  # Dr. Fodor's lognorm
  lognorm <- function(table) 
  {
    avg <- sum(rowSums(table))/nrow(table)
    table <- sweep(table,1,rowSums(table),"/")
    table <- log10(table*avg + 1)
    return(table)
  }
  
  lognorm_out <- lognorm(data)
  tss_out <- sweep(data,1,rowSums(data),"/")
  hielinger_out <- sqrt(sweep(data,1,rowSums(data),"/"))
  
  #write.csv(alr_out, paste0('/Users/dfrybrum/lognorm_v_coda',study,"/alr.csv"))
  #write.csv(clr_out, paste0('/Users/dfrybrum/lognorm_v_coda/',study,"/clr.csv"))
  #write.csv(ilr_out, paste0('/Users/dfrybrum/lognorm_v_coda/',study,"/ilr.csv"))
  write.csv(lognorm_out, paste0('/Users/dfrybrum/lognorm_v_coda/',study,"/lognorm.csv"))
  write.csv(tss_out, paste0('/Users/dfrybrum/lognorm_v_coda/',study,"/tss.csv"))
  write.csv(hielinger_out, paste0('/Users/dfrybrum/lognorm_v_coda/',study,"/heilinger.csv"))
}

