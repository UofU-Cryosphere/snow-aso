# Convert a tif to shp
gdaltindex CO_20170221.shp CO_20170221_tif.tif

# Cut to shape
gdalwarp -cutline INPUT.shp -crop_to_cutline -dstalpha INPUT.tif OUTPUT.tif

# Get a GeoJSON
ogr2ogr -f "GeoJSON" output.json input.shp

# Convert kmz to shp
ogr2ogr -f KML output.shp input.kml

# Get boundary from SfM cloud
pdal info --boundary sfm.laz

# Clip the lidar with sfm boundary
pdal pipeline pdal_pipeline_crop.json

# Warp
gdalwarp source.tif outfile.tif -t_srs "+proj=utm +zone=13 +datum=WGS84 +units=m +no_defs +ellps=WGS84 +towgs84=0,0,0"
gdalwarp source.tif outfile.tif -t_srs EPSG:32613

