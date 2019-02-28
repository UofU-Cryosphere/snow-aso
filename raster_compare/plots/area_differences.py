import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from matplotlib import cm
from matplotlib.gridspec import GridSpec

from .plot_base import PlotBase


# Plot differences between rasters and show histogram of the differences
class AreaDifferences(PlotBase):
    TITLE = '{0} differences'

    HIST_TEXT = '50%:   {:5.2f}\n' \
                'NMAD:  {:5.2f}\n' \
                '68.3%: {:5.2f}\n' \
                '95%:   {:5.2f}'
    HIST_BIN_WIDTH = 0.01
    BOX_PLOT_TEXT = '{0:8}: {1:6.3f}'
    BOX_PLOT_WHISKERS = [5, 95]

    OUTPUT_FILE_NAME = 'elevation_differences.png'

    COLORMAP = cm.get_cmap('PuOr')

    def add_hist_stats(self, ax):
        box_text = AreaDifferences.HIST_TEXT.format(
            self.raster_difference.mad.median,
            self.raster_difference.mad.normalized(),
            self.raster_difference.mad.standard_deviation(),
            self.raster_difference.mad.standard_deviation(2),
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
        PlotBase.add_to_legend(
            ax, '\n'.join(text), handlelength=0, handletextpad=0
        )

    def plot(self):
        self.print_status()

        fig = plt.figure(constrained_layout=False)
        fig.set_size_inches(14, 12)
        heights = [2, 1]
        grid_opts=dict(figure=fig, height_ratios=heights)

        difference = self.raster_difference.band_filtered

        if self.band_data_description is 'Elevation':
            grid_spec = GridSpec(
                nrows=2, ncols=3, width_ratios=[3,2,3], **grid_opts
            )
            bins = np.arange(
                difference.min(),
                difference.max() + self.HIST_BIN_WIDTH,
                self.HIST_BIN_WIDTH
            )
            bounds = dict(
                norm=colors.BoundaryNorm(
                    boundaries=bins, ncolors=self.COLORMAP.N
                )
            )
        else:
            grid_spec = GridSpec(
                nrows=2, ncols=2, width_ratios=[3,2], **grid_opts
            )
            bounds = dict()
            bins = 'auto'

        ax1 = fig.add_subplot(grid_spec[0, :])
        diff_plot = ax1.imshow(
            difference,
            cmap=self.COLORMAP,
            alpha=0.8,
            extent=self.sfm.extent,
            **bounds
        )
        ax1.set_title(self.TITLE.format(self.band_data_description))
        self.insert_colorbar(
            plt, ax1, diff_plot, self.SCALE_BAR_LABEL[self.band_data_description]
        )

        ax2 = fig.add_subplot(grid_spec[1, 0])
        ax2.hist(difference.compressed(), bins=bins, label='Count')
        ax2.set_xlabel(self.SCALE_BAR_LABEL[self.band_data_description])
        ax2.set_ylabel('Count')
        if self.band_data_description is 'Elevation':
            self.add_hist_stats(ax2)

        ax3 = fig.add_subplot(grid_spec[1, 1])
        box = ax3.boxplot(
            difference.compressed(),
            sym='k+',
            whis=self.BOX_PLOT_WHISKERS,
            positions=[0.1]
        )
        ax3.set_xlim([0, .35])
        ax3.tick_params(
            axis='x', which='both', bottom=False, top=False, labelbottom=False
        )
        ax3.set_ylabel(self.SCALE_BAR_LABEL[self.band_data_description])
        self.add_box_plot_stats(ax3, box)

        if self.band_data_description is 'Elevation':
            ax4 = fig.add_subplot(grid_spec[1, 2])
            probplot = sm.ProbPlot(difference.compressed())
            probplot.qqplot(ax=ax4, line='s')
            ax4.get_lines()[0].set(markersize=1)
            ax4.get_lines()[1].set(color='black', dashes=[4, 1])
            ax4.set_title('Normal Q-Q Plot')

        plt.savefig(self.output_file)
