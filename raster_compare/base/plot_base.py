from base.raster_file import RasterFile


class PlotBase(object):
    NUM_BINS = 50
    BIN_WIDTH = 10  # 10m

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

    def __init__(self, lidar, sfm):
        self.lidar = lidar if type(lidar) is RasterFile else RasterFile(lidar)
        self.sfm = sfm if type(sfm) is RasterFile else RasterFile(sfm)

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
