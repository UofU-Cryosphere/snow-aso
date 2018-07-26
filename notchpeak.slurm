#!/bin/bash

#SBATCH --job-name=u1135435_agisoft
#SBATCH --account=notchpeak-gpu                 # account - abbreviated by -A
#SBATCH --partition=notchpeak-gpu               # partition, abbreviated by -p # # set data and working directories

#SBATCH --time=24:00:00                         # wall time, abbreviated by -t
#SBATCH --nodes=1                               # number of cluster nodes, abbreviated by -N
#SBATCH --ntasks=32                             # number of requested CPU cores
#SBATCH --mem=0                                 # No limit on memory
#SBATCH -w notch003                             # Target specific GPU node, possible GPU nodes: notch00[1-3]
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

PROJECT_NAME='CO_20170221'

module load photoscan
photoscan.sh -platform offscreen -r $HOME/snow-aso/agisoft_workflow.py --base-path $HOME/scratch/CO_20170221 --project-name $PROJECT_NAME > $HOME/scratch/$PROJECT_NAME.log

# Compress the results
# cd $HOME/scratch/CO_20170221

# tar -c --use-compress-program=pigz -f $PROJECT_NAME.tgz PROJECT_NAME.*