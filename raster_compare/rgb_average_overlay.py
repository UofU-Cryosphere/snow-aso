import argparse

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from base import RgbAverage, PlotBase, RasterFile

parser = argparse.ArgumentParser()
parser.add_argument(
    '--ortho-image',
    type=str,
    help='Path to ortho photo used as background',
    required=True
)
parser.add_argument(
    '--raster-dem',
    type=str,
    help='Optional raster for axes labels'
)

COLOR_LIST = ['gold', 'darkorange', 'red', 'brown']
NUM_COLORS = len(COLOR_LIST)
LOWER_BOUND = 215

if __name__ == '__main__':
    arguments = parser.parse_args()

    average = RgbAverage(arguments.ortho_image)
    raster = RasterFile(arguments.raster_dem)

    cmap = LinearSegmentedColormap.from_list('gdrb', COLOR_LIST, N=NUM_COLORS)

    norm = colors.BoundaryNorm(
        boundaries=[LOWER_BOUND, 220, 225, 230, 255],
        ncolors=4
    )

    average.values[average.values < LOWER_BOUND] = np.NaN

    fig, (ax1, cax) = plt.subplots(
        nrows=2, figsize=(6, 5), gridspec_kw={'height_ratios': [1, 0.07]}
    )
    ax1.imshow(plt.imread(
        arguments.ortho_image), zorder=0, extent=raster.extent
    )
    img = ax1.imshow(
        average.values,
        extent=raster.extent,
        cmap=cmap, norm=norm,
        vmin=LOWER_BOUND, vmax=RgbAverage.MAX_PIXEL_VALUE,
        zorder=1, alpha=0.7
    )
    ax1.set_title('Pixel Brightness', **PlotBase.title_opts())
    fig.colorbar(img, cax=cax, orientation='horizontal')
    # plt.tight_layout()
    plt.show(**PlotBase.output_defaults())
