from base.common import LIDAR, SFM
from base.raster_file import RasterFile
from area_plot import AreaPlot
from dem_differences import DemDifferences
from histograms import Histogram

if __name__ == '__main__':
    lidar_file = RasterFile(LIDAR)
    sfm_file = RasterFile(SFM)

    [AreaPlot(LIDAR, SFM).plot(attr) for attr in AreaPlot.TYPES]
    DemDifferences(lidar_file, sfm_file).plot()
    [Histogram(LIDAR, SFM).plot(attr) for attr in Histogram.TYPES]
