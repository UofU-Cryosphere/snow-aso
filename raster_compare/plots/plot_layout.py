import matplotlib.pyplot as plt


class PlotLayout(object):
    @staticmethod
    def two_row():
        """
        Two row design with legend axes at the bottom
        :return:
        """
        return plt.subplots(
            nrows=3, figsize=(6, 12),
            gridspec_kw={'height_ratios': [1, 1, 0.07], 'hspace': 0.3}
        )

    @staticmethod
    def two_col():
        """
        Two column design with legend axes on the right
        :return:
        """
        return plt.subplots(
            ncols=3, figsize=(12, 4),
            gridspec_kw={'width_ratios': [1, 1, 0.05], 'wspace': 0.05}
        )
