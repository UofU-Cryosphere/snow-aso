import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import math
from matplotlib import cm

from raster_compare.base import PdalMapper
from .plot_base import PlotBase


class RasterPointSpread(PlotBase):
    PLOT_TITLE = 'Point elevation spread difference per cell'
    OUTPUT_FILE_NAME = 'raster_point_spread.png'
    HIST_BIN_WIDTH = 0.1
    MIN_OUTLIER_VALUE = None    # Adjust with histogram

    def __init__(self, raster, **kwargs):
        self._output_path = kwargs['output_path']
        self._raster = raster
        self.configure_matplotlib()

    @property
    def raster(self):
        return self._raster

    def min_values(self):
        self.raster.band_number = PdalMapper.RASTER_BANDS['min']
        return self.raster.elevation

    def max_values(self):
        self.raster.band_number = PdalMapper.RASTER_BANDS['max']
        return self.raster.elevation

    def bounds(self, diff):
        max_val = math.ceil(diff.max())
        min_val = math.floor(diff.min())

        bounds = np.arange(min_val, self.MIN_OUTLIER_VALUE, 1)
        bounds = np.append(bounds, [max_val])
        return bounds

    def plot(self):
        diff_per_cell = self.max_values() - self.min_values()

        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 10))

        bounds = self.bounds(diff_per_cell)
        norm = colors.BoundaryNorm(boundaries=bounds, ncolors=256)

        # === Area plot ===
        diff = ax1.imshow(
            diff_per_cell,
            # vmin=, vmax=, # Limit displayed value range
            extent=self.raster.extent,
            cmap=cm.get_cmap('magma_r'),
            norm=norm,
        )
        ax1.set_title(self.PLOT_TITLE)
        self.insert_colorbar(
            plt, ax1, diff, self.SCALE_BAR_LABEL['elevation'],
            # boundaries=bounds[7::], # Limit displayed value range
            # ticks=bounds[1::2], # Adapt tick marks
        )

        # === Histogram ===
        bins = np.arange(bounds[0], bounds[-1] + 1, self.HIST_BIN_WIDTH)

        ax2.hist(diff_per_cell.compressed(), bins=bins)
        ax2.set_xticks(bins[10::20])
        ax2.set_xlim(bins[0], bins[-1])
        ax2.set_xlabel('Spread [m]')
        ax2.set_yscale('log')
        ax2.set_ylabel('Count')
        ax2.axvline(
            diff_per_cell.mean(),
            color='orange', linewidth=2,
            label='Mean: {:.2f}'.format(diff_per_cell.mean())
        )
        ax2.legend()

        plt.savefig(self.output_file)
