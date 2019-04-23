#!/bin/bash

#SBATCH --job-name=agisoft
#SBATCH --account=owner-gpu-guest
#SBATCH --partition=notchpeak-gpu-guest
#SBATCH --qos=photoscan

#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --mem=0
#SBATCH --constraint="2080ti"                   # notch083 and 084 have four RTX 2080 Ti GPU's
#SBATCH --gres=gpu:2080ti:4
#SBATCH --exclusive

#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=u1135435@utah.edu

#SBATCH -o slurm-%j.out-%N
#SBATCH -e slurm-%j.err-%N

# Enable CPU Hyper-threading
export OMP_NUM_THREADS=${SLURM_NTASKS}

# Needed for PDF export in Agisoft using QT
export QT_QPA_FONTDIR=/usr/share/fonts/open-sans

PROJECT_NAME='CB_20180524'

module load photoscan
metashape.sh -platform offscreen \
             -r ${HOME}/snow-aso/CHPC/Agisoft/agisoft_workflow.py \
             --base-path ${HOME}/scratch/${PROJECT_NAME} \
             --project-name ${PROJECT_NAME} \
             --dense-cloud-quality medium \
             > ${HOME}/scratch/${PROJECT_NAME}.log
