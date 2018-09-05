import gdal
import numpy as np
import os
import sys


class RasterFile(object):
    def __init__(self, filename):
        if os.path.exists(filename):
            self.filename = filename
        else:
            print('File not found:\n  ' + filename)
            sys.exit()

        self._file = None
        self._extent = None
        self._elevation = None
        self._hillshade = None
        self._slope = None
        self._aspect = None

    @property
    def file(self):
        if self._file is None:
            self._file = gdal.Open(self.filename)
        return self._file

    @file.setter
    def file(self, value):
        self._file = value

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

    @staticmethod
    def get_values_for_raster(raster, band_number=1):
        band = raster.GetRasterBand(band_number)
        values = np.ma.masked_values(
            band.ReadAsArray(), band.GetNoDataValue() or 0., copy=False
        )
        del band
        return values

    def get_raster_attribute(self, attribute):
        raster = gdal.DEMProcessing(
                '', self.file, attribute, format='MEM'
            )
        raster_values = self.get_values_for_raster(raster)
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
            self._elevation = self.get_values_for_raster(self.file)
        return self._elevation

    def geo_transform(self):
        return self._file.GetGeoTransform()

    def crop_to_shape(self, shape_file):
        print('Cropping raster:\n   ' + self.filename +
              '\nto shape:\n   ' + shape_file + '\n')
        self.file = gdal.Warp(
            '', self.filename, format='MEM', dstAlpha=True, cropToCutline=True,
            cutlineDSName=shape_file
        )
