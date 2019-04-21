## Images time table

Generates CSV required to process imagery with PhotoScan. Main execution file
is `scripts/create_csv.py`.

The `bin/` folder contains a sbet converter from Applanix's binary format to a human-readable CSV.

### Required inputs:

* EIF data files from ASO flight
* SBET file from ASO flight

#### EIF data

There are two version of `.eif` files. Flights pre-dating May of 2018 only carry
a timestamp (GPS time) and corresponding image name.

Flights after May of 2018 have the full geo-location (lat, lon, altitude) and
flight orientation (pitch, roll, yaw) for every image. **However**, the provided
flight orientation do not correspond to entries in the SBET and need re-calculation.
Currently the following is done:
* Yaw: `(360 - yaw) % 360`
* Pitch: Flipped with Roll value + 180˚
* Roll: Flipped with Pitch value and kept as is

#### SBET data

The SBET file is delivered in binary format and the provided 
`extract_cols_from_sbet` executable can transform that into a `.csv` file. This
is then used as input to query IMU data per image.
