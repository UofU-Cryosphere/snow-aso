from base.common import LIDAR, SFM
from base.raster_file import RasterFile
from dem_compare import DemCompare
from dem_differences import DemDifferences
from histograms import Histogram

if __name__ == '__main__':
    lidar_file = RasterFile(LIDAR)
    sfm_file = RasterFile(SFM)

    DemCompare(lidar_file, sfm_file).plot()
    DemDifferences(lidar_file, sfm_file).plot()
    [Histogram(LIDAR, SFM).plot(type) for type in Histogram.TYPES]
