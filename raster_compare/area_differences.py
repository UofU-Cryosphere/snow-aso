import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1 import make_axes_locatable

from base.plot_base import PlotBase


# Plot differences between rasters and show histogram of the differences
class AreaDifferences(PlotBase):
    TITLE = '{0} differences'
    TITLE_HIST = '{0} difference distribution'

    HIST_TEXT = 'Mean: {:10.2f}\n' \
                'SD: {:10.2f}\n' \
                'Min: {:10.2f}\n' \
                'Max: {:10.2f}'
    BOX_PLOT_TEXT = '{0}: {1:.3f}'
    BOX_PLOT_WHISKERS = [2.5, 97.5]

    OUTPUT_FILE = '{0}{1}_differences.png'

    @staticmethod
    def add_hist_stats(ax, diff):
        box_text = AreaDifferences.HIST_TEXT.format(
            diff.mean(), diff.std(), diff.min(), diff.max()
        )
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
    def elevation_bounds():
        bounds = np.array(
            [-20, -10, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 10, 20]
        )
        return dict(norm=colors.BoundaryNorm(boundaries=bounds, ncolors=256))

    def plot(self, raster_attr):
        self.print_status(str(raster_attr))

        fig = plt.figure(constrained_layout=False)
        fig.set_size_inches(12, 10)
        grid_spec = GridSpec(2, 2, figure=fig)

        if raster_attr is 'elevation':
            bounds = self.elevation_bounds()
        else:
            bounds = dict()

        ax1 = fig.add_subplot(grid_spec[0, :])
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

        legend = make_axes_locatable(ax1)
        cax = legend.append_axes("right", size="5%", pad=0.05)
        scale_bar = plt.colorbar(diff_plot, cax=cax)
        scale_bar.set_label(
            label=self.SCALE_BAR_LABEL[raster_attr],
            size=PlotBase.LABEL_FONT_SIZE
        )

        ax2 = fig.add_subplot(grid_spec[1, :1])
        ax2.hist(
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
        self.add_hist_stats(
            ax2, getattr(self.raster_difference, raster_attr)
        )

        ax3 = fig.add_subplot(grid_spec[1:, -1])
        box = ax3.boxplot(
            getattr(self.raster_difference, raster_attr).compressed(),
            sym='k+',
            whis=self.BOX_PLOT_WHISKERS,
        )
        self.add_box_plot_stats(ax3, box)

        plt.tight_layout()
        plt.savefig(
            self.OUTPUT_FILE.format(self.output_path, raster_attr),
            dpi=PlotBase.DEFAULT_DPI
        )
