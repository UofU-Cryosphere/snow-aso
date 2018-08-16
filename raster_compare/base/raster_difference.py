import numpy as np
from base.raster_file import RasterFile


class RasterDifference(object):
    ELEVATION_UPPER_FILTER = 20
    ELEVATION_LOWER_FILTER = -10

    BIN_WIDTH = 10  # 10m

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
            self._elevation.mask[
                self._elevation > self.ELEVATION_UPPER_FILTER
                ] = self.ELEVATION_UPPER_FILTER
            self._elevation.mask[
                self._elevation < self.ELEVATION_LOWER_FILTER
                ] = self.ELEVATION_LOWER_FILTER
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

    @staticmethod
    def percentage_mean(diff, count):
        return (np.absolute(diff).sum() / count) * 100

    @staticmethod
    def round_to_tenth(elevation):
        return elevation - (elevation % 10)
