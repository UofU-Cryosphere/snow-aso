import argparse
import csv
import os

import eif_image_data
import sbet_query

CSV_HEADER_ROW = [
    'File_name', 'X', 'Y', 'Z', 'Yaw', 'Pitch', 'Roll', 'Timestamp'
]
CSV_OUTPUT_FILE = 'images_metadata.csv'

IMAGE_DIR = 'camera'


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
    '--base-path', help='Root directory of the basin', required=True
)
parser.add_argument(
    '--old-eif-type',
    help='Flag to indicate old eif files with no IMU data',
    default=False,
)

if __name__ == '__main__':
    arguments = parser.parse_args()

    basin_dir = os.path.join(arguments.base_path, '')
    print('Getting image list')
    image_list = eif_image_data.get_image_list(
        image_dir(arguments.base_path), arguments.old_eif_type
    )
    if arguments.old_eif_type:
        print('Adding IMU data')
        sbet_query.get_image_imu_data(basin_dir, image_list)
    print('Writing CSV file')
    write_output_file(basin_dir, image_list)
