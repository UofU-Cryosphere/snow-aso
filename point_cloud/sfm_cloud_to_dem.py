import argparse
import json
import os

import gdal
import pdal

from basin_data import BASINS_BOUNDARIES, BASIN_EPSG

LAZ_DEM_PIPELINE_JSON = {
    "pipeline": [
        "__INFILE__",
        {
            "filename": "__OUTFILE__",
            "type": "writers.gdal",
            "bounds": "__BASIN_BOUNDARIES__",
            "gdalopts": "__EPSG_CODE__",
            "gdaldriver": "GTiff",
            "resolution": "1.0",
            "output_type": "all",
        }
    ]
}

LAZ_TO_DEM_OUTFILE = '{0}_1m.tif'
DEM_COMPRESSED_OUTFILE = '{0}_1m_c.tif'

SAVE_MESSAGE = 'Saved output to:\n  {0}\n'

parser = argparse.ArgumentParser()
parser.add_argument(
    '--sfm-laz',
    type=argparse.FileType('r'),
    help='Path to lidar point cloud',
    required=True
)
parser.add_argument(
    '--basin',
    type=str,
    help='Basin boundaries',
    required=True,
    choices=BASINS_BOUNDARIES.keys()
)

if __name__ == '__main__':
    arguments = parser.parse_args()

    output_file = os.path.splitext(arguments.sfm_laz.name)[0]
    output_file = os.path.join(
        os.path.dirname(arguments.sfm_laz.name), output_file
    )

    print('Creating DEM')

    LAZ_DEM_PIPELINE_JSON['pipeline'][0] = arguments.sfm_laz.name
    LAZ_DEM_PIPELINE_JSON['pipeline'][1]['filename'] = \
        LAZ_TO_DEM_OUTFILE.format(output_file)
    LAZ_DEM_PIPELINE_JSON['pipeline'][1]['gdalopts'] = \
        't_srs=' + BASIN_EPSG[arguments.basin]
    LAZ_DEM_PIPELINE_JSON['pipeline'][1]['bounds'] = BASINS_BOUNDARIES[
        arguments.basin
    ]

    pdal_process = pdal.Pipeline(json.dumps(LAZ_DEM_PIPELINE_JSON))
    pdal_process.validate()
    pdal_process.execute()

    print(SAVE_MESSAGE.format(LAZ_TO_DEM_OUTFILE.format(output_file)))

    print('Compressing tif')

    gdal.Translate(
        DEM_COMPRESSED_OUTFILE.format(output_file),
        gdal.Open(LAZ_TO_DEM_OUTFILE.format(output_file), gdal.GA_ReadOnly),
        creationOptions=["COMPRESS=LZW", "TILED=YES",
                         "BIGTIFF=IF_SAFER", "NUM_THREADS=ALL_CPUS"]
    )

    print(SAVE_MESSAGE.format(DEM_COMPRESSED_OUTFILE.format(output_file)))
