import gdal
import numpy as np


class RasterFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.file = gdal.Open(filename)
        self._extent = None
        self._data = None
        self._max_elevation = None
        self._min_elevation = None
        self._hillshade = None

    @property
    def extent(self):
        if self._extent is None:
            gt = self.file.GetGeoTransform()
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
    def raster_data(self):
        if self._data is None:
            band = self.file.GetRasterBand(1)
            self._data = np.ma.masked_values(
                band.ReadAsArray(), band.GetNoDataValue(), copy=False
            )
            del band
        return self._data

    @property
    def max_elevation(self):
        if self._max_elevation is None:
            self._max_elevation = self.raster_data.max()
        return self._max_elevation

    @property
    def min_elevation(self):
        if self._min_elevation is None:
            self._min_elevation = self.raster_data.min()
        return self._min_elevation
