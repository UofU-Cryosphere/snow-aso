import argparse
import os

import matplotlib as mpl
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np

from base import RasterFile, PlotBase, MedianAbsoluteDeviation

parser = argparse.ArgumentParser()
parser.add_argument(
    '--ortho-image',
    type=str,
    help='Path to ortho photo used as background',
    required=True
)
parser.add_argument(
    '--difference-dem',
    type=str,
    help='Path to raster file with differences in elevation',
    required=True
)

if __name__ == '__main__':
    arguments = parser.parse_args()

    ortho_img = plt.imread(arguments.ortho_image)

    diff = RasterFile(arguments.difference_dem)
    mad = MedianAbsoluteDeviation(diff.elevation.compressed())

    inside = np.ma.mask_or(
        diff.elevation.mask,
        np.ma.masked_outside(
            diff.elevation,
            mad.data_median - mad.standard_deviation(2),
            mad.data_median + mad.standard_deviation(2)
        ).mask
    )
    outside = np.ma.mask_or(
        diff.elevation.mask,
        np.ma.masked_inside(
            diff.elevation,
            mad.data_median + mad.standard_deviation(2),
            mad.data_median - mad.standard_deviation(2)
        ).mask
    )

    cmap = mpl.colors.ListedColormap(['dodgerblue', 'cyan', 'yellow', 'orange'])
    cmap.set_over('darkred')
    cmap.set_under('darkblue')

    bounds = [
        mad.data_median - mad.standard_deviation(2),
        mad.data_median - mad.standard_deviation(1),
        mad.data_median,
        mad.data_median + mad.standard_deviation(1),
        mad.data_median + mad.standard_deviation(2)
    ]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    fig, (ax1, ax2, cax) = plt.subplots(
        nrows=3, gridspec_kw={'height_ratios': [1, 1, 0.07], 'hspace': 0.3 }
    )

    diff_options = dict(
        zorder=1, norm=norm, cmap=cmap, extent=diff.extent, alpha=0.5,
    )

    ax1.imshow(ortho_img, zorder=0, extent=diff.extent)
    diff.elevation.mask = inside
    ax1.imshow(diff.elevation, **diff_options)
    ax1.set_title('95th percentile deviation', size=PlotBase.TITLE_FONT_SIZE)

    ax2.imshow(ortho_img, zorder=0, extent=diff.extent)
    diff.elevation.mask = outside
    img = ax2.imshow(diff.elevation, **diff_options)
    ax2.set_title('Outliers', size=PlotBase.TITLE_FONT_SIZE)

    fig.colorbar(
        img, cax=cax, orientation='horizontal', extend='both',
        extendfrac='auto', spacing='uniform', boundaries=[-20.] + bounds + [20.]
    )

    fig.set_size_inches(6, 10)
    base_path = os.path.dirname(arguments.ortho_image)
    plt.savefig(
        os.path.join(base_path, 'elevation_difference_overlay.png'),
        **PlotBase.output_defaults()
    )
