import gdal
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

ROOT_PATH = '/Volumes/warehouse/projects/UofU/ASO/SB_20170221/'
LIDAR = ROOT_PATH + 'sfm-vs-lidar/CO_lidar_1m_32613_cut.tif'
SFM = ROOT_PATH + 'Agisoft/CO_20170221_dem_1m_32613_cut.tif'


def get_mesh_grid(gt, data):
    x_res = 1 # gt[1]
    y_res = 1 # gt[5]

    return np.meshgrid(
        np.arange(gt[0], gt[0] + data.shape[1] * x_res, x_res), # X
        np.arange(gt[3], gt[3] + data.shape[0] * y_res, y_res)  # Y
    )


def render_3d(file):
    source = gdal.Open(file)
    z = np.ma.masked_less_equal(
        source.GetRasterBand(1).ReadAsArray(),
        source.GetRasterBand(1).GetNoDataValue(),
        copy=False,
    )

    x, y = get_mesh_grid(source.GetGeoTransform(), z)

    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})

    surface = ax.plot_surface(
        x, y, z,
        cmap=cm.get_cmap('jet'),
        linewidth=0,
        vmin=z.min(),
        vmax=z.max(),
        alpha=0.7
    )

    ax.view_init(60, 140)
    fig.colorbar(surface)

    plt.show()


if __name__ == '__main__':
    render_3d(LIDAR)