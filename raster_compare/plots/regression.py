import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

from .plot_base import PlotBase


class Regression(PlotBase):
    EXPLANATORY_VARS = [
        'lidar_elevation', 'lidar_slope', 'lidar_aspect',
        'sfm_elevation', 'sfm_slope', 'sfm_aspect',
    ]

    def __init__(self, **kwargs):
        super().__init__(
            kwargs['lidar'], kwargs['sfm'],
            output_path=kwargs['output_path'],
            band_number=kwargs['band_number'],
        )
        self.df = self.load_data_frame()

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, value):
        self._df = value

    def load_data_frame(self):
        return pd.DataFrame({
            'diff': self.raster_difference.band_filtered.filled(np.NaN).ravel(),
            'lidar_elevation': self.lidar.band_values().filled(np.NaN).ravel(),
            'sfm_elevation': self.sfm.band_values().filled(np.NaN).ravel(),
            'lidar_slope': self.lidar.slope.filled(np.NaN).ravel(),
            'sfm_slope': self.sfm.slope.filled(np.NaN).ravel(),
            'lidar_aspect': self.lidar.aspect.filled(np.NaN).ravel(),
            'sfm_aspect': self.sfm.aspect.filled(np.NaN).ravel(),
        })

    def save_plot(self, **kwargs):
        plt.savefig(
            self.output_path + '/{0}_scatter_plot.png'.format(kwargs['name'])
        )

    def plot_lidar_vs_sfm(self):
        self.print_status('Lidar vs. SfM elevations')
        plt.figure()
        plt.scatter(self.sfm.band_filtered, self.lidar.band_filtered, s=0.5)
        plt.xlabel('Lidar')
        plt.ylabel('SfM')
        self.save_plot(name='Lidar_vs_sfm')

    def plot_for_query(self, query, name):
        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))
        row = 0
        col = 0
        for variable in self.EXPLANATORY_VARS:
            self.print_status(name + ' difference values vs. ' + variable)
            query.plot(
                kind='scatter', x=variable, y='diff', s=0.5, ax=axes[row, col]
            )
            axes[row, col].set_title(variable)
            axes[row, col].set_xlabel('')
            if col == 0:
                axes[row, col].set_ylabel('Difference in Elevation')
            else:
                axes[row, col].set_ylabel('')

            if col == 2:
                col = 0
                row += 1
            else:
                col += 1

        self.save_plot(name=name + '_elevation_diff')

    def plot_difference_vs_source(self):
        self.plot_for_query(self.df.query('diff < 0'), 'negative')
        self.plot_for_query(self.df.query('diff > 0'), 'positive')

    @staticmethod
    def aspect_to_category(degree):
        if 45 < degree <= 135:
            return 'East'
        elif 135 < degree <= 225:
            return 'South'
        elif 225 < degree <= 315:
            return 'West'
        elif degree is np.NAN:
            return np.NaN
        else:
            return 'North'

    def categorize_aspect(self, column_name, from_column_name):
        self.df[column_name] = self.df.apply(
            lambda row: self.aspect_to_category(row[from_column_name]), axis=1
        )
        self.df[column_name].astype('category')

    def hexbin_plot(self):
        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))
        row = 0
        col = 0
        for variable in self.EXPLANATORY_VARS:
            self.print_status('Hexbin plot for ' + variable)
            self.df.query('-.48 > diff | diff > 0.6').plot.hexbin(
                x='diff', y=variable, gridsize=40, ax=axes[row, col]
            )
            axes[row, col].set_title(variable)
            axes[row, col].set_xlabel('')
            if col == 0:
                axes[row, col].set_ylabel('Difference in Elevation')
            else:
                axes[row, col].set_ylabel('')

            if col == 2:
                col = 0
                row += 1
            else:
                col += 1

        self.save_plot(name='hexbin_elevation_diff')

    def qqplot(self):
        fig = plt.figure(figsize=(12,8))
        probplot = sm.ProbPlot(self.raster_difference.band_filtered.compressed())
        ax = fig.gca()
        probplot.qqplot(ax=ax, line='s')
        ax.get_lines()[0].set(markersize=1)
        ax.get_lines()[1].set(color='black', dashes=[4, 1])
        ax.set_title('Normal Q-Q Plot')
        plt.savefig(self.output_path + '/qq_plot.png')

    def plot_all(self):
        self.plot_lidar_vs_sfm()
        self.plot_difference_vs_source()
        self.hexbin_plot()

    @staticmethod
    def fit_model(y, x, name):
        print('\n** OLS for: ' + name + ' **\n')
        model = sm.OLS(y, x, missing='drop').fit()
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
            self.lidar.band_filtered.ravel(),
            self.sfm.band_filtered.ravel(),
            'Lidar vs. SfM',
        )

    def fit_all(self):
        self.fit_lidar_vs_sfm()
        self.fit_difference_vs_source(self.lidar, 'Lidar')
        self.fit_difference_vs_source(self.sfm, 'SfM')

    def run(self):
        # self.plot_all()
        self.qqplot()
        # self.fit_all()
