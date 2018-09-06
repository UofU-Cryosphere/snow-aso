import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

from base import PlotBase


class Regression(PlotBase):
    def __init__(self, **kwargs):
        super().__init__(kwargs['lidar'], kwargs['sfm'], kwargs['output_path'])
        self._elevation_differences = None

    @property
    def elevation_differences(self):
        if self._elevation_differences is None:
            self._elevation_differences = \
                self.raster_difference.elevation.filled(np.NaN).ravel()
        return self._elevation_differences

    def scatter_plot(self, x, y, **kwargs):
        plt.figure()
        plt.scatter(x, y, s=0.5)
        plt.xlabel(kwargs['xlabel'])
        plt.ylabel(kwargs['ylabel'])
        plt.savefig(
            self.output_path + '/{0}_scatter_plot.png'.format(kwargs['name']),
            **self.output_defaults()
        )

    def plot_lidar_vs_sfm(self):
        self.scatter_plot(
            self.sfm.elevation,
            self.lidar.elevation,
            name='lidar_vs_sfm',
            xlabel='SfM',
            ylabel='Lidar',
        )

    def plot_difference_vs_source(self, source, name):
        for variable in self.TYPES:
            name = name + '_' + variable
            self.print_status(name)
            self.scatter_plot(
                self.elevation_differences,
                getattr(source, variable),
                name=name,
                xlabel='Difference in Elevation',
                ylabel=name + ': ' + str(variable),
            )

    def plot_all(self):
        self.plot_lidar_vs_sfm()
        self.plot_difference_vs_source(self.lidar, 'Lidar')
        self.plot_difference_vs_source(self.sfm, 'SfM')

    @staticmethod
    def fit_model(y, x, name):
        print('\n** OLS for: ' + name + ' **\n')
        model = sm.OLS(y, x, missing='drop',).fit()
        print(model.summary())

    def fit_difference_vs_source(self, source, name):
        for variable in self.TYPES:
            self.fit_model(
                self.elevation_differences,
                getattr(source, variable).ravel(),
                name + ': ' + variable,
            )

    def fit_lidar_vs_sfm(self):
        self.fit_model(
            self.lidar.elevation.ravel(),
            self.sfm.elevation.ravel(),
            'Lidar vs. SfM',
        )

    def fit_all(self):
        self.fit_lidar_vs_sfm()
        self.fit_difference_vs_source(self.lidar, 'Lidar')
        self.fit_difference_vs_source(self.sfm, 'SfM')

    def run(self):
        self.plot_all()
        self.fit_all()
