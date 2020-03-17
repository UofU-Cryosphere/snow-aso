#!/bin/bash

#SBATCH --job-name=python
#SBATCH --account=owner-gpu-guest
#SBATCH --partition=notchpeak-gpu-guest

#SBATCH --time=24:00:00
#SBATCH --ntasks=16
#SBATCH --mem=16G

#SBATCH --mail-type=FAIL
#SBATCH --mail-user=email@address.com

#SBATCH -o slurm-%j.out-%N                      # stdout, using job ID (%j) and the first node (%N)
#SBATCH -e slurm-%j.err-%N                      # stderr, using job and first node

source load_conda_env.sh snow_aso

PROJECT_NAME='project_xyz'
HOME_DIR="${HOME}/scratch/${PROJECT_NAME}"

mkdir -p ${HOME_DIR}
cd ${HOME_DIR}

python path/to/script.py
