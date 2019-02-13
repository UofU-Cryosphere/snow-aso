import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

from .plot_base import PlotBase
from raster_compare.base import RasterDifference


class Histogram(PlotBase):
    BOX_TEXT = 'Mean: {0}'

    OUTPUT_FILE = '{0}{1}_histogram.png'

    @staticmethod
    def show_mean(ax, value):
        ax.axvline(value, color='orange', linewidth=2)
        PlotBase.add_to_legend(ax, Histogram.BOX_TEXT.format(value.round(2)))

    # Plot elevation histograms per bin width side by side
    def render_side_by_side(self):
        plt.subplot(1, 1, 1)
        plt.hist(
            [
                self.lidar.elevation.compressed(),
                self.sfm.elevation.compressed()
            ],
            label=['lidar', 'sfm'],
            color=['g', 'b'],
            bins=PlotBase.NUM_BINS,
            alpha=0.4
        )
        plt.legend(loc='upper right')

    def render_elevation(self, ax1, ax2, ax3, mean):
        ax1.set_title('Elevation distribution', **PlotBase.title_opts())
        ax1.set_ylabel('Count', **PlotBase.label_opts())
        Histogram.show_mean(ax1, self.lidar.elevation.mean())

        ax2.set_title('Elevation distribution', **PlotBase.title_opts())
        ax2.set_ylabel('Count', **PlotBase.label_opts())
        Histogram.show_mean(ax2, self.sfm.elevation.mean())

        ax3.set_title(
            'Differences per elevation in 10 m intervals',
            **PlotBase.title_opts()
        )
        ax3.set_ylabel('Percent', **PlotBase.label_opts())
        ax3.set_xlabel('Elevation', **PlotBase.label_opts())
        PlotBase.add_to_legend(ax3, self.BOX_TEXT.format(mean.round(4)))

    def render_slope(self, ax1, ax2, ax3, mean):
        ax1.set_title('Slope distribution', **PlotBase.title_opts())
        ax1.set_ylabel('Degree', **PlotBase.label_opts())
        Histogram.show_mean(ax1, self.lidar.slope.mean())

        ax2.set_title('Slope distribution', **PlotBase.title_opts())
        ax2.set_ylabel('Count', **PlotBase.label_opts())
        Histogram.show_mean(ax2, self.sfm.slope.mean())

        ax3.set_title(
            'Differences per slope angle in 10 degree intervals',
            **PlotBase.title_opts()
        )
        ax3.set_ylabel('Percent', **PlotBase.label_opts())
        ax3.set_xlabel('Count', **PlotBase.label_opts())
        PlotBase.add_to_legend(ax3, self.BOX_TEXT.format(mean.round(2)))

    def render_aspect(self, ax1, ax2, ax3, mean):
        ax1.set_title('Aspect distribution', **PlotBase.title_opts())
        ax1.set_ylabel('Count', **PlotBase.label_opts())
        Histogram.show_mean(ax1, self.lidar.aspect.mean())

        ax2.set_title('Aspect distribution', **PlotBase.title_opts())
        ax2.set_ylabel('Count', **PlotBase.label_opts())
        Histogram.show_mean(ax2, self.sfm.aspect.mean())

        ax3.set_title(
            'Differences per aspect angle in 10 degree intervals',
            **PlotBase.title_opts()
        )
        ax3.set_ylabel('Percent', **PlotBase.label_opts())
        ax3.set_xlabel('Degree', **PlotBase.label_opts())
        PlotBase.add_to_legend(ax3, self.BOX_TEXT.format(mean.round(2)))

    # Plot histogram for given raster attribute and
    # one difference histogram per bin width of 10
    def render_stacked(self, raster_attr):
        figure(figsize=(14, 16))
        bins = self.raster_difference.bin_range(raster_attr)
        min_value = getattr(self.lidar, raster_attr).min()
        max_value = getattr(self.lidar, raster_attr).max()

        hist_opts = dict(bins=bins, alpha=0.5)

        ax1 = plt.subplot(3, 1, 1)
        h1 = plt.hist(
            getattr(self.lidar, raster_attr).compressed(),
            label=PlotBase.LIDAR_LABEL,
            color='b',
            **hist_opts
        )
        ax1.set_xlim(min_value, max_value + 1)

        ax2 = plt.subplot(3, 1, 2)
        self.sfm.join_masks(raster_attr, getattr(self.lidar, raster_attr))
        h2 = plt.hist(
            getattr(self.sfm, raster_attr).compressed(),
            label=PlotBase.SFM_LABEL,
            color='g',
            **hist_opts
        )
        ax2.set_xlim(min_value, max_value + 1)
        ax2.legend()

        diff = h2[0] - h1[0]
        percent = (diff / h1[0]) * 100

        ax3 = plt.subplot(3, 1, 3)
        plt.bar(bins[:-1],  # Remove the upper boundary from bins
                height=percent,
                edgecolor='black',
                label='Percent',
                width=RasterDifference.BIN_WIDTH,
                color='red',
                align='edge')
        ax3.set_xlim(min_value, max_value + 1)

        mean = RasterDifference.percentage_mean(
            diff, getattr(self.sfm, raster_attr).count()
        )
        getattr(self, 'render_{0}'.format(raster_attr))(ax1, ax2, ax3, mean)

    def plot(self, style):
        if style in self.TYPES:
            self.print_status(str(style))
            self.render_stacked(style)
        elif style == 'side-by-side':
            self.print_status(style)
            self.render_side_by_side()

        plt.savefig(
            self.OUTPUT_FILE.format(self.output_path, style),
            **PlotBase.output_defaults()
        )
