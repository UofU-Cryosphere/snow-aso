import csv
import os

from images_time_table.constants import CO_IMAGE_PATH
from images_time_table.eif_image_data import get_image_list
from images_time_table.sbet_query import get_image_imu_data

HEADER_ROW = ['File_name', 'Timestamp', 'X', 'Y', 'Z', 'Roll', 'Pitch', 'Yaw']
OUTPUT_FILE = os.path.join(CO_IMAGE_PATH, 'images_time_table.csv')


def write_output_file(images_data):
    with open(OUTPUT_FILE, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(HEADER_ROW)
        writer.writerows(images_data)


if __name__ == '__main__':
    print('Getting image list')
    image_list = get_image_list()
    print('Adding IMU data')
    get_image_imu_data(image_list)
    print('Writing CSV file')
    write_output_file(image_list)
