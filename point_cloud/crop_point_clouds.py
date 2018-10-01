import argparse
import copy
import glob
import json
import re
from multiprocessing import Pool

import pdal

BASINS_BOUNDARIES = {
    'SBB': "([259249.411, 261872.873], [4198548, 4200442.470])",
    'ERW': "([322522.941446, 336546.729388], [4305592.330964, 4322441.471803])",
    'TRW': "([254245.744045, 307343.886432], [4179326.892644, 4229667.195265])"
}

PIPELINE_JSON_TEMPLATE = {
    'pipeline': [
        'infile',
        {
            'type': 'filters.crop',
            'bounds': 'boundaries'
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
    type=str,
    help='Basin boundaries - Options: SBB, TRW',
    required=True
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
        pipeline_json['pipeline'][2] = output_file

        pipelines.append(pipeline_json)

    with Pool() as pool:
        p_res = [
            pool.apply_async(execute_pdal, (pdal_json,))
            for pdal_json in pipelines
        ]

        [res.get() for res in p_res]
