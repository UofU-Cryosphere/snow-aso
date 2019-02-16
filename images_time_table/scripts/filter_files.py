import argparse
import csv
import glob
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument(
    '--image-path',
    type=str,
    help='Root directory of the basin',
    required=True
)
parser.add_argument(
    '--file-csv',
    type=str,
    help='Path to csv file containing images to keep',
    default='tif',
)

if __name__ == '__main__':
    arguments = parser.parse_args()
    file_list = []

    with open(arguments.file_csv, 'r', newline='') as csv_file:
        files = csv.reader(csv_file)
        [file_list.append(file[0]) for file in files]

    images = glob.glob(os.path.join(arguments.image_path, '*.tif'))

    keep_folder = os.path.join(arguments.image_path, 'keep', '')
    if not os.path.exists(keep_folder):
        os.mkdir(keep_folder)


    for image in images:
        if os.path.basename(image) in file_list:
            print('moving file: ' + str(image))
            print('  to: ' + keep_folder)
            shutil.move(image, keep_folder)
