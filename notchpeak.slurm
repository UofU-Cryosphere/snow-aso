#!/bin/bash

#SBATCH --job-name=u1135435_agisoft
#SBATCH --account=notchpeak-gpu                 # account - abbreviated by -A
#SBATCH --partition=notchpeak-gpu               # partition, abbreviated by -p # # set data and working directories

#SBATCH --time=12:00:00                         # wall time, abbreviated by -t
#SBATCH --nodes=1                               # number of cluster nodes, abbreviated by -N
#SBATCH --ntasks=16                             # number of requested cores
#SBATCH --mem=0                                 # No limit on memory
#SBATCH -w notch003                             # Target specific GPU node, possible GPU nodes: notch00[1-3]
#SBATCH --gres=gpu:v100:3                       # Use the GPU on notchpeak, resource_type:resource_name:resource_count
                                                # Each node has 3 GPUs. Recommended to request them all.

#SBATCH --mail-type=FAIL                        # Events to send mail out
#SBATCH --mail-user=u1135435@utah.edu           # Email address to sent to

#SBATCH -o slurm-%j.out-%N            # stdout, using job ID (%j) and the first node (%N)
#SBATCH -e slurm-%j.err-%N            # stderr, using job and first node

module load photoscan
photoscan.sh -platform offscreen -r $HOME/snow-aso/agisoft_workflow.py --base-path $HOME/scratch/CO_20170221 --project-name CO_tiff_20170221 > $HOME/scratch/CO_20170221.log

