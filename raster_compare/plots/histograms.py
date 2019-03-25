import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure

from .plot_base import PlotBase


class Histogram(PlotBase):
    BOX_TEXT = 'Mean: {0}'

    BIN_WIDTH = 10  # 10m

    OUTPUT_FILE_NAME = 'elevation_histogram.png'

    @staticmethod
    def show_mean(ax, value):
        ax.axvline(value, color='orange', linewidth=2)
        PlotBase.add_to_legend(ax, Histogram.BOX_TEXT.format(value.round(2)))

    # Plot elevation histograms per bin width side by side
    def render_side_by_side(self):
        plt.subplot(1, 1, 1)
        plt.hist(
            [
                self.lidar.band_values().compressed(),
                self.sfm.band_values().compressed()
            ],
            label=['lidar', 'sfm'],
            color=['g', 'b'],
            bins=PlotBase.NUM_BINS,
            alpha=0.4
        )
        plt.legend(loc='upper right')

    def bin_range(self, lidar, sfm):
        min_value = min(lidar.min(), sfm.min())
        max_value = max(lidar.max(), sfm.max())

        return np.arange(min_value, max_value + self.BIN_WIDTH, self.BIN_WIDTH)

    def render_stacked(self):
        figure(figsize=(14, 16))

        lidar = self.lidar.band_values()
        sfm = self.sfm.band_values()

        bins = self.bin_range(lidar, sfm)
        hist_opts = dict(bins=bins, alpha=0.5)

        ax1 = plt.subplot(3, 1, 1)
        h1 = plt.hist(
            lidar.compressed(),
            label=PlotBase.LIDAR_LABEL,
            color='b',
            **hist_opts
        )
        ax1.set_xlim(bins[0], bins[-1] + 1)

        ax2 = plt.subplot(3, 1, 2)
        sfm.mask = np.ma.mask_or(sfm.mask, lidar.mask)
        h2 = plt.hist(
            sfm.compressed(),
            label=PlotBase.SFM_LABEL,
            color='g',
            **hist_opts
        )
        ax2.set_xlim(bins[0], bins[-1] + 1)
        ax2.legend()

        diff = h2[0] - h1[0]
        percent = (diff / h1[0]) * 100

        ax3 = plt.subplot(3, 1, 3)
        plt.bar(bins[:-1],  # Remove the upper boundary from bins
                height=percent,
                edgecolor='black',
                label='Percent',
                width=self.BIN_WIDTH,
                color='red',
                align='edge')
        ax3.set_xlim(bins[0], bins[-1] + 1)

        mean = (np.absolute(diff).sum() / sfm.count()) * 100

        # Add labels
        ax1.set_title('Elevation distribution')
        ax1.set_ylabel('Count')
        Histogram.show_mean(ax1, lidar.mean())

        ax2.set_title('Elevation distribution')
        ax2.set_ylabel('Count')
        Histogram.show_mean(ax2, sfm.mean())

        ax3.set_title('Differences per elevation in 10 m intervals')
        ax3.set_ylabel('Percent')
        ax3.set_xlabel('Elevation')
        PlotBase.add_to_legend(ax3, self.BOX_TEXT.format(mean.round(4)))

    def plot(self, style=None):
        if style is None:
            self.print_status()
            self.render_stacked()
        elif style == 'side-by-side':
            self.print_status(style)
            self.render_side_by_side()

        plt.savefig(self.output_file)
