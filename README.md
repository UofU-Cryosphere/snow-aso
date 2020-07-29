## Process aerial imagery with SfM

Collection of scripts to process aerial imagery from the Airborne Snow 
Observatory (ASO) using Agisoft Metashape on CHPC and produce a GeoTiff for
further analysis. 

### Agisoft

Script to run Agisoft's Metashape through their Python API.

### CHPC

Configuration to run SLURM jobs in a miniconda environment, installed in a user
directory.

### images_time_table

Set of scripts to create a geo-location csv reference file for images. 

### Workflow

Steps to align two point clouds, having the classification for the area in 
a GeoTiff.

## Third party tools

The repository relies heavily on these tools:

* [GDAL](https://gdal.org)
* [PDAL](https://pdal.io)
* [ASP](https://stereopipeline.readthedocs.io)

## Setup

Steps for local setup:
* Clone repository
* Create conda environment using the supplied `environment.yml`:
```shell
conda env create -f environment.yml
```
* Install this repo to your conda environment:
```shell
conda activate snow_aso
cd path/to/repository/snow-aso
pip install -e .
```
* For Metashape development, [download their Python 3 module](https://www.agisoft.com/downloads/installer/)
and install into the conda environment. Replace `Metashape.whl` below with the actual downloaded file name 
```shell
conda activate snow_aso
cd path/to/download/
pip install Metashape.whl
```
