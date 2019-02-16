import decimal

import numpy as np


class DecimalConverter(object):
    @staticmethod
    def parse_value(value):
        if len(value) == 0:
            return np.NaN
        return decimal.Decimal(value)
