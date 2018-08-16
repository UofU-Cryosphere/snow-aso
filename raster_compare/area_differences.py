import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import math

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

    @staticmethod
    def add_stats_box(ax, diff):
        mean = diff.mean()
        sd = diff.std()
        box_text = 'Mean: ' + str(mean.round(2)) + '\nSD: ' + str(sd.round(2))
        PlotBase.add_to_legend(ax, box_text)

    @staticmethod
    def setup_figure():
        figure, (ax1, cax, ax2) = plt.subplots(
            ncols=3,
            gridspec_kw={"width_ratios": [1, 0.1, 1], 'height_ratios': [1]}
        )
        figure.set_size_inches(14, 8)

        return ax1, cax, ax2

    @staticmethod
    def equal_aspect_hist(hist):
        x_range = math.fabs(hist[1].min()) + hist[1].max()
        y_range = math.fabs(hist[0].min()) + hist[0].max()
        return x_range / y_range

    @staticmethod
    def elevation_bounds():
        bounds = np.array(
            [-20, -10, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 10, 20]
        )
        return dict(norm=colors.BoundaryNorm(boundaries=bounds, ncolors=256))

    def plot(self, raster_attr):
        ax1, cax, ax2 = AreaDifferences.setup_figure()

        if raster_attr is 'elevation':
            bounds = AreaDifferences.elevation_bounds()
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
        ax2.set_aspect(AreaDifferences.equal_aspect_hist(hist))
        AreaDifferences.add_stats_box(
            ax2, getattr(self.raster_difference, raster_attr)
        )

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
