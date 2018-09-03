from base.common import LIDAR, SFM, SHAPE_FILE
from base.raster_file import RasterFile
from area_plot import AreaPlot
from area_differences import AreaDifferences
from histograms import Histogram

if __name__ == '__main__':
    lidar_file = RasterFile(LIDAR)
    sfm_file = RasterFile(SFM)

    lidar_file.crop_to_shape(SHAPE_FILE)
    sfm_file.crop_to_shape(SHAPE_FILE)

    [AreaPlot(lidar_file, sfm_file).plot(attr) for attr in AreaPlot.TYPES]
    [
        AreaDifferences(lidar_file, sfm_file).plot(attr)
        for attr in AreaDifferences.TYPES
     ]
    [Histogram(lidar_file, sfm_file).plot(attr) for attr in Histogram.TYPES]
