import argparse
import csv
import os

import eif_image_data
import sbet_query

TIMESTAMP_COLUMN = 'Timestamp'
CSV_HEADER_ROW = [
    'File_name', 'X', 'Y', 'Z', 'Yaw', 'Pitch', 'Roll', 'Time Diff',
    TIMESTAMP_COLUMN
]
CSV_OUTPUT_FILE = 'images_metadata.csv'

IMAGE_DIR = 'camera'


def timestamp_col_index():
    return CSV_HEADER_ROW.index(TIMESTAMP_COLUMN)


def image_dir(base_path):
    return os.path.join(base_path, IMAGE_DIR)


def write_output_file(base_path, images_data):
    csv_file = os.path.join(base_path, IMAGE_DIR, CSV_OUTPUT_FILE)
    with open(csv_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(CSV_HEADER_ROW)
        writer.writerows(images_data)


parser = argparse.ArgumentParser()
parser.add_argument(
    '--base-path',
    type=str,
    help='Root directory of the basin',
    required=True
)
parser.add_argument(
    '--old-eif-type',
    type=bool,
    help='Flag to indicate old eif files with no IMU data',
    default=False,
)
parser.add_argument(
    '--query-sbet',
    type=bool,
    help='Flag to force querying the SBET file for new EIF file type',
    default=False,
)

if __name__ == '__main__':
    arguments = parser.parse_args()
    query_sbet = arguments.old_eif_type or arguments.query_sbet

    basin_dir = os.path.join(arguments.base_path, '')
    print('Getting image list')
    image_list = eif_image_data.get_image_list(
        image_dir(arguments.base_path),
        arguments.old_eif_type,
        arguments.query_sbet
    )
    if query_sbet:
        print('Adding IMU data')
        sbet_query.get_image_imu_data(basin_dir, image_list)
    print('Writing CSV file')
    write_output_file(basin_dir, image_list)
