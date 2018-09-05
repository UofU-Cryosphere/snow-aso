import argparse
import os

from eif_data import EifData
from images_meta_csv import ImagesMetaCsv
from sbet_file import SbetFile

IMAGE_DIR = 'camera'

parser = argparse.ArgumentParser()
parser.add_argument(
    '--base-path',
    type=str,
    help='Root directory of the basin',
    required=True
)
parser.add_argument(
    '--old-eif-type',
    action="store_true",
    help='Flag to indicate old eif files with no IMU data',
)
parser.add_argument(
    '--query-sbet',
    action="store_true",
    help='Flag to force querying the SBET file for new EIF file type',
)
parser.add_argument(
    '--image-type',
    type=str,
    help='Change image file names to given type. Default: tif',
    default='tif',
)

if __name__ == '__main__':
    arguments = parser.parse_args()
    query_sbet = arguments.old_eif_type or arguments.query_sbet

    basin_dir = os.path.join(arguments.base_path, '')

    eif_data = EifData(
        os.path.join(basin_dir, IMAGE_DIR),
        old_eif_type=arguments.old_eif_type,
        force_query=arguments.query_sbet,
        image_type=arguments.image_type
    )
    eif_data.get_images()

    sbet = SbetFile(basin_dir)

    if query_sbet:
        image_list = [
            sbet.imu_data_for_row(row)
            for row in eif_data.images_time_table
        ]
    else:
        image_list = eif_data.images_time_table
        [sbet.set_altitude_for_row(row) for row in image_list]

    ImagesMetaCsv.write_output_file(basin_dir, image_list)
