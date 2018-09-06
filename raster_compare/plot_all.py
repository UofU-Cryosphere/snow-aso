import argparse

from area_differences import AreaDifferences
from area_plot import AreaPlot
from base.raster_compare import RasterCompare
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

    comparison = RasterCompare(**vars(arguments))
    comparison.prepare()

    if arguments.plots:
        area_plot = AreaPlot(**comparison.file_args())
        [area_plot.plot(attr) for attr in AreaPlot.TYPES]
        del area_plot

        area_difference = AreaDifferences(**comparison.file_args())
        [area_difference.plot(attr) for attr in AreaDifferences.TYPES]
        del area_difference

        histogram = Histogram(**comparison.file_args())
        [histogram.plot(attr) for attr in Histogram.TYPES]
        del histogram

    if arguments.regression:
        Regression(**comparison.file_args()).scatter_plots()
