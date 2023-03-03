# Data Transformations/Normalization Schemes for Compositional Sets
# Code Testing for Aaron Yerke
# Written by Daisy Fry Brumit

# imports as needed
library(ape)
library(phyloseq)
library(compositions)
library(dplyr)

paths <- list("Jones_ForwardReads_DADA2.txt","Noguera-Julian_ForwardReads_DADA2.txt",
              "Zeller_ForwardReads_DADA2.txt","Vangay_ForwardReads_DADA2.txt")

labels <- list('Jones','NJ',"Zeller","Vangay")

for (i in 1:length(paths)) {
  data <- data.frame(read.delim(toString(paths[i]), sep= '\t'))
  zero_counts <- apply(data, 2, function(x) {
    return(sum(x ==0)) }) # per sample, how many zeros counted for each taxon
  # ALR
  D <- which(zero_counts == min(zero_counts))[1] # return name of col with fewest zero counts, denominator for ALR
  alr_out <- as.matrix(compositions::alr(x=as.matrix(data + 1), ivar=D)) # add 1 to table for log functions, use D as denom
  
  # CLR
  clr_out <- as.matrix(compositions::clr(x=as.matrix(data + 1)))
  
  # ILR
  ilr_out <- as.matrix(compositions::ilr(x=as.matrix(data + 1)))
  
  # LOGNORM
  # Dr. Fodor's lognorm
  lognorm <- function(table) {
    avg <- sum(rowSums(table))/nrow(table)
    table <- sweep(table,1,rowSums(table),"/")
    table <- log10(table*avg + 1)
    return(table)
  }
  
  lognorm_out <- lognorm(data)
  
  write.csv(alr_out, paste0(labels[i],"_alr.csv"))
  write.csv(clr_out, paste0(labels[i],"_clr.csv"))
  write.csv(ilr_out, paste0(labels[i],"_ilr.csv"))
  write.csv(lognorm_out, paste0(labels[i],"_lognorm.csv"))
}


