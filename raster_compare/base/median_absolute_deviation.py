import math

import numpy as np


class MedianAbsoluteDeviation(object):
    """
    Median Absolute Deviation
    """

    MAD_CONSTANT = 1.4826

    def __init__(self, data):
        self._data = data
        self._data_mean = np.median(self.data)
        self._percentiles = {}

    @property
    def data(self):
        return self._data

    @property
    def data_median(self):
        return self._data_mean

    @property
    def median(self):
        return self.percentile(50)

    def absolute_difference(self, a):
        return math.fabs(a - self.data_median)

    def normalized(self):
        """
        NMAD from Höhle & Höhle, 2009
        """
        absolute_difference = np.vectorize(self.absolute_difference)
        return self.MAD_CONSTANT * np.median(absolute_difference(self.data))

    def percentile(self, percent):
        if str(percent) not in self._percentiles:
            absolute_difference = np.vectorize(self.absolute_difference)
            self._percentiles[str(percent)] = \
                np.percentile(absolute_difference(self.data), percent)
        return self._percentiles[str(percent)]
