import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure

from base.common import ROOT_PATH, SFM, LIDAR
from base.plot_defaults import \
    title_opts, text_box_args, output_defaults, label_opts, \
    BIN_WIDTH, NUM_BINS, LIDAR_LABEL, SFM_LABEL
from base.raster_file import RasterFile

OUTPUT_FILE = ROOT_PATH + '/elevation_histograms.png'


def add_stats_box(ax, data):
    ax.text(
        **text_box_args(3380, 90000, 'Mean: ' + str(data.mean().round(2)))
    )


# Plot elevation histograms per bin width side by side
def render_side_by_side(lidar, sfm):
    plt.subplot(1, 1, 1)
    plt.hist(
        [lidar.raster_data.compressed(), sfm.raster_data.compressed()],
        label=['lidar', 'sfm'],
        color=['g', 'b'],
        bins=NUM_BINS,
        alpha=0.4
    )
    plt.legend(loc='upper right')


# Plot elevation distribution histogram individually and
# one difference histogram per bin width of 10m
def render_stacked(lidar, sfm):
    v_min = min(lidar.min_elevation, sfm.min_elevation)
    v_max = min(lidar.max_elevation, sfm.max_elevation) + 1
    bins = np.arange(v_min, v_max + BIN_WIDTH, BIN_WIDTH)

    figure(figsize=(14, 16))

    hist_opts = dict(bins=bins, alpha=0.5)

    ax1 = plt.subplot(3, 1, 1)
    h1 = plt.hist(
        lidar.raster_data.compressed(), label=LIDAR_LABEL, color='b',
        **hist_opts
    )
    plt.xlim(v_min, v_max)
    plt.title('Elevation distribution', **title_opts())
    plt.ylabel('Count', **label_opts())
    plt.legend()
    add_stats_box(ax1, lidar.raster_data)

    ax2 = plt.subplot(3, 1, 2)
    h2 = plt.hist(
        sfm.raster_data.compressed(), label=SFM_LABEL, color='g', **hist_opts
    )
    plt.xlim(v_min, v_max)
    plt.title('Elevation distribution', **title_opts())
    plt.ylabel('Count', **label_opts())
    plt.legend()
    add_stats_box(ax2, sfm.raster_data)

    diff = (h2[0] - h1[0])

    plt.subplot(3, 1, 3)
    plt.bar(bins[:-1],
            height=diff,
            edgecolor='black',
            width=BIN_WIDTH,
            color='red',
            align='edge')
    plt.xlim(v_min, v_max)
    plt.title('Differences per elevation in 10 m intervals', **title_opts())
    plt.ylabel('Count', **label_opts())
    plt.xlabel('Elevation', **label_opts())


def plot(lidar, sfm, style='stacked'):
    if style == 'stacked':
        render_stacked(lidar, sfm)
    elif style == 'side-by-side':
        render_side_by_side(lidar, sfm)

    plt.savefig(OUTPUT_FILE, **output_defaults())


if __name__ == '__main__':
    lidar_file = RasterFile(LIDAR)
    sfm_file = RasterFile(SFM)

    plot(lidar_file, sfm_file)
