#!/bin/bash

#SBATCH --job-name=u1135435_pdal
#SBATCH --account=kingspeak-gpu
#SBATCH --partition=kingspeak-gpu

#SBATCH --time=24:00:00           
#SBATCH --nodes=1                 
#SBATCH --ntasks=12               
#SBATCH --mem=0
#SBATCH -w kp298

#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=u1135435@utah.edu           # Email address for events

#SBATCH -o slurm-%j.out-%N                      # stdout, using job ID (%j) and the first node (%N)
#SBATCH -e slurm-%j.err-%N                      # stderr, using job and first node

SOURCE_DIR='/Path/to/dir'
SCRATCH_DIR='/scratch'

REFERENCE_LAZ='reference.laz'
SOURCE_LAZ='source.laz'

cd $SCRATCH_DIR

cp $SOURCE_DIR/$REFERENCE_LAZ .
cp $SOURCE_DIR/$SOURCE_LAZ .

# Requires ASP to be installed in HOME directory
~/asp/bin/pc_align --max-displacement 1 \
         --threads $SLURM_NTASKS \
         --max-num-reference-points 200000000\
         --max-num-source-points 100000000 \
         --save-transformed-source-points \
         $SCRATCH_DIR/$REFERENCE_LAZ \
         $SCRATCH_DIR/$SOURCE_LAZ

gzip /scratch/local/run/run-beg_errors.csv
gzip /scratch/local/run/run-end_errors.csv

mv /scratch/local/run ~/scratch
rm $SCRATCH_DIR/$REFERENCE_LAZ 
rm $SCRATCH_DIR/$SOURCE_LAZ 
