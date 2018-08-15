import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure

from base.common import ROOT_PATH, SFM, LIDAR
from base.plot_base import PlotBase

OUTPUT_FILE = ROOT_PATH + '/elevation_histograms.png'


class ElevationHistogram(PlotBase):
    @staticmethod
    def add_stats_box(ax, data):
        ax.text(
            **PlotBase.text_box_args(
                3380, 90000, 'Mean: ' + str(data.mean().round(2))
            )
        )

    # Plot elevation histograms per bin width side by side
    def render_side_by_side(self):
        plt.subplot(1, 1, 1)
        plt.hist(
            [
                self.lidar.raster_data.compressed(),
                self.sfm.raster_data.compressed()
            ],
            label=['lidar', 'sfm'],
            color=['g', 'b'],
            bins=PlotBase.NUM_BINS,
            alpha=0.4
        )
        plt.legend(loc='upper right')

    # Plot elevation distribution histogram individually and
    # one difference histogram per bin width of 10m
    def render_stacked(self):
        v_min = min(self.lidar.min_elevation, self.sfm.min_elevation)
        v_max = min(self.lidar.max_elevation, self.sfm.max_elevation) + 1
        bins = np.arange(v_min, v_max + PlotBase.BIN_WIDTH, PlotBase.BIN_WIDTH)

        figure(figsize=(14, 16))

        hist_opts = dict(bins=bins, alpha=0.5)

        ax1 = plt.subplot(3, 1, 1)
        h1 = plt.hist(
            self.lidar.raster_data.compressed(),
            label=PlotBase.LIDAR_LABEL,
            color='b',
            **hist_opts
        )
        plt.xlim(v_min, v_max)
        plt.title('Elevation distribution', **PlotBase.title_opts())
        plt.ylabel('Count', **PlotBase.label_opts())
        plt.legend()
        ElevationHistogram.add_stats_box(ax1, self.lidar.raster_data)

        ax2 = plt.subplot(3, 1, 2)
        h2 = plt.hist(
            self.sfm.raster_data.compressed(),
            label=PlotBase.SFM_LABEL,
            color='g', **hist_opts
        )
        plt.xlim(v_min, v_max)
        plt.title('Elevation distribution', **PlotBase.title_opts())
        plt.ylabel('Count', **PlotBase.label_opts())
        plt.legend()
        ElevationHistogram.add_stats_box(ax2, self.sfm.raster_data)

        percent = (h2[0] - h1[0])/h1[0]

        ax3 = plt.subplot(3, 1, 3)
        plt.bar(bins[:-1],
                height=percent,
                edgecolor='black',
                width=PlotBase.BIN_WIDTH,
                color='red',
                align='edge')
        plt.xlim(v_min, v_max)
        plt.title(
            'Differences per elevation in 10 m intervals',
            **PlotBase.title_opts()
        )
        plt.ylabel('Percent', **PlotBase.label_opts())
        plt.xlabel('Elevation', **PlotBase.label_opts())
        ax3.text(
            **PlotBase.text_box_args(
                4000, -0.3, 'Mean: ' + str(percent.mean().round(4))
            )
        )

    def plot(self, style='stacked'):
        if style == 'stacked':
            self.render_stacked()
        elif style == 'side-by-side':
            self.render_side_by_side()

        plt.savefig(OUTPUT_FILE, **PlotBase.output_defaults())


if __name__ == '__main__':
    ElevationHistogram(LIDAR, SFM).plot()
