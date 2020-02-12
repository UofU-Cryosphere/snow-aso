## ASO aerial imagery processing

Collection of scripts to process aerial imagery from the Airborne Snow 
Observatory (ASO) using Agisoft Metashape on CHPC. 

### Agisoft

Script to run Agisoft's Metashape through their Python API.

### CHPC

Folder contains sample files SLURM scripts.

### images_time_table

Set of scripts to create a geo-location csv reference file for images. 

### PDAL

Collection of sample pipelines.

### point_cloud

Python scripts that use PDAL to create GeoTiffs from point cloud files.

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
* For Metashape development, [download their Python package](https://www.agisoft.com/downloads/installer/)
and install into the conda environment. Replace `Metashape.whl` below with the actual downloaded file name 
```shell
conda activate snow_aso
cd path/to/repository/snow-aso
pip install -e Metashape.whl
```
