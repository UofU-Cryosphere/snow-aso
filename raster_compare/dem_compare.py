import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition

from base.common import ROOT_PATH, SFM, LIDAR
from base.plot_base import PlotBase

OUTPUT_FILE = ROOT_PATH + '/dem_compare.png'


class DemCompare(PlotBase):
    def plot(self):
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
            vmin=self.min_for_attr('elevation'),
            vmax=self.max_for_attr('elevation'),
        )

        ax1.imshow(self.lidar.elevation, extent=self.lidar.extent, **im_opts)
        ax1.set_title(PlotBase.LIDAR_LABEL, **PlotBase.title_opts())

        image = ax2.imshow(
            self.sfm.elevation, extent=self.sfm.extent, **im_opts
        )
        ax2.set_yticklabels([])
        ax2.set_title(PlotBase.SFM_LABEL, **PlotBase.title_opts())

        # Lidar and SfM scale bar
        ip_1 = InsetPosition(ax2, [1.03, 0, 0.05, 1])
        cax.set_axes_locator(ip_1)
        plt.colorbar(image, cax=cax) \
            .set_label(label='Meter', size=PlotBase.LABEL_FONT_SIZE)

        plt.subplots_adjust(hspace=0.1)

        plt.savefig(OUTPUT_FILE, **PlotBase.output_defaults())


# Plot DEMs side by side
if __name__ == '__main__':
    DemCompare(LIDAR, SFM).plot()
