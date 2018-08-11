import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition

from base.common import ROOT_PATH, SFM, LIDAR
from base.plot_defaults import \
    title_opts, output_defaults, LABEL_FONT_SIZE, LIDAR_LABEL, SFM_LABEL
from base.raster_file import RasterFile

OUTPUT_FILE = ROOT_PATH + '/dem_compare.png'


def plot(lidar, sfm):
    figure, (ax1, ax2, cax) = plt.subplots(
        ncols=3,
        gridspec_kw={"width_ratios": [1, 1, 0.1]}
    )
    figure.set_size_inches(10, 8)

    axes = (ax1, ax2)
    ax1.get_shared_x_axes().join(ax1, ax2)
    ax1.get_shared_y_axes().join(ax1, ax2)

    for n, ax in enumerate(axes):
        ax.set_facecolor('0.9')

    hillshade_opts = dict(cmap='gray', clim=(1, 255),)
    ax1.imshow(lidar.hill_shade, extent=lidar.extent, **hillshade_opts)
    ax2.imshow(sfm.hill_shade, extent=sfm.extent, **hillshade_opts)

    v_min = min(lidar.min_elevation, sfm.min_elevation)
    v_max = min(lidar.max_elevation, sfm.max_elevation)

    im_opts = dict(cmap=cm.get_cmap('jet'), alpha=0.3, vmin=v_min, vmax=v_max)

    ax1.imshow(lidar.raster_data, extent=lidar.extent, **im_opts)
    ax1.set_title(LIDAR_LABEL, **title_opts())

    image = ax2.imshow(sfm.raster_data, extent=sfm.extent, **im_opts)
    ax2.set_yticklabels([])
    ax2.set_title(SFM_LABEL, **title_opts())

    # Lidar and SfM scale bar
    ip_1 = InsetPosition(ax2, [1.03, 0, 0.05, 1])
    cax.set_axes_locator(ip_1)
    plt.colorbar(image, cax=cax).set_label(label='Meter', size=LABEL_FONT_SIZE)

    plt.subplots_adjust(hspace=0.1)

    plt.savefig(OUTPUT_FILE, **output_defaults())


# Plot DEMs side by side
if __name__ == '__main__':
    lidar_file = RasterFile(LIDAR)
    sfm_file = RasterFile(SFM)

    plot(lidar_file, sfm_file)
