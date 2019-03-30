import numpy as np
from osgeo import gdal, gdalnumeric


class RasterFile(object):
    def __init__(self, filename, band_number):
        self.file = filename
        self._band_number = band_number
        self._extent = None
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
    def band_number(self):
        return self._band_number

    @band_number.setter
    def band_number(self, band_number):
        self._band_number = band_number

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

    def band_values(self, **kwargs):
        raster = kwargs.get('raster', self.file)
        band_number = kwargs.get('band_number', self.band_number)

        band = raster.GetRasterBand(band_number)
        values = np.ma.masked_values(
            gdalnumeric.BandReadAsArray(band),
            band.GetNoDataValue() or 0.,
            copy=False
        )
        del band
        return values

    def get_raster_attribute(self, attribute, **kwargs):
        raster = gdal.DEMProcessing(
            '', self.file, attribute, format='MEM', **kwargs
        )
        raster_values = self.band_values(raster=raster, band_number=1)
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
