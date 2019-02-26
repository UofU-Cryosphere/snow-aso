from raster_compare.base import PdalMapper
from .raster_point_spread import RasterPointSpread


class RasterPointSpreadDifference(RasterPointSpread):
    def __init__(self, raster, raster_2, **kwargs):
        super().__init__(raster, **kwargs)
        self._raster_2 = raster_2

    @property
    def raster_2(self):
        return self._raster_2

    def min_values(self, raster):
        raster.band_number = PdalMapper.RASTER_BANDS['min']
        return raster.elevation

    def max_values(self, raster):
        raster.band_number = PdalMapper.RASTER_BANDS['max']
        return raster.elevation

    def diff_per_cell(self):
        diff_per_cell = self.max_values(self.raster) - \
                        self.min_values(self.raster)
        diff_per_cell_2 = self.max_values(self.raster_2) - \
                          self.min_values(self.raster_2)

        return diff_per_cell_2 - diff_per_cell
