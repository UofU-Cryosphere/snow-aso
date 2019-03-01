import argparse

from raster_compare.base import PdalMapper, RasterFile
from raster_compare.plots import OrthoRgbAverage

parser = argparse.ArgumentParser()
parser.add_argument(
    '--ortho-image',
    type=str,
    help='Path to ortho photo used as background',
    required=True
)
parser.add_argument(
    '--raster-dem',
    type=str,
    help='Optional raster for axes labels'
)

if __name__ == '__main__':
    arguments = parser.parse_args()

    raster = RasterFile(arguments.raster_dem, PdalMapper.RASTER_BANDS['mean'])
    rgb_ortho = OrthoRgbAverage(
        raster, ortho_image=arguments.ortho_image, output_path=''
    )
    rgb_ortho.plot()
