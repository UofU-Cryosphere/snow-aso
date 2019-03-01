import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from .plot_base import PlotBase


class OrthoRgbAverage(PlotBase):
    COLOR_LIST = ['gold', 'darkorange', 'red', 'brown', 'maroon']
    NUM_COLORS = len(COLOR_LIST)
    MAX_PIXEL_VALUE = 255.0
    LOWER_BOUND = 215

    def cmap(self):
        return LinearSegmentedColormap.from_list(
            'gdrb', self.COLOR_LIST, N=self.NUM_COLORS
        )

    def norm(self):
        return colors.BoundaryNorm(
            boundaries=[self.LOWER_BOUND, 220, 225, 230, 254, 255],
            ncolors=self.NUM_COLORS
        )

    def rgb_average(self):
        average = np.mean(self.ortho_image, axis=2)
        average_masked = np.ma.array(average)
        average_masked.mask = self.data.band_values().mask

        average_masked[average_masked < self.LOWER_BOUND] = np.NaN

        return average_masked

    def plot(self):
        rgb_values = self.rgb_average()

        fig, (ax1, cax) = plt.subplots(
            nrows=2, figsize=(8, 7), gridspec_kw={'height_ratios': [1, 0.07]}
        )

        self.add_ortho_background(ax1, self.data)

        img = ax1.imshow(
            rgb_values,
            extent=self.data.extent,
            cmap=self.cmap(), norm=self.norm(),
            vmin=self.LOWER_BOUND, vmax=self.MAX_PIXEL_VALUE,
            zorder=1, alpha=0.7
        )
        ax1.set_title('Pixel Brightness')
        fig.colorbar(img, cax=cax, orientation='horizontal')
        plt.show()

        plt.hist(
            rgb_values.compressed(),
            bins=np.arange(self.LOWER_BOUND, self.MAX_PIXEL_VALUE + 1, 1)
        )
        plt.yscale('log')
        plt.show()
