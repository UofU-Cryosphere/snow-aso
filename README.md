## ASO aerial imagery processing

Collection of scripts to process aerial imagery from the Airborne Snow 
Observatory (ASO) using Agisoft PhotoScan on CHPC. The generated DEMS, exported
as GeoTiffs, are then statistically compared against an coincident DEM by lidar. 

### CHPC

* `agisoft_workflow.py`

Script that processes the images with Agisoft PhotoScan using their Python API.
Requires input information to the image folder location, plus a reference file 
that contains geo location and flight orientation information per image as CSV.

* `notchpeak.slurm`

Slurm batch script to enqueue a job on CHPC.

### Images time table

Generates CSV required to process imagery with PhotoScan. Main execution file
is `create_csv.py`.

#### Required inputs:

* EIF data files from ASO flight
* SBET file from ASO flight

***EIF data***

There are two version of `.eif` files. Flights pre-dating May of 2018 only carry
a timestamp (GPS time) and corresponding image name.

Flights after May of 2018 have the full geo-location (lat, lon, altitude) and
flight orientation (pitch, roll, yaw) for every image. **However**, the provided
flight orientation do not correspond to entries in the SBET and need re-calculation.
Currently the following is done:
* Yaw: `(360 - yaw) % 360`
* Pitch: Flipped with Roll value + 180˚
* Roll: Flipped with Pitch value and kept as is

***SBET data***

The SBET file is delivered in binary format and the provided 
`extract_cols_from_sbet` executable can transform that into a `.csv` file. This
is then used as input to query IMU data per image.

### Raster compare

Set of scripts to plot difference between two DEMs.
