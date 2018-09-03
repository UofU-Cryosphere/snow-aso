import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition

from base.common import ROOT_PATH, SFM, LIDAR
from base.plot_base import PlotBase

OUTPUT_FILE = ROOT_PATH + '/{0}_differences.png'


class AreaDifferences(PlotBase):
    TYPES = ['elevation', 'slope', 'aspect']
    SCALE_BAR_LABEL = {
        'aspect': 'Degree',
        'elevation': 'Meter',
        'slope': 'Angle',
    }
    TITLE = '{0} differences'
    TITLE_HIST = '{0} difference distribution'

    BOX_PLOT_TEXT = '{0}: {1:.3f}'
    BOX_PLOT_WHISKERS = [2.5, 97.5]

    @staticmethod
    def add_hist_stats(ax, diff):
        mean = diff.mean()
        sd = diff.std()
        box_text = 'Mean: ' + str(mean.round(2)) + '\nSD: ' + str(sd.round(2))
        PlotBase.add_to_legend(ax, box_text)

    def add_box_plot_stats(self, ax, box_plot_data):
        text = [
            self.BOX_PLOT_TEXT.format(
                str(self.BOX_PLOT_WHISKERS[1]) + '%',
                box_plot_data['caps'][1].get_ydata()[0]
            ),
            self.BOX_PLOT_TEXT.format(
                'Upper', box_plot_data['whiskers'][1].get_ydata()[0]
            ),
            self.BOX_PLOT_TEXT.format(
                'Median', box_plot_data['medians'][0].get_ydata()[0]
            ),
            self.BOX_PLOT_TEXT.format(
                'Lower', box_plot_data['whiskers'][0].get_ydata()[0]
            ),
            self.BOX_PLOT_TEXT.format(
                str(self.BOX_PLOT_WHISKERS[0]) + '%',
                box_plot_data['caps'][0].get_ydata()[0]
            ),
        ]
        PlotBase.add_to_legend(ax, '\n'.join(text))


    @staticmethod
    def setup_figure():
        figure, (ax1, cax, ax2, ax3) = plt.subplots(
            ncols=4,
            gridspec_kw={"width_ratios": [1, 0.1, 1, 1], 'height_ratios': [1]}
        )
        figure.set_size_inches(18, 8)

        return ax1, cax, ax2, ax3

    @staticmethod
    def equal_aspect_axes(x_min, x_max, y_min, y_max):
        x_range = x_max - x_min
        y_range = y_max - y_min
        return x_range / y_range

    @staticmethod
    def elevation_bounds():
        bounds = np.array(
            [-20, -10, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 10, 20]
        )
        return dict(norm=colors.BoundaryNorm(boundaries=bounds, ncolors=256))

    def plot(self, raster_attr):
        ax1, cax, ax2, ax3 = self.setup_figure()

        if raster_attr is 'elevation':
            bounds = self.elevation_bounds()
        else:
            bounds = dict()

        diff_plot = ax1.imshow(
            getattr(self.raster_difference, raster_attr),
            cmap=cm.get_cmap('PuOr'),
            alpha=0.8,
            extent=self.sfm.extent,
            **bounds
        )
        ax1.set_title(
            self.TITLE.format(raster_attr.capitalize()), **PlotBase.title_opts()
        )

        hist = ax2.hist(
            getattr(self.raster_difference, raster_attr).compressed(),
            bins='auto',
            label='Count',
        )
        ax2.set_title(
            self.TITLE_HIST.format(raster_attr.capitalize()),
            **PlotBase.title_opts()
        )
        ax2.set_xlabel(
            self.SCALE_BAR_LABEL[raster_attr], **PlotBase.label_opts()
        )
        ax2.set_aspect(self.equal_aspect_axes(
            x_min=hist[1].min(), x_max=hist[1].max(),
            y_min=hist[0].min(), y_max=hist[0].max(),
        ))
        self.add_hist_stats(
            ax2, getattr(self.raster_difference, raster_attr)
        )

        box = ax3.boxplot(
            getattr(self.raster_difference, raster_attr).compressed(),
            sym='k+',
            whis=self.BOX_PLOT_WHISKERS,
        )
        ax3.set_aspect(self.equal_aspect_axes(
            x_min=ax3.get_xlim()[0], x_max=ax3.get_xlim()[1],
            y_min=ax3.get_ylim()[0], y_max=ax3.get_ylim()[1],
        ))
        self.add_box_plot_stats(ax3, box)

        # Differences scale bar
        ip_2 = InsetPosition(ax1, [1.03, 0, 0.05, 1])
        cax.set_axes_locator(ip_2)
        scale_bar = plt.colorbar(diff_plot, cax=cax)
        scale_bar.set_label(
            label=self.SCALE_BAR_LABEL[raster_attr],
            size=PlotBase.LABEL_FONT_SIZE
        )

        plt.subplots_adjust(hspace=0.1)
        plt.savefig(
            OUTPUT_FILE.format(raster_attr), **PlotBase.output_defaults()
        )


# Plot differences between rasters and show histogram of the differences
if __name__ == '__main__':
    [AreaDifferences(LIDAR, SFM).plot(attr) for attr in AreaDifferences.TYPES]
