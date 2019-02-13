import matplotlib.pyplot as plt
from matplotlib import cm

from .plot_base import PlotBase


# Plot DEMs side by side
class AreaPlot(PlotBase):
    OUTPUT_FILE = '{0}{1}_comparison.png'

    def plot(self, raster_attr):
        self.print_status(str(raster_attr))

        figure, (ax1, ax2) = plt.subplots(ncols=2)
        figure.set_size_inches(10, 5)

        axes = (ax1, ax2)
        ax1.get_shared_x_axes().join(ax1, ax2)
        ax1.get_shared_y_axes().join(ax1, ax2)

        for n, ax in enumerate(axes):
            ax.set_facecolor('0.9')

        hillshade_opts = dict(cmap='gray', clim=(1, 255))
        ax1.imshow(
            self.lidar.hill_shade, extent=self.lidar.extent, **hillshade_opts
        )
        self.sfm.join_masks('hill_shade', getattr(self.lidar, raster_attr))
        ax2.imshow(
            self.sfm.hill_shade, extent=self.sfm.extent, **hillshade_opts
        )

        im_opts = dict(
            cmap=cm.get_cmap('jet'),
            alpha=0.3,
            vmin=self.min_for_attr(raster_attr),
            vmax=self.max_for_attr(raster_attr),
        )

        ax1.imshow(
            getattr(self.lidar, raster_attr),
            extent=self.lidar.extent,
            **im_opts
        )
        ax1.set_title(PlotBase.LIDAR_LABEL, **PlotBase.title_opts())

        self.sfm.join_masks(raster_attr, getattr(self.lidar, raster_attr))
        image = ax2.imshow(
            getattr(self.sfm, raster_attr), extent=self.sfm.extent, **im_opts
        )
        ax2.set_yticklabels([])
        ax2.set_title(PlotBase.SFM_LABEL, **PlotBase.title_opts())

        self.insert_colorbar(plt, ax2, image, self.SCALE_BAR_LABEL[raster_attr])

        plt.tight_layout()
        plt.savefig(
            self.OUTPUT_FILE.format(self.output_path, raster_attr),
        )
