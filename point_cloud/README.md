## Point cloud processing

* `basin_data.py`

Contains dictionaries for study areas with their bounding box and EPSG codes.

* `create_dem_lidar.json`

Sample PDAL pipeline that filters point cloud to include last and only returns,
and writes result as a GeoTIFF in 1m resolution.

* `crop_point_cloud.py`

Batch process multiple lidar files and crop each one to the bounding
box of the given basin name.

* `pc_align.sh`

Sample bash script to run ASP `pc_align` tool to co-register point clouds.

### Lidar and SfM

Main two scripts needed for comparing points clouds are:
* `sfm_cloud_to_dem.py`
* `lidar_cloud_to_dem.py`

For usage see:
```bash
python [lidar|sfm]_cloud_to_dem.py --help
```

#### Required input files

* CASI vegetation mask as GeoTiff
* ENVI vegetation mask as GeoTiff

The vegetation removal is done in a two-step process. First the ASO spectrometer
is used, for a first filter, and then an additional mask (created with ENVI) is 
applied to extend the excluded areas around trees.

#### Lidar script

The lidar script will create the following:
* `<input_file_name>_masked.laz`

This file has all vegetation masked out and is used as a source point 
cloud for `pc_align`.

* `<input_file_name>_1m.tif`

GeoTiff with only snow classified surfaces at 1m resolution. Can be used without
further modification with `raster_compare`.

#### SfM script

The SfM script should be fed with the aligned point cloud by `pc_align` and will
create the following:

* `<input_file_name>_maseked_1m.tif`

GeoTiff with only snow classified surfaces at 1m resolution. Can be used without
further modification with `raster_compare`.

### CASI mask
The delivered CASI mask by ASO has the following mapping for band values:
* 1: snow
* 2: rock
* 3: vegetation