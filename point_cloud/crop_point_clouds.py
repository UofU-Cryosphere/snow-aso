import argparse
import copy
import glob
import json
import re
from multiprocessing import Pool

import pdal

from basin_data import BASINS_BOUNDARIES, BASIN_EPSG

PIPELINE_JSON_TEMPLATE = {
    'pipeline': [
        'infile',
        {
            'type': 'filters.crop',
            'bounds': 'boundaries',
            'a_srs': 'epsg',
        },
        'outfile'
    ]
}

LAZ_FILE_PATTERN = "{0}/*.la[s|z]"

parser = argparse.ArgumentParser()
parser.add_argument(
    '--base-path',
    type=str,
    help='Root directory',
    required=True
)
parser.add_argument(
    '--basin',
    type=str, required=True, choices=BASINS_BOUNDARIES.keys(),
    help='Basin short name to lookup bounding box',
)


def execute_pdal(pipeline):
    print('Processing input file: ' + pipeline['pipeline'][0])
    pdal_process = pdal.Pipeline(json.dumps(pipeline))
    pdal_process.validate()
    pdal_process.execute()
    print('** Created output file: ' + pipeline['pipeline'][2])


if __name__ == '__main__':
    arguments = parser.parse_args()

    files = glob.glob(LAZ_FILE_PATTERN.format(arguments.base_path))

    pipelines = []
    for input_file in files:
        output_file = re.sub(r'\.la[s|z]', '_cropped.laz', input_file)

        pipeline_json = copy.deepcopy(PIPELINE_JSON_TEMPLATE)
        pipeline_json['pipeline'][0] = input_file
        pipeline_json['pipeline'][1]['bounds'] = \
            BASINS_BOUNDARIES[arguments.basin]
        pipeline_json['pipeline'][1]['a_srs'] = \
            BASIN_EPSG[arguments.basin]
        pipeline_json['pipeline'][2] = output_file

        pipelines.append(pipeline_json)

    with Pool() as pool:
        p_res = [
            pool.apply_async(execute_pdal, (pdal_json,))
            for pdal_json in pipelines
        ]

        [res.get() for res in p_res]
