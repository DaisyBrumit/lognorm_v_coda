# Data Transformations/Normalization Schemes for Compositional Sets
# Code Testing for Aaron Yerke
# Written by Daisy Fry Brumit

# imports as needed
library(ape)
library(phyloseq)
library(compositions)
library(dplyr)

table <- data.frame(read.delim('Jones_ForwardReads_DADA2.txt', sep= '\t'))
tsub <- table %>% select(1:100)


zero_counts <- apply(table, 2, function(x) {
  return(sum(x ==0)) }) # per sample, how many zeros counted for each taxon
# ALR
D <- which(zero_counts == min(zero_counts))[1] # return name of col with fewest zero counts, denominator for ALR
alr_out <- as.matrix(compositions::alr(x=as.matrix(table + 1), ivar=D)) # add 1 to table for log functions, use D as denom

# CLR
clr_out <- as.matrix(compositions::clr(x=as.matrix(table + 1)))

# ILR
ilr_out <- as.matrix(compositions::ilr(x=as.matrix(table + 1)))

# LOGNORM
# Dr. Fodor's lognorm
lognorm <- function(table) {
  avg <- sum(rowSums(table))/nrow(table)
  table <- sweep(table,1,rowSums(table),"/")
  table <- log10(table*avg + 1)
  return(table)
}

lognorm_out <- lognorm(table)
