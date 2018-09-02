#!/bin/bash

#SBATCH --job-name=u1135435_agisoft
#SBATCH --account=owner-gpu-guest
#SBATCH --partition=notchpeak-gpu-guest

#SBATCH --time=24:00:00                         # wall time
#SBATCH --nodes=1                               # number of cluster nodes
#SBATCH --ntasks=32                             # number of requested CPU cores
#SBATCH --mem=0                                 
#SBATCH --constraint="titanv"                   # notch055 has four Titan V GPUs
#SBATCH --gres=gpu:titanv:4                     
#SBATCH --exclusive

#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=u1135435@utah.edu           # Email address for events

#SBATCH -o slurm-%j.out-%N                      # stdout, using job ID (%j) and the first node (%N)
#SBATCH -e slurm-%j.err-%N                      # stderr, using job and first node

# Enable CPU Hyper-threading
export OMP_NUM_THREADS=$SLURM_NTASKS

# Needed for PDF export in Agisoft using QT
export export QT_QPA_FONTDIR=/usr/share/fonts/open-sans

PROJECT_NAME='CB_20180524'

module load photoscan
photoscan.sh -platform offscreen \
             -r $HOME/snow-aso/CHPC/agisoft_workflow.py \
             --base-path $HOME/scratch/$PROJECT_NAME \
             --project-name $PROJECT_NAME \
             > $HOME/scratch/$PROJECT_NAME.log
