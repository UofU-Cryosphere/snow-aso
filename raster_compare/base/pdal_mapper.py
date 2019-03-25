class PdalMapper(object):
    # Band assignment according to pdal writer.gdal
    # See: https://pdal.io/stages/writers.gdal.html#dimension
    RASTER_BANDS = {
        'min': 1,
        'max': 2,
        'mean': 3,
        # 'idw': 4,  # Unused
        'count': 5,
        'stdev': 6,
    }
