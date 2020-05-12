## Workflow Descriptions
Step number descriptions correspond to files in folders.

### Classifier
#### 1.)
Tool: _PDAL_

Create a cropped reference cloud that is classified with GeoTiff classification
raster.

Filters applied:
* Crop to target area with padding
* Classification using GeoTiff

```shell script
pdal pipeline ${PROJECT_HOME}/classifier/1_classify_cloud.json \
  --readers.las.filename=/path/to/source.laz \
  --writers.las.filename=/path/to/classified.laz
```

#### 2.)
Tool: _PDAL_

Create GeoTiff from all points that are classified as stable,
with a band for minimum and another for maximum number of returns.

Filters applied:
* Points classified as stable ground surfaces

```shell script
pdal pipeline ${PROJECT_HOME}/classifier/2_create_NoR_geotiff.json \                 
  --readers.las.filename=/path/to/classified.laz \                                       
  --writers.gdal.filename=/path/to/classified.tif
```

#### 3.)
Tool: _PDAL_

Create GeoTiff with elevation value of all points classified as stable.

Filters applied:
* Points classified as stable ground surfaces

#### 4.)
Tool: _GDAL_

Create updated classification GeoTiff, where pixels are:
* Classified as stable
* 'NumberOfReturns' is 1
* Slope angle more than 5 and less than 50 degrees.
* No snow depth value was measured in delivery product of ASO

### Co-Registration
#### 1.)
Tool: _PDAL_

Crop reference cloud to target area with padding, retain points with single 
return pulse and classified as stable.

Filters applied:
* Crop to target area with padding
* Points classified as stable ground surface
* Keep points with 'NumberOfReturns' of 1

```shell script
pdal pipeline ${PROJECT_HOME}/steps/1L_prepare_fixed_cloud.json \
  --readers.las.filename=/path/to/source.laz \
  --filters.colorization.raster=/path/to/classifier.tif \
  --writers.las.filename=/path/to/reference.laz
```

#### 2.)
Tool: _PDAL_

Create cloud that is used as moving source for co-registration.

Filters applied:
* Crop to target area with padding

```shell script
pdal pipeline 2_create_moving_cloud.json \
    --readers.las.filename=/path/to/source.laz \
    --writers.laz.filename=/path/to/moving.laz
```

#### 3.)
Tool: _ASP_

Run the co-registration using ASP `pc_align` tool using clouds produced in
step 1 and 2.

```shell script
source ${PROJECT_HOME}/steps/3_pc_align.sh \
  ${SCRATCH_HOME}/pc_align/run \
  /path/to/reference.laz \                      
  /path/to/moving.laz                       
```

#### 4.)
Tool: _PDAL_

Create 1m resolution GeoTiff from the aligned (4M) and a 3m resolution file for
the reference (4R) cloud. 
The reference cloud will be filtered to points with single returns before
being exported to a raster. The output is used for elevation, slope, and aspect
calculation in the analysis. The 3m resolution is necessary with the low point
density per square meter of the reference cloud.

```shell script
pdal pipeline 4M_create_geotiff.json.json \
    --readers.las.filename=/path/to/aligned.laz \
    --writers.gdal.filename=/path/to/aligned.tif
```

### Process-helpers

Collection of handy wrappers and data post-processing steps. All files with
`.gdal` are option files that can be passed to GDAL via the `--optfile` 
parameter. 

#### apply_transformation

Tool: _ASP_

Wrapper for pc_align to apply a transformation from a different run to another
point cloud.

#### cut_to_shape

Tool: _GDAL_

Cut any GeoTiff to boundaries of the watershed.

#### extract_elevation_band

Tool: _GDAL_

Extract the elevation band from the output of step 5. 

#### geo_diff

Tool: _ASP_

Wrapper for ASP geo_diff tool to ensure use of floats in output result.

#### resample_3m_cut

Tool: _GDAL_

Interpolate the SfM output to 3m resolution for comparison with downloaded 
snow depth map. This step also cuts the output raster to the final shape of the
watershed.
