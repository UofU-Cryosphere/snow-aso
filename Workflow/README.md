## Workflow Descriptions
Step number descriptions correspond to files in folders.

### Classifier
#### 1
Tool: _PDAL_

Create a cropped reference cloud that is classified with GeoTiff classification
raster.

Filters applied:
* Crop to target area with padding
* Classification using GeoTiff

#### 2
Tool: _PDAL_

Create GeoTiff of all points classified as stable with bands for minimum and
maximum for number of returns.

Filters applied:
* Points classified as stable ground surfaces

#### 3
Tool: _GDAL_

Create update classification GeoTiff, where pixels are:
* Classified as stable
* Attribute `NumberOfReturns` is 1
* No snow depth value was measured in delivery product of ASO

### Co-Registration
#### 1
Tool: _PDAL_

Crop reference cloud to target area with padding, retain points with single 
return pulse and classified as stable.

Filters applied:
* Crop to target area with padding
* Points classified as stable ground surface
* Keep points with 'NumberOfReturns' of 1

#### 2
Tool: _PDAL_

Create cloud that is used as moving source for co-registration.

Filters applied:
* Crop to target area with padding

#### 3
Tool: _ASP_

Run the co-registration using ASP `pc_align` tool using clouds produced in
step 1 and 2.

#### 4
Tool: _PDAL_

Create 1m resolution GeoTiff from the aligned (4M) and a 3m resolution file for
the reference (4R) cloud. 
The reference cloud will be filtered to points with single returns before
being exported to a raster.

#### 5
Tool: _GDAL_

Interpolate the SfM output to 3m resolution for comparison with downloaded 
snow depth map. This step also cuts the output raster to the final shape of the
watershed.
