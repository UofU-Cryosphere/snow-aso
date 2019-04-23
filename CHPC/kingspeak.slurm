#!/bin/bash

#SBATCH --job-name=my_job
#SBATCH --account=kingspeak-gpu
#SBATCH --partition=kingspeak-gpu

#SBATCH --time=36:00:00
#SBATCH --ntasks=12
#SBATCH --mem=0
#SBATCH -w kp297
#SBATCH --constraint="titanx"
#SBATCH --gres=gpu:titanx:8

#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=u1135435@utah.edu

#SBATCH -o slurm-%j.out-%N                      # stdout, using job ID (%j) and the first node (%N)
#SBATCH -e slurm-%j.err-%N                      # stderr, using job and first node

