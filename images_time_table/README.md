## Images time table

Generates CSV required to process imagery with PhotoScan. Main execution file
is `scripts/create_csv.py`. For usage of the script see:
```bash
python scripts/create_csv.py --help
```

The `bin/` folder contains a SBET converter from Applanix's binary format to a 
human-readable CSV.

### Required inputs

* EIF data files from ASO flight
* SBET file from ASO flight

### Required folder structure

The `create_csv.py` expects the following root folder structure:
```
ROOT
-| Camera
--| 01_EIF
---| *.eif
-| SBET
--| sbet.csv
```

The SBET file should have the following sequence:
```
GpsTime,X,Y,Z,Heading,Roll,Pitch
```

### Create SBET csv with `extract_cols_from_sbet`

The supplied `extract_cols_from_sbet.c` converter can be compiled on OS X using
the gcc compiler:
```bash
    gcc -o extract_cols_from_sbet extract_cols_from_sbet.c
```

The created binary can then be used with:
```bash
extract_cols_from_sbet /path/to/sbet_file.sbet ./
```

The `./` will write the output csv file to the current directory, but any valid
file path can be given.

## Notes on EIF and SBET data

### EIF

There are two version of `.eif` files. Flights pre-dating May of 2018 only carry
a timestamp (GPS time) and corresponding image name.

Flights after May of 2018 have the full geo-location (lat, lon, altitude) and
flight orientation (pitch, roll, yaw) for every image. **However**, the provided
flight orientation do not correspond to entries in the SBET and need re-calculation.
Currently the following is done:
* Yaw: `(360 - yaw) % 360`
* Pitch: Flipped with Roll value + 180˚
* Roll: Flipped with Pitch value and kept as is

### SBET

The SBET file is delivered in binary format and, when converted into a `.csv` file, 
is used as input to query IMU data per image.
