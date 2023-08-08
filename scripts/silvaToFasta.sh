#!/bin/bash
#SBATCH --partition=Orion
#SBATCH --nodes=1
#SBATCH --mem=64GB
#SBATCH --time=200:00:00
#SBATCH --job-name=sFasta

cd ..

module load R

Rscript silvaToFasta.R --no-save

echo "Beam me up, Scotty!"
