import csv
import glob
import os

from images_time_table.constants import CO_IMAGE_PATH

EIF_SOURCE_FILES = os.path.join(CO_IMAGE_PATH, '01_EIF/*.eif')


def file_name_from_path(path):
    return path.split('\\')[-1]


def add_entry_to_table(images_time_table, row):
    file_name = file_name_from_path(row[1])
    images_time_table.append(
        [
            file_name,
            row[0],
        ]
    )


def get_image_list():
    images_time_table = []

    for source_file in glob.glob(EIF_SOURCE_FILES):
        with open(source_file) as input_file:
            csv_reader = csv.reader(input_file, delimiter=' ')
            [
                add_entry_to_table(images_time_table, row)
                for row in csv_reader
            ]

    return sorted(images_time_table, key=lambda row: row[1])
