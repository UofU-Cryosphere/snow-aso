from raster_compare.base import PdalMapper
from .raster_point_spread import RasterPointSpread


class RasterPointSpreadDifference(RasterPointSpread):
    """
        data - reference raster
        compare_data - raster that is compared 
    """

    def __init__(self, data, compare_data, **kwargs):
        super().__init__(data, **kwargs)
        self._compare_data = compare_data

    @property
    def compare_data(self):
        return self._compare_data

    def diff_per_cell(self):
        diff_per_cell = self.data.band_values(
            band_number=PdalMapper.RASTER_BANDS['max']
        ) - self.data.band_values(
            band_number=PdalMapper.RASTER_BANDS['min']
        )
        diff_per_cell_2 = self.compare_data.band_values(
            band_number=PdalMapper.RASTER_BANDS['max']
        ) - self.compare_data.band_values(
            band_number=PdalMapper.RASTER_BANDS['min']
        )

        return diff_per_cell_2 - diff_per_cell
