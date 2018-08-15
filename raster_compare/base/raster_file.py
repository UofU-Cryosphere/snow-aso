import gdal
import numpy as np


class RasterFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.file = gdal.Open(filename)
        self._extent = None
        self._elevation = None
        self._hillshade = None
        self._slope = None
        self._aspect = None

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

    @property
    def hill_shade(self):
        if self._hillshade is None:
            hill_shade = gdal.DEMProcessing(
                '', self.filename, 'hillshade', format='MEM'
            )
            band = hill_shade.GetRasterBand(1)
            self._hillshade = np.ma.masked_values(
                band.ReadAsArray(), band.GetNoDataValue(), copy=False
            )
            del hill_shade
        return self._hillshade

    @property
    def slope(self):
        if self._slope is None:
            slope = gdal.DEMProcessing(
                '', self.filename, 'slope', format='MEM'
            )
            band = slope.GetRasterBand(1)
            self._slope = np.ma.masked_values(
                band.ReadAsArray(), band.GetNoDataValue(), copy=False
            )
            del slope
        return self._slope

    @property
    def aspect(self):
        if self._aspect is None:
            aspect = gdal.DEMProcessing(
                '', self.filename, 'aspect', format='MEM'
            )
            band = aspect.GetRasterBand(1)
            self._aspect = np.ma.masked_values(
                band.ReadAsArray(), band.GetNoDataValue(), copy=False
            )
            del aspect
        return self._aspect

    @property
    def elevation(self):
        if self._elevation is None:
            band = self.file.GetRasterBand(1)
            self._elevation = np.ma.masked_values(
                band.ReadAsArray(), band.GetNoDataValue(), copy=False
            )
            del band
        return self._elevation

    def geo_transform(self):
        return self.file.GetGeoTransform()
