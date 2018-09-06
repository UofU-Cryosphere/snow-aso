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

    def scatter_plots(self):
        for variable in self.TYPES:
            self.print_status(variable)

            plt.figure()
            plt.scatter(
                self.elevation_differences,
                getattr(self.lidar, variable),
            )
            plt.xlabel('Difference in Elevation')
            plt.ylabel('Lidar: ' + str(variable))
            plt.savefig(
                self.output_path + '/{0}_scatter_plot.png'.format(variable),
                **self.output_defaults()
            )

    def fit_models(self):
        for variable in self.TYPES:
            print('\n** OLS for: ' + str(variable) + ' **\n')
            model = sm.OLS(
                self.elevation_differences,
                getattr(self.lidar, variable).ravel(),
                missing='drop',
            ).fit()
            print(model.summary())

    def run(self):
        self.scatter_plots()
        self.fit_models()
