#!/bin/bash

#SBATCH --job-name=snow_depth
#SBATCH --account=owner-gpu-guest
#SBATCH --partition=notchpeak-gpu-guest

#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --mem=0
#SBATCH -w notch055

#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=u1135435@utah.edu

#SBATCH -o slurm-%j.out-%N                      # stdout, using job ID (%j) and the first node (%N)
#SBATCH -e slurm-%j.err-%N                      # stderr, using job and first node

ml anaconda
source activate ~/conda_envs/raster_compare

SNOW_ON='ERW_20180524'
SNOW_OFF='ERW_20180912'
SCRATCH_DIR="/uufs/chpc.utah.edu/common/home/u1135435/scratch"
HOME_DIR="${SCRATCH_DIR}/ERW_snow_depth"

# Speed up GDAL reading
export GDAL_CACHEMAX=30%

cd ${HOME_DIR}

python ~/raster_compare/scripts/run_all.py \
  --base-path ${HOME_DIR} \
  --lidar-dem snow_off/${SNOW_OFF}_merge_1m.tif \
  --sfm-dem snow_on/${SNOW_ON}_merge_1m.tif \
  --shape-file ${SNOW_ON}_32613.shp \
  --ortho-image ${SNOW_ON}_ortho_5m.tif \
  --differences \
  --side-by-side 
