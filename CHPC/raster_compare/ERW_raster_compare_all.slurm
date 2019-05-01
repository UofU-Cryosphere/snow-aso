#!/bin/bash

#SBATCH --job-name=raster_compare
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

PROJECT_NAME='ERW_20180524'
HOME_DIR="/uufs/chpc.utah.edu/common/home/u1135435/scratch/$PROJECT_NAME"

# Speed up GDAL reading
export GDAL_CACHEMAX=20%

cd ${HOME}

python ~/raster_compare/scripts/run_all.py \
  --base-path ${HOME} \
  --lidar-dem Lidar/${PROJECT_NAME}_merge_1m.tif \
  --sfm-dem Agisoft/${PROJECT_NAME}_Agisoft_aligned_masked_1m.tif \
  --shape-file ${PROJECT_NAME}_32613.shp \
  --ortho-image ${PROJECT_NAME}_ortho_5m.tif \
  --differences \
  --side-by-side 

mv ${HOME}/comparison/elevation_difference.png ${HOME}/comparison/elevation_difference_mean.png
mv ${HOME}/comparison/elevation_difference_overlay.png ${HOME}/comparison/elevation_difference_overlay_mean.png
mv ${HOME}/comparison/elevation_comparison.png ${HOME}/comparison/elevation_comparison_mean.png


