import gdal
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition

ROOT_PATH = '/Volumes/warehouse/projects/UofU/ASO/SB_20170221/'
LIDAR = ROOT_PATH + 'sfm-vs-lidar/CO_lidar_1m_32613_cut.tif'
SFM = ROOT_PATH + 'Agisoft/CO_20170221_dem_1m_32613_cut.tif'

NUM_BINS = 50


def get_hill_shade(filename):
    hill_shade = gdal.DEMProcessing('', filename, 'hillshade', format='MEM')
    band = hill_shade.GetRasterBand(1)
    return np.ma.masked_values(
        band.ReadAsArray(), band.GetNoDataValue(), copy=False
    )


def get_raster_values(filename):
    file = gdal.Open(filename)
    band = file.GetRasterBand(1)
    return np.ma.masked_values(
        band.ReadAsArray(), band.GetNoDataValue(), copy=False
    )


def get_extent(file):
    gt = file.GetGeoTransform()
    x_min = gt[0]
    x_max = gt[0] + file.RasterXSize / gt[1]
    y_min = gt[3] + file.RasterYSize / gt[5]
    y_max = gt[3]

    return x_min, x_max, y_min, y_max


def text_box_args(x, y, text, **kwargs):
    return dict(
        x=x, y=y, s=text, ha='left', va='top',
        bbox=dict(
            boxstyle='square',
            edgecolor='black',
            facecolor='grey',
            alpha=0.2,
            pad=0.6
        ),
        **kwargs)


def render_diff():
    extent_sfm = get_extent(gdal.Open(SFM))

    figure, (ax1, cax, ax2) = plt.subplots(
        nrows=1,
        ncols=3,
        gridspec_kw={"width_ratios":[1, 0.1, 1], 'height_ratios':[1]}
    )

    sfm = get_raster_values(SFM)
    lidar = get_raster_values(LIDAR)

    diff = sfm - lidar

    diff.mask[diff.data > 20] = 20
    diff.mask[diff.data < -10] = -10

    diff_plot = ax1.imshow(
        diff,
        cmap=cm.get_cmap('tab20c'),
        alpha=0.3,
        vmin=-diff.min(),
        vmax=diff.max(),
        extent=extent_sfm
    )
    ax1.set_title('Difference', fontdict={ 'fontsize': 20 })

    mean = diff.mean()
    sd = diff.std()
    box_text = 'Mean: ' + str(mean.round(2)) + '\nSD: ' + str(sd.round(2))

    ax2.hist(diff.compressed(), bins='auto')
    ax2.set_title('Differences in Meter', fontsize=20)
    ax2.set_xlabel('Meter', fontsize=16)
    ax2.set_aspect(0.000935)
    ax2.text(**text_box_args(11, 24000, box_text, fontsize=16))

    # Differences scale bar
    ip_2 = InsetPosition(ax1, [1.03, 0, 0.05, 1])
    cax.set_axes_locator(ip_2)
    plt.colorbar(diff_plot, cax=cax).set_label(label='Meter',size=16)

    plt.subplots_adjust(hspace=0.1)

    figure.set_size_inches(14, 8)
    plt.savefig(ROOT_PATH + '/dem_diff.png', bbox_inches='tight', dpi=200)


def render_dems():
    extent_lidar = get_extent(gdal.Open(LIDAR))
    extent_sfm = get_extent(gdal.Open(SFM))

    figure, (ax1, ax2, cax) = plt.subplots(
        ncols=3,
        gridspec_kw={"width_ratios":[1, 1, 0.1]}
    )

    axes = (ax1, ax2)
    ax1.get_shared_x_axes().join(ax1, ax2)
    ax1.get_shared_y_axes().join(ax1, ax2)

    for n, ax in enumerate(axes):
        ax.set_facecolor('0.9')

    ax1.imshow(
        get_hill_shade(LIDAR), cmap='gray', clim=(1,255), extent=extent_lidar
    )
    ax2.imshow(
        get_hill_shade(SFM), cmap='gray', clim=(1,255), extent=extent_sfm
    )

    sfm = get_raster_values(SFM)
    lidar = get_raster_values(LIDAR)
    vmin = min(lidar.min(), sfm.min())
    vmax = min(lidar.max(), sfm.max())

    ax1.imshow(
        lidar,
        cmap=cm.get_cmap('jet'),
        alpha=0.3,
        vmin=vmin,
        vmax=vmax,
        extent=extent_lidar
    )
    ax1.set_title('Lidar', fontdict={ 'fontsize': 24 })

    image = ax2.imshow(
        sfm,
        cmap=cm.get_cmap('jet'),
        alpha=0.3,
        vmin=vmin,
        vmax=vmax,
        extent=extent_sfm
    )
    ax2.set_yticklabels([])
    ax2.set_title('SfM', fontdict={ 'fontsize': 24 })

    # Lidar and SfM scale bar
    ip_1 = InsetPosition(ax2, [1.03, 0, 0.05, 1])
    cax.set_axes_locator(ip_1)
    plt.colorbar(image, cax=cax).set_label(label='Meter',size=16)

    plt.subplots_adjust(hspace=0.1)

    figure.set_size_inches(10, 8)
    plt.savefig(ROOT_PATH + '/dem_compare.png', bbox_inches='tight', dpi=300)


def render_hist():
    sfm = get_raster_values(SFM)
    lidar = get_raster_values(LIDAR)

    ax1 = plt.subplot(2, 1, 1)
    plt.hist(
        lidar.compressed(), bins=NUM_BINS, alpha=0.5, label='lidar', color='b'
    )
    plt.xlim(lidar.min(), lidar.max())
    plt.legend()
    plt.title('Elevation distribution')
    plt.ylabel('Count')
    ax1.text(
        **text_box_args(3380, 125000, 'Mean: ' + str(lidar.mean().round(2)))
    )

    ax2 = plt.subplot(2, 1, 2)
    plt.hist(sfm.compressed(), bins=NUM_BINS, alpha=0.5, label='sfm', color='g')
    plt.xlim(sfm.min(), sfm.max())
    plt.legend()
    plt.ylabel('Count')
    plt.xlabel('Elevation')
    ax2.text(**text_box_args(3380, 125000, 'Mean: ' + str(sfm.mean().round(2))))

    plt.savefig(
        ROOT_PATH + '/histogram_elevations.png', bbox_inches='tight', dpi=300
    )


if __name__ == '__main__':
    # render_dems()
    render_diff()
    # render_hist()
