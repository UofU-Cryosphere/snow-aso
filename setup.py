from setuptools import setup

setup(
    name='snow-aso',
    version='0.1',
    packages=[
        'images_time_table.base',
    ],
    url='https://github.com/UofU-Cryosphere/snow-aso',
    author='Joachim Meyer',
    author_email='j.meyer@utah.edu',
    description='Raster comparison tools',
    install_requires=[
        'numpy', 'pandas'
    ]
)
