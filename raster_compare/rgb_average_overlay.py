import argparse

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from base import RgbAverage

parser = argparse.ArgumentParser()
parser.add_argument(
    '--ortho-image',
    type=str,
    help='Path to ortho photo used as background',
    required=True
)

COLOR_LIST = ['gold', 'darkorange', 'red', 'brown']
NUM_COLORS = len(COLOR_LIST)
LOWER_BOUND = 215

if __name__ == '__main__':
    arguments = parser.parse_args()

    luminance = RgbAverage(arguments.ortho_image)

    cmap = LinearSegmentedColormap.from_list('gdrb', COLOR_LIST, N=NUM_COLORS)

    norm = colors.BoundaryNorm(
        boundaries=[LOWER_BOUND, 220, 225, 230, 255],
        ncolors=4
    )

    luminance.values[luminance.values < LOWER_BOUND] = np.NaN

    plt.figure(figsize=(12, 8))
    plt.imshow(plt.imread(arguments.ortho_image), zorder=0)
    plt.imshow(
        luminance.values,
        cmap=cmap, norm=norm,
        vmin=LOWER_BOUND, vmax=RgbAverage.MAX_PIXEL_VALUE,
        zorder=1, alpha=0.7
    )
    plt.colorbar()
    plt.show()
