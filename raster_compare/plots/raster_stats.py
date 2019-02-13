import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

from .plot_base import PlotBase


class RasterStats(PlotBase):
    BAND_STATS = {
        'min': 1,
        'max': 2,
        'stdev': 6,
    }
    OUTPUT_FILE_NAME = '{0}/raster_stats_{1}_{2}.png'
    PLOT_TITLE = '{0} {1} {2}% percentile'

    def plot(self, band_stat, options):

        diff_per_cell = self.sfm.values_for_band(
            band_number=self.BAND_STATS[band_stat]) - \
                        self.lidar.values_for_band(
                            band_number=self.BAND_STATS[band_stat])

        filter_value = np.percentile(
            np.absolute(diff_per_cell.compressed()), options.percentile
        )

        if options.outliers:
            mask = np.ma.masked_inside(
                diff_per_cell, -filter_value, filter_value
            ).mask
            name_suffix = 'outliers'
        else:
            mask = np.ma.masked_outside(
                diff_per_cell, -filter_value, filter_value
            ).mask
            name_suffix = str(options.percentile) + '_percentile'

        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12, 12))

        diff_per_cell.mask = mask
        diff = ax1.imshow(
            diff_per_cell, extent=self.lidar.extent, cmap='Oranges'
        )

        bins = np.arange(diff_per_cell.min(), diff_per_cell.max() + 1, 1)
        ax2.hist(diff_per_cell.compressed(), bins=bins)

        legend = make_axes_locatable(ax1)
        cax = legend.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(diff, cax=cax)

        self.print_status(str(band_stat) + ' - ' + name_suffix)

        ax1.set_title(
            self.PLOT_TITLE.format(band_stat, name_suffix, options.percentile)
        )
        plt.tight_layout()
        plt.savefig(
            self.OUTPUT_FILE_NAME.format(
                self.output_path, band_stat, name_suffix
            ),
            dpi=self.DEFAULT_DPI
        )
