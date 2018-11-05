import argparse
import matplotlib.pyplot as plt

from base.plot_base import PlotBase
from base.point_cloud import PointCloud

parser = argparse.ArgumentParser()
parser.add_argument(
    '--point-cloud-file',
    type=str,
    help='Path to point cloud file',
    required=True
)

if __name__ == '__main__':
    arguments = parser.parse_args()
    point_cloud = PointCloud(arguments.point_cloud_file)

    plt.hist(
        point_cloud.values['Z'],
        bins=PlotBase.NUM_BINS,
        label='lidar',
        alpha=0.5,
        color='g'
    )
    plt.xlim(point_cloud.values['Z'].min(), point_cloud.values['Z'].max())
    plt.xlim(point_cloud.values['Z'].min(), point_cloud.values['Z'].max())
    plt.ylabel('Count')
    plt.xlabel('Elevation')
    plt.title('Point cloud elevations')

    plt.show()
