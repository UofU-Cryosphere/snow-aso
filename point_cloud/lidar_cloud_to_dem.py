import argparse
import json
import os

import gdal
import pdal

from basin_data import BASINS_BOUNDARIES, BASIN_EPSG

LAZ_MASK_PIPELINE_JSON = {
    "pipeline": [
        "__INFILE__",
        {
            "type": "filters.colorization",
            "raster": "/Path/To/CASI_Mask.tif",
            "dimensions": "Red:1"
        },
        {
            "type": "filters.range",
            "limits": "Red[0:2]"
        },
        {
            "type": "filters.colorization",
            "raster": "/Path/To/ENVI_Mask.tif",
            "dimensions": "Red:1"
        },
        {
            "type": "filters.range",
            "limits": "Red(2:255]"
        },
        {
            "filename": "__OUTFILE__",
            "type": "writers.las",
            "compression": "laszip",
            "forward": "all",
            "dataformat_id": 0,
        }
    ]
}

LAZ_DEM_PIPELINE_JSON = {
    "pipeline": [
        "__INFILE__",
        {
            "type": "filters.colorization",
            "raster": "/Path/To/CASI_Mask.tif",
            "dimensions": "Red:1"
        },
        {
            "type": "filters.range",
            "limits": "Red[0:1]"
        },
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

LAZ_MASKED_OUTFILE = '{0}_masked.laz'
LAZ_TO_DEM_OUTFILE = '{0}_1m.tif'
DEM_COMPRESSED_OUTFILE = '{0}_1m_c.tif'

SAVE_MESSAGE = 'Saved output to:\n  {0}\n'

parser = argparse.ArgumentParser()
parser.add_argument(
    '--lidar-laz',
    type=argparse.FileType('r'),
    help='Path to lidar point cloud',
    required=True
)
parser.add_argument(
    '--casi-mask',
    type=argparse.FileType('r'),
    help='Path to CASI mask',
    required=True
)
parser.add_argument(
    '--envi-mask',
    type=argparse.FileType('r'),
    help='Path to ENVI mask',
    required=True
)
parser.add_argument(
    '--basin',
    type=str,
    help='Basin boundaries',
    required=True,
    choices=BASINS_BOUNDARIES.keys()
)


def execute_pdal(pipeline):
    pdal_process = pdal.Pipeline(json.dumps(pipeline))
    pdal_process.validate()
    pdal_process.execute()


if __name__ == '__main__':
    arguments = parser.parse_args()

    print('Masking out vegetation')

    output_file = os.path.splitext(arguments.lidar_laz.name)[0]
    output_file = os.path.join(
        os.path.dirname(arguments.lidar_laz.name), output_file
    )

    LAZ_MASK_PIPELINE_JSON['pipeline'][0] = arguments.lidar_laz.name
    LAZ_MASK_PIPELINE_JSON['pipeline'][1]['raster'] = arguments.casi_mask.name
    LAZ_MASK_PIPELINE_JSON['pipeline'][3]['raster'] = arguments.envi_mask.name
    LAZ_MASK_PIPELINE_JSON['pipeline'][5]['filename'] = \
        LAZ_MASKED_OUTFILE.format(output_file)

    execute_pdal(LAZ_MASK_PIPELINE_JSON)
    print(SAVE_MESSAGE.format(LAZ_MASKED_OUTFILE.format(output_file)))

    print('Creating DEM')

    LAZ_DEM_PIPELINE_JSON['pipeline'][0] = LAZ_MASKED_OUTFILE.format(
        output_file)
    LAZ_DEM_PIPELINE_JSON['pipeline'][1]['raster'] = arguments.casi_mask.name
    LAZ_DEM_PIPELINE_JSON['pipeline'][3]['filename'] = \
        LAZ_TO_DEM_OUTFILE.format(output_file)
    LAZ_DEM_PIPELINE_JSON['pipeline'][3]['gdalopts'] = \
        't_srs=' + BASIN_EPSG[arguments.basin]
    LAZ_DEM_PIPELINE_JSON['pipeline'][3]['bounds'] = BASINS_BOUNDARIES[
        arguments.basin
    ]

    execute_pdal(LAZ_DEM_PIPELINE_JSON)
    print(SAVE_MESSAGE.format(LAZ_TO_DEM_OUTFILE.format(output_file)))

    print('\nCompressing tif')

    gdal.Translate(
        DEM_COMPRESSED_OUTFILE.format(output_file),
        gdal.Open(LAZ_TO_DEM_OUTFILE.format(output_file), gdal.GA_ReadOnly),
        creationOptions=["COMPRESS=LZW", "TILED=YES",
                         "BIGTIFF=IF_SAFER", "NUM_THREADS=ALL_CPUS"]
    )

    print(SAVE_MESSAGE.format(DEM_COMPRESSED_OUTFILE.format(output_file)))
