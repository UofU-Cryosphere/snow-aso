import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

from base.common import LIDAR
from base.raster_file import RasterFile


def get_mesh_grid(gt, shape):
    x_res = 1  # gt[1]
    y_res = 1  # gt[5]

    return np.meshgrid(
        np.arange(gt[0], gt[0] + shape[1] * x_res, x_res),  # X
        np.arange(gt[3], gt[3] + shape[0] * y_res, y_res)  # Y
    )


def render_3d(source):
    x, y = get_mesh_grid(source.geo_transform(), source.raster_data.shape)

    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})

    surface = ax.plot_surface(
        x, y, source.raster_data.filled(np.nan),
        cmap=cm.get_cmap('jet'),
        linewidth=0,
        vmin=source.min_elevation,
        vmax=source.max_elevation,
        alpha=0.7,
    )

    ax.view_init(20, 20)
    fig.colorbar(surface)

    plt.show()


if __name__ == '__main__':
    lidar = RasterFile(LIDAR)
    render_3d(lidar)
