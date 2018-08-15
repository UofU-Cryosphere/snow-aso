import numpy as np
from base.raster_file import RasterFile


class RasterDifference(object):
    UPPER_FILTER = 20
    LOWER_FILTER = -10

    BIN_WIDTH = 10  # 10m

    def __init__(self, lidar, sfm):
        self.lidar = lidar if type(lidar) is RasterFile else RasterFile(lidar)
        self.sfm = sfm if type(sfm) is RasterFile else RasterFile(sfm)
        self._elevation = None

    @property
    def elevation(self):
        if self._elevation is None:
            self._elevation = self.sfm.elevation - self.lidar.elevation
            self._elevation.mask[
                self._elevation > self.UPPER_FILTER
                ] = self.UPPER_FILTER
            self._elevation.mask[
                self._elevation < self.LOWER_FILTER
                ] = self.LOWER_FILTER
        return self._elevation

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
    def round_to_tenth(elevation):
        return elevation - (elevation % 10)
