import numpy as np
from osgeo import gdal

from .median_absolute_deviation import MedianAbsoluteDeviation
from .raster_file import RasterFile


class RasterDifference(object):
    GDAL_DRIVER = gdal.GetDriverByName('GTiff')

    def __init__(self, lidar, sfm, band_number):
        self.lidar = RasterFile(lidar, band_number)
        self.sfm = RasterFile(sfm, band_number)
        self._aspect = None
        self.band_values = self.sfm.band_values() - self.lidar.band_values()
        self.band_mask = self.band_values.mask
        self.mad = MedianAbsoluteDeviation(self.band_values.compressed())
        self._slope = None

    @property
    def band_values(self):
        return self._band_values

    @band_values.setter
    def band_values(self, value):
        self._band_values = value

    @property
    def band_mask(self):
        return self._band_mask

    @band_mask.setter
    def band_mask(self, value):
        self._band_mask = np.copy(value)

    def band_outlier_max(self):
        return self.mad.data_median + self.mad.standard_deviation(2)

    def band_outlier_min(self):
        return self.mad.data_median - self.mad.standard_deviation(2)

    @property
    def band_filtered(self):
        self.band_values.mask = np.ma.mask_or(
            self.band_mask,
            np.ma.masked_outside(
                self.band_unfiltered,
                self.band_outlier_min(),
                self.band_outlier_max()
            ).mask
        )
        return self.band_values

    @property
    def band_unfiltered(self):
        self.band_values.mask = self.band_mask
        return self.band_values

    @property
    def band_outliers(self):
        self.band_values.mask = np.ma.mask_or(
            self.band_mask,
            np.ma.masked_inside(
                self.band_unfiltered,
                self.band_outlier_min(),
                self.band_outlier_max()
            ).mask
        )
        return self.band_values

    @property
    def aspect(self):
        if self._aspect is None:
            self._aspect = self.sfm.aspect - self.lidar.aspect
        return self._aspect

    @property
    def slope(self):
        if self._slope is None:
            self._slope = self.sfm.slope - self.lidar.slope
        return self._slope
