import os

ROOT_DIR = '/Volumes/warehouse/projects/UofU/ASO'
IMAGE_DIR = 'camera'
LIDAR_DIR = 'lidar'
# SBET (Smooth Best Estimated Trajectory)
SBET_DIR = 'SBET'

CO_DIR = 'CO_20170221'

CO_IMAGE_PATH = os.path.join(ROOT_DIR, CO_DIR, IMAGE_DIR)
CO_LIDAR_PATH = os.path.join(ROOT_DIR, CO_DIR, LIDAR_DIR)
CO_SBET_PATH = os.path.join(ROOT_DIR, CO_DIR, SBET_DIR)

