import csv
import glob
import os

import images_meta_csv
import sbet_query


def eif_files(base_path):
    return os.path.join(base_path, '01_EIF/**/*.eif')


def file_name_from_path(path):
    return path.split('\\')[-1]


def convert_timestamp(row, timestamp_index):
    row[timestamp_index] = sbet_query.seconds_to_time_of_day(
        row[timestamp_index]
    )


def add_entry_to_table(images_time_table, row, timestamp_index):
    file_row = [None] * len(images_meta_csv.CSV_HEADER_ROW)
    file_row[0] = file_name_from_path(row[1])
    file_row[timestamp_index] = row[0]
    images_time_table.append(file_row)


def sort_by_time(image_list, timestamp_index):
    return sorted(image_list, key=lambda row: row[timestamp_index])


def get_image_list(base_path, old_eif_style):
    images_time_table = []
    timestamp_index = images_meta_csv.CSV_HEADER_ROW.index('Timestamp')

    for source_file in glob.glob(eif_files(base_path), recursive=True):
        if old_eif_style:
            with open(source_file) as input_file:
                csv_reader = csv.reader(input_file, delimiter=' ')
                [
                    add_entry_to_table(images_time_table, row, timestamp_index)
                    for row in csv_reader
                ]
        else:
            file_data = open(source_file).readlines()
            file_data = file_data[3:] # First three lines have comments
            csv_reader = csv.DictReader(file_data, delimiter=';')
            for row in csv_reader:
                images_time_table.append([
                    file_name_from_path(row['file']),
                    row['longitude[deg]'],
                    row['latitude[deg]'],
                    row['altitude[m]'],
                    row['yaw[deg]'],
                    row['pitch[deg]'],
                    row['roll[deg]'],
                    row['#time[s]'],
                ])

    images_time_table = sort_by_time(images_time_table, timestamp_index)

    if not old_eif_style:
        [convert_timestamp(row, timestamp_index) for row in images_time_table]

    return images_time_table
