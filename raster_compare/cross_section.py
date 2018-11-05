import argparse

import matplotlib.pyplot as plt

from base import PointCloud, PlotBase

parser = argparse.ArgumentParser()
parser.add_argument(
    '--point-cloud-file',
    type=str,
    help='Path to point cloud file',
    required=True
)


def assign_to_line(point, lines):
    if point[2] < 3880:
        return

    if point[1] not in lines:
        lines[point[1]] = []
    lines[point[1]].append({'X': point[0], 'Z': point[2]})


if __name__ == '__main__':
    arguments = parser.parse_args()
    point_cloud = PointCloud(arguments.point_cloud_file)

    longitude_lines = {}

    [assign_to_line(point, longitude_lines) for point in point_cloud.values]

    colors = ['darkred', 'blue', 'darkgreen']
    longitudes = sorted(longitude_lines.keys())

    plot_pairs = int(len(longitudes) / 3)
    line_index = 0

    for plot in range(0, plot_pairs + 1):
        plt.figure(figsize=(8, 5))
        count_lines = 0

        for line in longitudes[line_index:line_index + 3]:
            x_values = [point['X'] for point in longitude_lines[line]]
            z_values = [point['Z'] for point in longitude_lines[line]]
            plt.scatter(
                x_values, z_values, label=str(line), s=0.1, marker='2',
                c=colors[count_lines]
            )

            count_lines += 1

        plt.xlabel('Latitude', **PlotBase.label_opts())
        plt.ylabel('Elevation (m)', **PlotBase.label_opts())
        plt.title(
            'SfM point cloud longitude cross section', **PlotBase.title_opts()
        )
        plt.legend(
            handlelength=0.5,
            prop={'family': 'monospace', 'size': 14}
        )
        if longitudes[line_index] == 4199210.5:
            plt.show(**PlotBase.output_defaults())

        if plot < plot_pairs:
            line_index += 3
