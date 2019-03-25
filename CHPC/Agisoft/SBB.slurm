#!/bin/bash

#SBATCH --job-name=agisoft
#SBATCH --account=notchpeak-gpu
#SBATCH --partition=notchpeak-gpu
#SBATCH --qos=photoscan

#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --mem=0
#SBATCH --constraint="v100"
#SBATCH --gres=gpu:v100:3

#SBATCH --exclusive

#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=u1135435@utah.edu

#SBATCH -o slurm-%j.out-%N
#SBATCH -e slurm-%j.err-%N

# Enable CPU Hyper-threading
export OMP_NUM_THREADS=$SLURM_NTASKS

# Needed for PDF export in Agisoft using QT
export QT_QPA_FONTDIR=/usr/share/fonts/open-sans

PROJECT_NAME='SB_20170221'

module load photoscan
metashape.sh -platform offscreen \
             -r $HOME/snow-aso/CHPC/Agisoft/agisoft_workflow.py \
             --base-path $HOME/scratch/$PROJECT_NAME \
             --project-name $PROJECT_NAME \
             > $HOME/scratch/$PROJECT_NAME.log
