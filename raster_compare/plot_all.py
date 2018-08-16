from base.common import LIDAR, SFM
from base.raster_file import RasterFile
from area_plot import AreaPlot
from area_differences import AreaDifferences
from histograms import Histogram

if __name__ == '__main__':
    lidar_file = RasterFile(LIDAR)
    sfm_file = RasterFile(SFM)

    [AreaPlot(LIDAR, SFM).plot(attr) for attr in AreaPlot.TYPES]
    [AreaDifferences(LIDAR, SFM).plot(attr) for attr in AreaDifferences.TYPES]
    [Histogram(LIDAR, SFM).plot(attr) for attr in Histogram.TYPES]
