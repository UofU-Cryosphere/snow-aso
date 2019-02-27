import argparse

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from raster_compare.base import PdalMapper, RgbAverage, RasterFile

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

COLOR_LIST = ['gold', 'darkorange', 'red', 'brown', 'maroon']
NUM_COLORS = len(COLOR_LIST)
LOWER_BOUND = 215

if __name__ == '__main__':
    arguments = parser.parse_args()

    average = RgbAverage(arguments.ortho_image)
    raster = RasterFile(arguments.raster_dem, PdalMapper.RASTER_BANDS['mean'])

    cmap = LinearSegmentedColormap.from_list('gdrb', COLOR_LIST, N=NUM_COLORS)

    norm = colors.BoundaryNorm(
        boundaries=[LOWER_BOUND, 220, 225, 230, 254, 255],
        ncolors=NUM_COLORS
    )

    average_masked = np.ma.array(average.values)
    average_masked.mask = raster.elevation.mask

    average_masked[average_masked < LOWER_BOUND] = np.NaN

    fig, (ax1, cax) = plt.subplots(
        nrows=2, figsize=(8, 7), gridspec_kw={'height_ratios': [1, 0.07]}
    )
    ax1.imshow(plt.imread(
        arguments.ortho_image), zorder=0, extent=raster.extent
    )
    img = ax1.imshow(
        average_masked,
        extent=raster.extent,
        cmap=cmap, norm=norm,
        vmin=LOWER_BOUND, vmax=RgbAverage.MAX_PIXEL_VALUE,
        zorder=1, alpha=0.7
    )
    ax1.set_title('Pixel Brightness')
    fig.colorbar(img, cax=cax, orientation='horizontal')
    plt.show()

    a = plt.hist(
        average_masked.compressed(),
        bins=np.arange(LOWER_BOUND, RgbAverage.MAX_PIXEL_VALUE + 1, 1)
    )
    plt.yscale('log')
    plt.show()
