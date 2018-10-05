#!/bin/bash

#SBATCH --job-name=u1135435_agisoft
#SBATCH --account=notchpeak-gpu                 # account - abbreviated by -A
#SBATCH --partition=notchpeak-gpu               # partition, abbreviated by -p

#SBATCH --time=24:00:00                         # wall time, abbreviated by -t
#SBATCH --nodes=1                               # number of cluster nodes, abbreviated by -N
#SBATCH --ntasks=32                             # number of requested CPU cores
#SBATCH --mem=0                                 # No limit on memory
#SBATCH -w notch003                             # Target specific GPU node, possible GPU nodes: notch00[1-3]
#SBATCH --constraint="v100"                     # Request specific feature to select any possible node available with it
#SBATCH --gres=gpu:v100:3                       # Use the GPU on notchpeak, resource_type:resource_name:resource_count
                                                # Each node has 3 GPUs. Recommended to request them all.
#SBATCH --exclusive

#SBATCH --mail-type=FAIL,END                    # Events to send mail out
#SBATCH --mail-user=u1135435@utah.edu           # Email address to sent to

#SBATCH -o slurm-%j.out-%N                      # stdout, using job ID (%j) and the first node (%N)
#SBATCH -e slurm-%j.err-%N                      # stderr, using job and first node
