import argparse

from base import RasterFile
from raster_stats import RasterStats

parser = argparse.ArgumentParser()
parser.add_argument(
    '--lidar',
    type=str,
    help='Path to raster file with differences in elevation',
    required=True
)
parser.add_argument(
    '--sfm',
    type=str,
    help='Path to raster file with differences in elevation',
    required=True
)
parser.add_argument(
    '--output-path',
    type=str,
    help='Path where plots should be saved to',
    required=True
)
parser.add_argument(
    '--stats-type',
    type=str,
    help='Type of statistic to compare. Options: max, min, stdev',
    choices=RasterStats.BAND_STATS.keys()
)
parser.add_argument(
    '--outliers',
    action='store_true',
    help='Plot for outliers above given percentile'
)
parser.add_argument(
    '--percentile',
    type=int,
    default=98,
    help='Percentile considered outlier'
)
parser.add_argument(
    '--all',
    action='store_true',
    help='Plot for all available stats-types including outliers'
)

if __name__ == '__main__':
    arguments = parser.parse_args()

    statistic = RasterStats(
        lidar=arguments.lidar,
        sfm=arguments.sfm,
        output_path=arguments.output_path
    )

    lidar_file = RasterFile(arguments.lidar)
    sfm_file = RasterFile(arguments.sfm)

    if arguments.all:
        for stat in RasterStats.BAND_STATS.keys():
            statistic.plot(stat, arguments)

            arguments.outliers = not arguments.outliers
            statistic.plot(stat, arguments)
    else:
        statistic.plot(RasterStats.BAND_STATS[arguments.stats_type], arguments)
