#!/bin/bash

#SBATCH --job-name=u1135435
#SBATCH --account=owner-gpu-guest
#SBATCH --partition=kingspeak-gpu-guest

#SBATCH --time=36:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=28
#SBATCH --mem=0
#SBATCH -w kp361

#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=u1135435@utah.edu           # Email address for events

#SBATCH -o slurm-%j.out-%N                      # stdout, using job ID (%j) and the first node (%N)
#SBATCH -e slurm-%j.err-%N                      # stderr, using job and first node

