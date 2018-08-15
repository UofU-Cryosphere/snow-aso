import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition

from base.common import ROOT_PATH, SFM, LIDAR
from base.plot_base import PlotBase

OUTPUT_FILE = ROOT_PATH + '/dem_diff.png'


class DemDifferences(PlotBase):
    @staticmethod
    def add_stats_box(ax, diff):
        mean = diff.mean()
        sd = diff.std()
        box_text = 'Mean: ' + str(mean.round(2)) + '\nSD: ' + str(sd.round(2))
        ax.text(
            **PlotBase.text_box_args(
                11, 24000, box_text, **PlotBase.label_opts()
            )
        )

    def plot(self):
        figure, (ax1, cax, ax2) = plt.subplots(
            ncols=3,
            gridspec_kw={"width_ratios": [1, 0.1, 1], 'height_ratios': [1]}
        )
        figure.set_size_inches(14, 8)

        diff = self.sfm.raster_data - self.lidar.raster_data

        diff.mask[diff.data > 20] = 20
        diff.mask[diff.data < -10] = -10

        bounds = np.array(
            [-20, -10, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 10, 20]
        )
        norm = colors.BoundaryNorm(boundaries=bounds, ncolors=256)

        diff_plot = ax1.imshow(
            diff,
            cmap=cm.get_cmap('PuOr'),
            norm=norm,
            alpha=0.8,
            extent=self.sfm.extent
        )
        ax1.set_title('Difference', **PlotBase.title_opts())

        ax2.hist(diff.compressed(), bins='auto')
        ax2.set_title('Differences in Meter', **PlotBase.title_opts())
        ax2.set_xlabel('Meter', **PlotBase.label_opts())
        ax2.set_aspect(0.000935)
        DemDifferences.add_stats_box(ax2, diff)

        # Differences scale bar
        ip_2 = InsetPosition(ax1, [1.03, 0, 0.05, 1])
        cax.set_axes_locator(ip_2)
        plt.colorbar(diff_plot, cax=cax) \
            .set_label(label='Meter', size=PlotBase.LABEL_FONT_SIZE)

        plt.subplots_adjust(hspace=0.1)
        plt.savefig(OUTPUT_FILE, **PlotBase.output_defaults())


# Plot differences between rasters and show histogram of the differences
if __name__ == '__main__':
    DemDifferences(LIDAR, SFM).plot()
