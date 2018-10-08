import argparse
import os

import matplotlib as mpl
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np

from base import RasterFile, PlotBase

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

    values = diff.elevation
    mean = values.mean()
    sd = values.std()
    upper_sd = mean + sd
    lower_sd = mean - sd
    upper = np.percentile(values.compressed(), 97.5)
    lower = np.percentile(values.compressed(), 2.5)

    inside_sd = np.ma.mask_or(
        values.mask,
        np.ma.masked_outside(values, lower_sd, upper_sd).mask
    )
    outside_sd = np.ma.mask_or(
        values.mask,
        np.ma.masked_inside(values, upper_sd, lower_sd).mask
    )

    cmap = mpl.colors.ListedColormap(['dodgerblue', 'cyan', 'yellow', 'orange'])
    cmap.set_over('darkred')
    cmap.set_under('darkblue')

    bounds = [lower, lower_sd, mean, upper_sd, upper]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    fig, (ax1, ax2, cax) = plt.subplots(
        nrows=3, gridspec_kw={'height_ratios': [1, 1, 0.07], 'hspace': 0.3 }
    )

    diff_options = dict(
        zorder=1, norm=norm, cmap=cmap, extent=diff.extent, alpha=0.5,
    )

    ax1.imshow(ortho_img, zorder=0, extent=diff.extent)
    values.mask = inside_sd
    ax1.imshow(values, **diff_options)
    ax1.set_title('Inside Standard deviation', size=PlotBase.TITLE_FONT_SIZE)

    ax2.imshow(ortho_img, zorder=0, extent=diff.extent)
    values.mask = outside_sd
    img = ax2.imshow(values, **diff_options)
    ax2.set_title('Outside Standard deviation', size=PlotBase.TITLE_FONT_SIZE)

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
