import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from matplotlib.gridspec import GridSpec

from base.plot_base import PlotBase


# Plot differences between rasters and show histogram of the differences
class AreaDifferences(PlotBase):
    TITLE = '{0} differences'
    TITLE_HIST = '{0} difference distribution'

    HIST_TEXT = '50%:  {:10.2f}\n' \
                'NMAD: {:10.2f}\n' \
                '68.3%: {:10.2f}\n' \
                '95%: {:10.2f}'
    HIST_BIN_WIDTH = 0.05
    BOX_PLOT_TEXT = '{0:8}: {1:.3f}'
    BOX_PLOT_WHISKERS = [5, 95]

    OUTPUT_FILE = '{0}{1}_differences.png'

    def add_hist_stats(self, ax):
        box_text = AreaDifferences.HIST_TEXT.format(
            self.raster_difference.mad.median,
            self.raster_difference.mad.normalized(),
            self.raster_difference.mad.percentile(68.3),
            self.raster_difference.mad.percentile(95),
        )
        PlotBase.add_to_legend(ax, box_text)

    def add_box_plot_stats(self, ax, box_plot_data):
        text = [
            self.BOX_PLOT_TEXT.format(
                str(self.BOX_PLOT_WHISKERS[1]) + '%',
                box_plot_data['caps'][1].get_ydata()[0]
            ),
            self.BOX_PLOT_TEXT.format(
                'Upper Q3', box_plot_data['whiskers'][1].get_ydata()[0]
            ),
            self.BOX_PLOT_TEXT.format(
                'Median', box_plot_data['medians'][0].get_ydata()[0]
            ),
            self.BOX_PLOT_TEXT.format(
                'Lower Q2', box_plot_data['whiskers'][0].get_ydata()[0]
            ),
            self.BOX_PLOT_TEXT.format(
                str(self.BOX_PLOT_WHISKERS[0]) + '%',
                box_plot_data['caps'][0].get_ydata()[0]
            ),
        ]
        PlotBase.add_to_legend(ax, '\n'.join(text))

    @staticmethod
    def elevation_bounds(difference):
        bins = np.arange(difference.min(), difference.max() + 0.1, 0.1)
        return dict(norm=colors.BoundaryNorm(boundaries=bins, ncolors=256))

    def plot(self, raster_attr):
        self.print_status(str(raster_attr))

        fig = plt.figure(constrained_layout=False)
        fig.set_size_inches(12, 10)
        grid_spec = GridSpec(2, 2, figure=fig)

        difference = getattr(self.raster_difference, raster_attr)

        if raster_attr is 'elevation':
            bounds = self.elevation_bounds(difference)
            bins = np.arange(
                difference.min(),
                difference.max() + self.HIST_BIN_WIDTH,
                self.HIST_BIN_WIDTH
            )
        else:
            bounds = dict()
            bins = 'auto'

        ax1 = fig.add_subplot(grid_spec[0, :])
        diff_plot = ax1.imshow(
            difference,
            cmap=cm.get_cmap('PuOr'),
            alpha=0.8,
            extent=self.sfm.extent,
            **bounds
        )
        ax1.set_title(
            self.TITLE.format(raster_attr.capitalize()), **PlotBase.title_opts()
        )
        self.insert_colorbar(
            plt, ax1, diff_plot, self.SCALE_BAR_LABEL[raster_attr]
        )

        ax2 = fig.add_subplot(grid_spec[1, :1])
        ax2.hist(difference.compressed(), bins=bins, label='Count')
        ax2.set_title(
            self.TITLE_HIST.format(raster_attr.capitalize()),
            **PlotBase.title_opts()
        )
        ax2.set_xlabel(
            self.SCALE_BAR_LABEL[raster_attr], **PlotBase.label_opts()
        )
        self.add_hist_stats(ax2)

        ax3 = fig.add_subplot(grid_spec[1:, -1])
        box = ax3.boxplot(
            difference.compressed(),
            sym='k+',
            whis=self.BOX_PLOT_WHISKERS,
        )
        ax3.tick_params(
            axis='x', which='both', bottom=False, top=False, labelbottom=False
        )
        self.add_box_plot_stats(ax3, box)

        plt.tight_layout()
        plt.savefig(
            self.OUTPUT_FILE.format(self.output_path, raster_attr),
            dpi=PlotBase.DEFAULT_DPI
        )
