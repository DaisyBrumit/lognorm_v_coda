#!/bin/bash
#SBATCH --partition=Orion
#SBATCH --nodes=1
#SBATCH --mem=120GB
#SBATCH --job-name=silvaBlast
#SBATCH --time=200:00:00

module load blast

blast/2.11.0+
makeblastdb -in Silva/Silva_forBlast_noDups.fasta -parse_seqids -dbtype nucl
