import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

from .plot_base import PlotBase
from .plot_layout import PlotLayout


# Plot DEMs side by side
class SideBySide(PlotBase):
    OUTPUT_FILE_NAME = 'elevation_comparison.png'

    ORIENTATIONS = ['vertical', 'horizontal']
    COLOR_MAP = 'jet'

    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        self._orientation = kwargs.get('orientation', self.ORIENTATIONS[0])

    @property
    def orientation(self):
        return self._orientation

    @property
    def plot_vertical(self):
        return self.orientation == self.ORIENTATIONS[0]

    @property
    def plot_horizontal(self):
        return self.orientation == self.ORIENTATIONS[1]

    def setup_plot(self):
        if self.plot_vertical:
            figure, axes = PlotLayout.two_col()
        elif self.plot_horizontal:
            figure, axes = PlotLayout.two_row()
        else:
            raise ValueError('Unknown orientation for SideBySide plot')

        axes[0].get_shared_y_axes().join(*axes[:2])

        for n, ax in enumerate(axes[:2]):
            ax.set_facecolor('0.9')

        return axes

    def im_opts(self, lidar, sfm):
        return dict(
            cmap=cm.get_cmap(self.COLOR_MAP),
            alpha=0.3,
            vmin=min(lidar.min(), sfm.min()),
            vmax=max(lidar.max(), lidar.min()),
        )

    @staticmethod
    def add_colorbar(cax, data):
        return plt.colorbar(data, cax=cax)

    def plot(self):
        self.print_status()

        lidar = self.lidar.band_values()
        sfm = self.sfm.band_values()

        (ax1, ax2, cax) = self.setup_plot()

        self.add_hillshade_background(ax1, self.lidar)
        self.sfm.join_masks('hill_shade', lidar)
        self.add_hillshade_background(ax2, self.sfm)

        im_opts = self.im_opts(lidar, sfm)

        ax1.imshow(
            lidar, extent=self.lidar.extent, **im_opts
        )
        ax1.set_title(PlotBase.LIDAR_LABEL)

        sfm.mask = np.ma.mask_or(sfm.mask, lidar.mask)
        image = ax2.imshow(
            sfm, extent=self.sfm.extent, **im_opts
        )
        if self.plot_vertical:
            ax2.set_yticklabels([])
        ax2.set_title(PlotBase.SFM_LABEL)

        cbar = self.add_colorbar(cax, image)
        cbar.set_label(self.SCALE_BAR_LABEL['Elevation'])

        plt.savefig(self.output_file)
