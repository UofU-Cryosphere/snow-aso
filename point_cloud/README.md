## Point cloud processing

* `basin_data.py`

Contains dictionaries for study areas with their bounding box and EPSG codes

* `create_dem_lidar.json`

Sample PDAL pipeline that filters point cloud to include last and only returns,
and writes result as a GeoTIFF in 1m resolution.

* `crop_point_cloud.py`

Batch process multiple lidar files and crop each one to the boudning
box of the given basin name.

* `pc_align.sh`

Sample bash script to run ASP `pc_align` tool.

* `sfm_cloud_to_dem.py` and `lidar_cloud_to_dem.py`

Process a lidar/SfM point cloud to a corresponding DEM, creating masked products
for filtered vegetation and snow surfaces only along the way.