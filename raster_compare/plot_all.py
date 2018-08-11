import dem_compare
import dem_differences
import elevation_histograms

from base.common import LIDAR, SFM
from base.raster_file import RasterFile

if __name__ == '__main__':
    lidar_file = RasterFile(LIDAR)
    sfm_file = RasterFile(SFM)

    dem_compare.plot(lidar_file, sfm_file)
    dem_differences.plot(lidar_file, sfm_file)
    elevation_histograms.plot(lidar_file, sfm_file)
