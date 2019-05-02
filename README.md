## ASO aerial imagery processing

Collection of scripts to process aerial imagery from the Airborne Snow 
Observatory (ASO) using Agisoft Metashape on CHPC. 

### CHPC

Folder contains multiple sample files for SLURM to do various tasks.
Also has a script to run Agisoft's Metashape through their Python API.

### images_time_table

Set of scripts to create a geo-location csv reference file for images. 

### point_cloud

Python scripts that use PDAL to create GeoTiffs from point cloud files.

## Setup

Steps for local setup:
* Clone repository
* Create conda environment using the supplied `environment.yml`:
```bash
conda env create -f environment.yml
```
* Install this repo to your conda environment:
```bash
conda activate snow_aso
cd path/to/repository/snow-aso
pip install -e .
```
* For Metashape development, [download their Python package](https://www.agisoft.com/downloads/installer/)
and install into the conda environment. Replace `Metashape.whl` below with the actual downloaded file name 
```bash
conda activate snow_aso
cd path/to/repository/snow-aso
pip install -e Metashape.whl
```
