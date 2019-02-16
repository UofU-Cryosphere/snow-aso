from setuptools import setup

setup(
    name='raster-compare',
    version='0.1',
    packages=[
        'images_time_table.base', 'raster_compare.base', 'raster_compare.plots',
    ],
    url='https://github.com/UofU-Cryosphere/snow-aso',
    author='Joachim Meyer',
    author_email='j.meyer@utah.edu',
    description='Raster comparison tools',
    install_requires=[
        'gdal', 'matplotlib', 'numpy', 'pdal', 'pandas',
        'opencv-python', 'pillow', 'statsmodels'
    ]
)
