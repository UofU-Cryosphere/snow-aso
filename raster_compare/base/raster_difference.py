import numpy as np
from osgeo import gdal, gdalnumeric

from base.raster_file import RasterFile


class RasterDifference(object):
    ELEVATION_UPPER_FILTER = 20
    ELEVATION_LOWER_FILTER = -20

    BIN_WIDTH = 10  # 10m

    GDAL_DRIVER = gdal.GetDriverByName('GTiff')
    GDAL_OPTIONS = ["COMPRESS=LZW", "TILED=YES",
                    "BIGTIFF=IF_SAFER", "NUM_THREADS=ALL_CPUS"]

    def __init__(self, lidar, sfm):
        self.lidar = lidar if type(lidar) is RasterFile else RasterFile(lidar)
        self.sfm = sfm if type(sfm) is RasterFile else RasterFile(sfm)
        self._aspect = None
        self._elevation = None
        self._slope = None

    @property
    def aspect(self):
        if self._aspect is None:
            self._aspect = self.sfm.aspect - self.lidar.aspect
        return self._aspect

    @property
    def elevation(self):
        if self._elevation is None:
            self._elevation = self.sfm.elevation - self.lidar.elevation
            self._elevation.mask = np.ma.mask_or(
                self.lidar.elevation.mask,
                np.ma.masked_outside(
                    self._elevation,
                    self.ELEVATION_LOWER_FILTER,
                    self.ELEVATION_UPPER_FILTER
                ).mask
            )
        return self._elevation

    @property
    def slope(self):
        if self._slope is None:
            self._slope = self.sfm.slope - self.lidar.slope
        return self._slope

    def min_for_attr(self, attr):
        return min(
                getattr(self.lidar, attr).min(),
                getattr(self.sfm, attr).min()
            )

    def max_for_attr(self, attr):
        return max(
                getattr(self.lidar, attr).max(),
                getattr(self.sfm, attr).max()
            )

    def bin_range(self, attr):
        return np.arange(
            self.min_for_attr(attr),
            self.max_for_attr(attr) + RasterDifference.BIN_WIDTH,
            RasterDifference.BIN_WIDTH
        )

    def percentile(self, percent, attribute='elevation'):
        return np.percentile(getattr(self, attribute).compressed(), percent)

    @staticmethod
    def percentage_mean(diff, count):
        return (np.absolute(diff).sum() / count) * 100

    @staticmethod
    def round_to_tenth(elevation):
        return elevation - (elevation % 10)

    def save(self):
        file_name = self.sfm.file.GetDescription()
        file_name = file_name.replace('.tif', '_difference.tif')
        output_file = self.GDAL_DRIVER.CreateCopy(
            file_name,
            self.sfm.file,
            strict=0,
            options=self.GDAL_OPTIONS
        )

        band = output_file.GetRasterBand(1)
        no_data_value = band.GetNoDataValue()
        band.SetNoDataValue(no_data_value)
        gdalnumeric.BandWriteArray(band, self.elevation.filled(no_data_value))

        print('Saving difference raster:\n   ' + file_name)

        del band
        del output_file
