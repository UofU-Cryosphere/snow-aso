#!/bin/bash

#SBATCH --job-name=rclone_backup
#SBATCH --account=notchpeak-gpu
#SBATCH --partition=notchpeak-gpu

#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --mem=1G

#SBATCH --mail-type=FAIL,END                    # Events to send mail out
#SBATCH --mail-user=u1135435@utah.edu           # Email address to sent to

#SBATCH -o slurm-%j.out-%N                      # stdout, using job ID (%j) and the first node (%N)
#SBATCH -e slurm-%j.err-%N                      # stderr, using job and first node

ml rclone

cd ~/scratch/

rclone sync --log-level 'INFO' _SOURCE_ gcloud:/backup/_DESTINATION_
