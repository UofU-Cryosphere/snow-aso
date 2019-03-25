#!/bin/bash

#SBATCH --job-name=agisoft
#SBATCH --account=owner-gpu-guest
#SBATCH --partition=notchpeak-gpu-guest
#SBATCH --qos=photoscan

#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --mem=0                                 
#SBATCH --exclusive

#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=u1135435@utah.edu

#SBATCH -o slurm-%j.out-%N                      # stdout, using job ID (%j) and the first node (%N)
#SBATCH -e slurm-%j.err-%N                      # stderr, using job and first node

