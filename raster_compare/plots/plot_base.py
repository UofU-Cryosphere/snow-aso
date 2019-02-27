import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import sys
import os

from raster_compare.base import RasterDifference


class PlotBase(object):
    TYPES = ['elevation', 'slope', 'aspect']
    SCALE_BAR_LABEL = {
        'aspect': 'Degree',
        'elevation': '∆h [m]',
        'slope': 'Angle',
    }

    NUM_BINS = 50

    TITLE_FONT_SIZE = 20
    LABEL_FONT_SIZE = 16

    LIDAR_LABEL = 'Lidar'
    SFM_LABEL = 'SfM'

    DEFAULT_DPI = 200

    BOUNDING_BOX = dict(
        boxstyle='square',
        edgecolor='black',
        facecolor='grey',
        alpha=0.2,
        pad=0.6
    )

    def __init__(self, lidar, sfm, **kwargs):
        self._output_path = kwargs['output_path']
        if 'ortho_image' in kwargs:
            self._ortho_image = plt.imread(kwargs['ortho_image'])
        self.raster_difference = RasterDifference(
            lidar, sfm, kwargs['band_number']
        )
        self.configure_matplotlib()

    @staticmethod
    def configure_matplotlib():
        # Enable running on headless devices
        if sys.stdout.isatty():
            matplotlib.use('Agg')

        # Font sizes
        matplotlib.rcParams['axes.titlesize'] = PlotBase.TITLE_FONT_SIZE
        matplotlib.rcParams['axes.labelsize'] = PlotBase.LABEL_FONT_SIZE

        # Figure settings
        matplotlib.rcParams['figure.titlesize'] = PlotBase.TITLE_FONT_SIZE
        matplotlib.rcParams['figure.dpi'] = PlotBase.DEFAULT_DPI

        # Save settings
        matplotlib.rcParams['savefig.bbox'] = 'tight'

        # Save figure text editable
        matplotlib.rcParams['pdf.fonttype'] = 42
        matplotlib.rcParams['ps.fonttype'] = 42

    @property
    def output_path(self):
        return self._output_path

    @property
    def output_file(self):
        try:
            return os.path.join(self.output_path, self.OUTPUT_FILE_NAME)
        except NameError:
            print('*** OUTPUT_FILE_NAME not defined ***')
            print('*** Figure NOT saved ***')
            return

    @property
    def ortho_image(self):
        return self._ortho_image

    def __getattr__(self, name):
        return getattr(self.raster_difference, name)

    @staticmethod
    def text_box_args(x, y, text, **kwargs):
        return dict(
            x=x,
            y=y,
            s=text,
            ha='left', va='top', bbox=PlotBase.BOUNDING_BOX, **kwargs
        )

    def add_ortho_background(self, ax):
        ax.imshow(self.ortho_image, zorder=0, extent=self.lidar.extent)

    @staticmethod
    def add_hillshade_background(ax, raster_file):
        ax.imshow(
            raster_file.hill_shade,
            extent=raster_file.extent,
            cmap='gray', clim=(1, 255)
        )

    @staticmethod
    def add_to_legend(axes, text, **kwargs):
        mean = mpatches.Patch(color='none', label=text)
        handles, labels = axes.get_legend_handles_labels()
        handles.append(mean)
        axes.legend(handles=handles, prop={'family':'monospace'}, **kwargs)

    @staticmethod
    def insert_colorbar(plot, ax, data, label, **kwargs):
        legend = make_axes_locatable(ax)
        cax = legend.append_axes("right", size="5%", pad=0.05)
        scale_bar = plot.colorbar(data, cax=cax, **kwargs)
        scale_bar.set_label(label=label)
        return scale_bar

    def print_status(self, message=''):
        status = 'Plotting ' + self.__class__.__name__

        if len(message) > 0:
            status += ':\n   ' + message + '\n'

        print(status)
