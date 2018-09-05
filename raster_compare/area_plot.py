import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition

from base.plot_base import PlotBase


# Plot DEMs side by side
class AreaPlot(PlotBase):
    TYPES = ['elevation', 'slope', 'aspect']
    SCALE_BAR_LABEL = {
        'aspect': 'Degree',
        'elevation': 'Meter',
        'slope': 'Angle',
    }

    OUTPUT_FILE = '{0}{1}_comparison.png'

    def plot(self, raster_attr):
        self.print_status(str(raster_attr))

        figure, (ax1, ax2, cax) = plt.subplots(
            ncols=3,
            gridspec_kw={"width_ratios": [1, 1, 0.1]}
        )
        figure.set_size_inches(10, 8)

        axes = (ax1, ax2)
        ax1.get_shared_x_axes().join(ax1, ax2)
        ax1.get_shared_y_axes().join(ax1, ax2)

        for n, ax in enumerate(axes):
            ax.set_facecolor('0.9')

        hillshade_opts = dict(cmap='gray', clim=(1, 255))
        ax1.imshow(
            self.lidar.hill_shade, extent=self.lidar.extent, **hillshade_opts
        )
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

        image = ax2.imshow(
            getattr(self.sfm, raster_attr), extent=self.sfm.extent, **im_opts
        )
        ax2.set_yticklabels([])
        ax2.set_title(PlotBase.SFM_LABEL, **PlotBase.title_opts())

        # Lidar and SfM scale bar
        ip_1 = InsetPosition(ax2, [1.03, 0, 0.05, 1])
        cax.set_axes_locator(ip_1)
        scale_bar = plt.colorbar(image, cax=cax)
        scale_bar.set_label(
            label=self.SCALE_BAR_LABEL[raster_attr],
            size=PlotBase.LABEL_FONT_SIZE
        )

        plt.subplots_adjust(hspace=0.1)
        plt.savefig(
            self.OUTPUT_FILE.format(self.output_path, raster_attr),
            **PlotBase.output_defaults()
        )
