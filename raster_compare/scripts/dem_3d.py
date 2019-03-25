import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

from base.raster_file import RasterFile


def get_mesh_grid(gt, shape):
    x_res = 1  # gt[1]
    y_res = 1  # gt[5]

    return np.meshgrid(
        np.arange(gt[0], gt[0] + shape[1] * x_res, x_res),  # X
        np.arange(gt[3], gt[3] + shape[0] * y_res, y_res)  # Y
    )


def render_3d(source):
    x, y = get_mesh_grid(source.geo_transform(), source.band_values().shape)

    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})

    surface = ax.plot_surface(
        x, y, source.band_values().filled(np.nan),
        cmap=cm.get_cmap('jet'),
        linewidth=0,
        vmin=source.band_values().min(),
        vmax=source.band_values().max(),
        alpha=0.7,
    )

    ax.view_init(20, 20)
    fig.colorbar(surface)

    plt.show()


if __name__ == '__main__':
    lidar = RasterFile('', 1)
    render_3d(lidar)
