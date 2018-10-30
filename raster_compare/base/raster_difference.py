import numpy as np
from osgeo import gdal, gdalnumeric

from base.raster_file import RasterFile
from base.median_absolute_deviation import MedianAbsoluteDeviation


class RasterDifference(object):
    BIN_WIDTH = 10  # 10m

    GDAL_DRIVER = gdal.GetDriverByName('GTiff')
    GDAL_OPTIONS = ["COMPRESS=LZW", "TILED=YES",
                    "BIGTIFF=IF_SAFER", "NUM_THREADS=ALL_CPUS"]

    def __init__(self, lidar, sfm):
        self.lidar = lidar if type(lidar) is RasterFile else RasterFile(lidar)
        self.sfm = sfm if type(sfm) is RasterFile else RasterFile(sfm)
        self._aspect = None
        self.elevation_values = self.sfm.elevation - self.lidar.elevation
        self.elevation_mask = self.elevation_values.mask
        self.mad = MedianAbsoluteDeviation(self.elevation_values.compressed())
        self._slope = None

    @property
    def aspect(self):
        if self._aspect is None:
            self._aspect = self.sfm.aspect - self.lidar.aspect
        return self._aspect

    @property
    def elevation_values(self):
        return self._elevation_values

    @elevation_values.setter
    def elevation_values(self, value):
        self._elevation_values = value

    @property
    def elevation_mask(self):
        return self._elevation_mask

    @elevation_mask.setter
    def elevation_mask(self, value):
        self._elevation_mask = np.copy(value)

    def elevation_upper_filter(self):
        return self.mad.data_median + self.mad.percentile(95)

    def elevation_lower_filter(self):
        return self.mad.data_median - self.mad.percentile(95)

    @property
    def elevation(self):
        self.elevation_values.mask = np.ma.mask_or(
            self.elevation_mask,
            np.ma.masked_outside(
                self.elevation_unfiltered,
                self.elevation_lower_filter(),
                self.elevation_upper_filter()
            ).mask
        )
        return self.elevation_values

    @property
    def elevation_unfiltered(self):
        self.elevation_values.mask = self.elevation_mask
        return self.elevation_values

    @property
    def elevation_filtered(self):
        self.elevation_values.mask = np.ma.mask_or(
            self.elevation_mask,
            np.ma.masked_inside(
                self.elevation_unfiltered,
                self.elevation_lower_filter(),
                self.elevation_upper_filter()
            ).mask
        )
        return self.elevation_values

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
        gdalnumeric.BandWriteArray(band, self.elevation_values)

        print('Saving difference raster:\n   ' + file_name)

        del band
        del output_file
