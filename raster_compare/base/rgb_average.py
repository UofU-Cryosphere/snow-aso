import cv2
import numpy as np


class RgbAverage(object):
    MAX_PIXEL_VALUE = 255.0

    def __init__(self, image_path):
        self._image_path = image_path
        self._image_bgr = cv2.imread(image_path)
        self._values = None

    @property
    def image_path(self):
        return self._image_path

    @property
    def image_bgr(self):
        return self._image_bgr

    @property
    def values(self):
        if self._values is None:
            self._values = np.mean(self.image_bgr, axis=2)
            self._values[self._values == self.MAX_PIXEL_VALUE] = np.NaN
        return self._values
