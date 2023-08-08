#!/bin/bash
#SBATCH --partition=Orion
#SBATCH --nodes=1
#SBATCH --mem=120GB
#SBATCH --time=200:00:00

module load blast/2.9.0+

study=$1
echo "starting blast for ${study}"

blastn -query ~/fodor_lab/lognorm_v_coda/${study}/dada2seqs.fasta \
  -db  Silva/Silva_forBlast_noDups.fasta\
  -out ${study}/blast_out.txt \
  -outfmt "6 qseqid sseqid pident length evalue bitscore score ppos"

echo "Beam me up, Scotty!"
