#!/bin/bash

#SBATCH --job-name=u1135435_pdal
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
source activate ~/conda_envs/snow_aso

PROJECT_NAME='ERW_20180524'
LIDAR_FILE="${PROJECT_NAME}_merge.laz"
HOME_DIR="/uufs/chpc.utah.edu/common/home/u1135435/scratch/${PROJECT_NAME}"
LOCAL_SCRATCH='/scratch/local/u1135435'

mkdir -p ${LOCAL_SCRATCH}

cp ${HOME_DIR}/Lidar/${LIDAR_FILE} ${LOCAL_SCRATCH}/

cd ${HOME_DIR}

python ~/snow-aso/point_cloud/lidar_cloud_to_dem.py \
  --lidar-laz ${LOCAL_SCRATCH}/${LIDAR_FILE} \
  --casi-mask ${HOME_DIR}/${PROJECT_NAME}_CASI.tif \
  --basin ERW

rm ${LOCAL_SCRATCH}/${LIDAR_FILE}

cp ${LOCAL_SCRATCH}/* ${HOME_DIR}/

rm -rf ${LOCAL_SCRATCH}
