NUM_BINS = 50
BIN_WIDTH = 10  # 10m

TITLE_FONT_SIZE = 20
LABEL_FONT_SIZE = 16

LIDAR_LABEL = 'Lidar'
SFM_LABEL = 'SfM'

DEFAULT_DPI = 200

BOUNDING_BOX = dict(
    boxstyle='square', edgecolor='black', facecolor='grey', alpha=0.2, pad=0.6
)


def text_box_args(x, y, text, **kwargs):
    return dict(
        x=x, y=y, s=text, ha='left', va='top', bbox=BOUNDING_BOX, **kwargs
    )


def title_opts(**kwargs):
    return dict(fontdict={'fontsize': TITLE_FONT_SIZE}, **kwargs)


def label_opts(**kwargs):
    return dict(fontsize=LABEL_FONT_SIZE, **kwargs)


def output_defaults(**kwargs):
    return dict(bbox_inches='tight', dpi=DEFAULT_DPI, **kwargs)
