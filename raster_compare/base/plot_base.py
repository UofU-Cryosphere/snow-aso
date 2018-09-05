from base.raster_difference import RasterDifference
import matplotlib.patches as mpatches


class PlotBase(object):
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

    def __init__(self, lidar, sfm, output_path):
        self._output_path = output_path
        self.raster_difference = RasterDifference(lidar, sfm)

    @property
    def output_path(self):
        return self._output_path

    @property
    def lidar(self):
        return self.raster_difference.lidar

    @property
    def sfm(self):
        return self.raster_difference.sfm

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

    @staticmethod
    def title_opts(**kwargs):
        return dict(fontdict={'fontsize': PlotBase.TITLE_FONT_SIZE}, **kwargs)

    @staticmethod
    def label_opts(**kwargs):
        return dict(fontsize=PlotBase.LABEL_FONT_SIZE, **kwargs)

    @staticmethod
    def output_defaults(**kwargs):
        return dict(bbox_inches='tight', dpi=PlotBase.DEFAULT_DPI, **kwargs)

    @staticmethod
    def add_to_legend(axes, text):
        mean = mpatches.Patch(color='none', label=text)
        handles, labels = axes.get_legend_handles_labels()
        handles.append(mean)
        axes.legend(handles=handles)

