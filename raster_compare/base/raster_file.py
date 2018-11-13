import gdal
import numpy as np


class RasterFile(object):
    DEFAULT_BAND_NUMBER = 1

    def __init__(self, filename):
        self.file = filename
        self._extent = None
        self._elevation = None
        self._hillshade = None
        self._slope = None
        self._aspect = None

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, filename):
        self._file = gdal.Open(filename)

    @property
    def extent(self):
        if self._extent is None:
            gt = self.geo_transform()
            x_min = gt[0]
            x_max = gt[0] + self.file.RasterXSize / gt[1]
            y_min = gt[3] + self.file.RasterYSize / gt[5]
            y_max = gt[3]

            self._extent = x_min, x_max, y_min, y_max
        return self._extent

    def values_for_band(self, band_number=1, **kwargs):
        raster = kwargs.get('raster', self.file)

        band = raster.GetRasterBand(band_number)
        values = np.ma.masked_values(
            band.ReadAsArray(), band.GetNoDataValue() or 0., copy=False
        )
        del band
        return values

    def get_raster_attribute(self, attribute):
        raster = gdal.DEMProcessing('', self.file, attribute, format='MEM')
        raster_values = self.values_for_band(raster=raster)
        del raster
        return raster_values

    @property
    def hill_shade(self):
        if self._hillshade is None:
            self._hillshade = self.get_raster_attribute('hillshade')
        return self._hillshade

    @property
    def slope(self):
        if self._slope is None:
            self._slope = self.get_raster_attribute('slope')
        return self._slope

    @property
    def aspect(self):
        if self._aspect is None:
            self._aspect = self.get_raster_attribute('aspect')
        return self._aspect

    @property
    def elevation(self):
        if self._elevation is None:
            self._elevation = self.values_for_band()
        return self._elevation

    def geo_transform(self):
        return self.file.GetGeoTransform()

    def join_masks(self, attribute, other):
        """
        Extend the numpy mask for given attribute with mask from given other
        masked numpy array.

        Note: This will *permanently* change the mask.

        :param attribute: name of property to change the mask
        :param other: Masked numpy array to extend the mask with
        """
        attr = getattr(self, attribute)
        attr.mask = np.ma.mask_or(attr.mask, other.mask)