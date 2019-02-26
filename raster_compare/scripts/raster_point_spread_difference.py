import argparse

from raster_compare.base import PdalMapper, RasterFile
from raster_compare.plots import RasterPointSpreadDifference

parser = argparse.ArgumentParser()
parser.add_argument(
    '--raster',
    type=str,
    help='Relative path to raster',
    required=True
)
parser.add_argument(
    '--raster-2',
    type=str,
    help='Relative path to raster 2',
    required=True
)
parser.add_argument(
    '--output-path',
    type=str,
    help='Path where plots should be saved to',
    required=True
)

if __name__ == '__main__':
    arguments = parser.parse_args()

    raster = RasterFile(arguments.raster, PdalMapper.RASTER_BANDS['max'])
    raster_2 = RasterFile(arguments.raster_2, PdalMapper.RASTER_BANDS['max'])
    rps = RasterPointSpreadDifference(
        raster, raster_2, output_path=arguments.output_path
    )

    rps.plot()
