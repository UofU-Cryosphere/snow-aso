import argparse

from raster_compare.base import PdalMapper, RasterFile
from raster_compare.plots import RasterPointSpread

parser = argparse.ArgumentParser()
parser.add_argument(
    '--raster',
    type=str,
    help='Relative path to raster to generate spread for',
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
    rps = RasterPointSpread(raster, output_path=arguments.output_path)

    rps.plot()
