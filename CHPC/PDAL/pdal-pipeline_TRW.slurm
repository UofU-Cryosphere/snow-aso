#!/bin/bash

#SBATCH --job-name=u1135435_pdal
#SBATCH --account=owner-gpu-guest
#SBATCH --partition=notchpeak-gpu-guest

#SBATCH --time=24:00:00                         # wall time
#SBATCH --nodes=1                               # number of cluster nodes
#SBATCH --ntasks=2                              # number of requested CPU cores
#SBATCH --mem=0
#SBATCH -w notch055

#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=u1135435@utah.edu           # Email address for events

#SBATCH -o slurm-%j.out-%N                      # stdout, using job ID (%j) and the first node (%N)
#SBATCH -e slurm-%j.err-%N                      # stderr, using job and first node

ml anaconda

source activate ~/conda_envs/snow_aso

cd ~/scratch

pdal pipeline ~/snow-aso/CHPC/PDAL/pipelines/TRW_agisoft_clip.json
