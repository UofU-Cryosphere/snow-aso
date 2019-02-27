import matplotlib.pyplot as plt
from matplotlib import cm

from .plot_base import PlotBase


# Plot DEMs side by side
class SideBySide(PlotBase):
    OUTPUT_FILE = '{0}{1}_comparison.png'

    COLOR_MAP = 'jet'

    @staticmethod
    def setup_plot():
        figure, axes = plt.subplots(
            figsize=(12, 4), ncols=3,
            gridspec_kw={'width_ratios': [1, 1, 0.05], 'wspace': 0.05}
        )

        axes[0].get_shared_y_axes().join(*axes[:2])

        for n, ax in enumerate(axes[:2]):
            ax.set_facecolor('0.9')

        return axes

    def im_opts(self, raster_attr):
        return dict(
            cmap=cm.get_cmap(self.COLOR_MAP),
            alpha=0.3,
            vmin=self.min_for_attr(raster_attr),
            vmax=self.max_for_attr(raster_attr),
        )

    @staticmethod
    def add_colorbar(cax, data):
        return plt.colorbar(data, cax=cax)

    def plot(self, raster_attr):
        self.print_status(str(raster_attr))

        (ax1, ax2, cax) = self.setup_plot()

        self.add_hillshade_background(ax1, self.lidar)
        self.sfm.join_masks('hill_shade', getattr(self.lidar, raster_attr))
        self.add_hillshade_background(ax2, self.sfm)

        ax1.imshow(
            getattr(self.lidar, raster_attr),
            extent=self.lidar.extent,
            **self.im_opts(raster_attr)
        )
        ax1.set_title(PlotBase.LIDAR_LABEL)

        self.sfm.join_masks(raster_attr, getattr(self.lidar, raster_attr))
        image = ax2.imshow(
            getattr(self.sfm, raster_attr),
            extent=self.sfm.extent,
            **self.im_opts(raster_attr)
        )
        ax2.set_yticklabels([])
        ax2.set_title(PlotBase.SFM_LABEL)

        cbar = self.add_colorbar(cax, image)
        cbar.set_label(self.SCALE_BAR_LABEL[raster_attr])

        plt.savefig(
            self.OUTPUT_FILE.format(self.output_path, raster_attr),
        )
