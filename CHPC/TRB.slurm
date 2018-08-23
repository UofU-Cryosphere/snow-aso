#!/bin/bash

#SBATCH --job-name=u1135435_agisoft
#SBATCH --account=notchpeak-gpu                 # account - abbreviated by -A
#SBATCH --partition=notchpeak-gpu               # partition, abbreviated by -p

#SBATCH --time=24:00:00                         # wall time, abbreviated by -t
#SBATCH --nodes=1                               # number of cluster nodes, abbreviated by -N
#SBATCH --ntasks=32                             # number of requested CPU cores
#SBATCH --mem=0                                 # No limit on memory
#SBATCH --constraint="v100"                     # Request specific feature to select any possible node available with it
#SBATCH --gres=gpu:v100:3                       # Use the GPU on notchpeak, resource_type:resource_name:resource_count
                                                # Each node has 3 GPUs. Recommended to request them all.
#SBATCH --exclusive

#SBATCH --mail-type=FAIL,END                    # Events to send mail out
#SBATCH --mail-user=u1135435@utah.edu           # Email address to sent to

#SBATCH -o slurm-%j.out-%N                      # stdout, using job ID (%j) and the first node (%N)
#SBATCH -e slurm-%j.err-%N                      # stderr, using job and first node

# Enable CPU Hyper-threading
export OMP_NUM_THREADS=$SLURM_NTASKS

# Needed for PDF export in Agisoft using QT
export export QT_QPA_FONTDIR=/usr/share/fonts/open-sans

PROJECT_NAME='TE_20180528'

module load photoscan
photoscan.sh -platform offscreen \
             -r $HOME/snow-aso/CHPC/agisoft_workflow.py \
             --base-path $HOME/scratch/$PROJECT_NAME \
             --project-name $PROJECT_NAME \
             --dense-cloud-quality medium \
             > $HOME/scratch/$PROJECT_NAME.log
