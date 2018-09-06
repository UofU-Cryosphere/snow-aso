import argparse
import os
import sys

from base.raster_file import RasterFile
from area_plot import AreaPlot
from area_differences import AreaDifferences
from histograms import Histogram
from regression import Regression

parser = argparse.ArgumentParser()
parser.add_argument(
    '--base-path',
    type=str,
    help='Root directory',
    required=True
)
parser.add_argument(
    '--lidar-dem',
    type=str,
    help='Relative path to lidar DEM relative from base path',
    required=True
)
parser.add_argument(
    '--sfm-dem',
    type=str,
    help='Relative path to SfM DEM relative from base path',
    required=True
)
parser.add_argument(
    '--shape-file',
    type=str,
    help='Shapefile for sfm and lidar relative from base path',
)
parser.add_argument(
    '--output-path',
    type=str,
    help='Directory where plots should be saved to',
    default='comparison'
)
parser.add_argument(
    '--plots',
    action='store_true',
    help='Create comparison plots for elevation, slope, and aspect difference'
)
parser.add_argument(
    '--regression',
    action='store_true',
    help='Run regression analysis'
)

if __name__ == '__main__':
    arguments = parser.parse_args()

    base_path = os.path.join(arguments.base_path)

    lidar_file = RasterFile(os.path.join(base_path, arguments.lidar_dem))
    sfm_file = RasterFile(os.path.join(base_path, arguments.sfm_dem))

    output_path = os.path.join(base_path, arguments.output_path, '')
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    shape_file = os.path.join(base_path, arguments.shape_file)
    if arguments.shape_file and os.path.exists(shape_file):
        lidar_file.crop_to_shape(shape_file)
        sfm_file.crop_to_shape(shape_file)
    elif arguments.shape_file:
        print('ERROR - Shapefile not found:\n   ' + shape_file)
        sys.exit()

    args = dict(lidar=lidar_file, sfm=sfm_file, output_path=output_path)

    if arguments.plots:
        area_plot = AreaPlot(**args)
        [area_plot.plot(attr) for attr in AreaPlot.TYPES]
        del area_plot

        area_difference = AreaDifferences(**args)
        [area_difference.plot(attr) for attr in AreaDifferences.TYPES]
        del area_difference

        histogram = Histogram(**args)
        [histogram.plot(attr) for attr in Histogram.TYPES]
        del histogram

    if arguments.regression:
        Regression(**args).scatter_plots()
