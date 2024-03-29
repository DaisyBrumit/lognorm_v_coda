# PARSING SCRIPT TAKEN FROM AARON YERKE'S BALANCE TREES PROJECT
# Columns follow this pattern:
# qseqid sseqid pident length evalue bitscore score ppos
# 
# 1.	qseqid	 query (e.g., unknown gene) sequence id
# 2.	sseqid	 subject (e.g., reference genome) sequence id
# 3.	pident	 percentage of identical matches
# 4.	length	 alignment length (sequence overlap)
# 5.	evalue	 expect value
# 6.	bitscore	 bit score
# 7.  score     Raw score
# 8.  ppos      Percentage of positive-scoring matches
# Comparison stategy: compare ppos (if tie, go with biggest alignment length)

input_file <- "blast_out.txt"

# init empty df
df <- data.frame(#qseqid=character(),
  sseqid=character(),
  bitscore=integer(),
  count_matched=integer(),
  stringsAsFactors=FALSE)

# read in txt file as r object for efficiency
con <- file(input_file, "r")
while ( TRUE ) {
  line = readLines(con, n = 1)
  if ( length(line) == 0 ) {
    break
  }
  # set values based on guide above
  result = unlist(strsplit(line, '\t'))
  qseq = result[1]
  sseq = unlist(strsplit(result[2],"\\|"))[2] #dbj|AB064923|
  evalue = as.numeric(result[5])
  bitsc = as.integer(result[6])

  # add new rows and record unique vs repeat value counts for later
  if (evalue < 10^-10){
    if ( qseq %in% row.names(df)){
      
      if (bitsc > df[qseq, "bitscore"]){
        count = df[qseq,count_matched]
        df[qseq,] = list(sseq, bitsc, count + 1)
      }
      
    }else{
      newRow <- data.frame(sseqid=sseq,
                           bitscore=bitsc,
                           count_matched=1) 
      row.names(newRow) = qseq
      df = rbind(df, newRow)
    }
  }
}
close(con)

#print helpful sanity checks
print(paste("original nrow:", nrow(df)))
print(paste("number of unique rows:", length(unique(rownames(df)))))

myT <- table(df[,"sseqid"])

print(paste("ave seq/node:", mean(myT), "\nmax seq/node:", max(myT)))

pdf("blastpase.pdf")
hist(myT, breaks = 150, xlab = "Sequences per node tip", main = "Histogram of seqs per node tip")
barplot(myT, las = 2, xlab = "Sequences per node tip", main = "Histogram of seqs per node tip")
dev.off()

write.csv(df, file = "parsed_output.csv")
