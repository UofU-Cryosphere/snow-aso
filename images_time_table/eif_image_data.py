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


def build_table_entry(row, old_eif_style):
    table_entry = [None] * len(images_meta_csv.CSV_HEADER_ROW)

    if old_eif_style:
        table_entry[0] = file_name_from_path(row[1])
        table_entry[images_meta_csv.timestamp_col_index()] = row[0]
    else:
        table_entry[0] = file_name_from_path(row['file'])
        table_entry[images_meta_csv.timestamp_col_index()] = row['#time[s]']

    return table_entry


def read_eif_file(file):
    file_data = open(file).readlines()
    file_data = file_data[3:] # First three lines have comments
    return csv.DictReader(file_data, delimiter=';')


def get_image_list(base_path, old_eif_type, query_sbet):
    images_time_table = []

    for source_file in glob.glob(eif_files(base_path), recursive=True):
        if old_eif_type:
            with open(source_file) as input_file:
                csv_reader = csv.reader(input_file, delimiter=' ')
                images_time_table.extend([
                    build_table_entry(row, old_eif_type)
                    for row in csv_reader
                ])
        elif not old_eif_type and query_sbet:
            images_time_table.extend([
                build_table_entry(row, old_eif_type)
                for row in read_eif_file(source_file)
            ])
        elif not old_eif_type:
            for row in read_eif_file(source_file):
                images_time_table.append([
                    file_name_from_path(row['file']),
                    row['longitude[deg]'],
                    row['latitude[deg]'],
                    row['altitude[m]'],
                    row['yaw[deg]'],
                    row['pitch[deg]'],
                    row['roll[deg]'],
                    0, # 'Time Diff' values for new eif type are always 0
                    row['#time[s]'],
                ])

    if images_time_table is None:
        print('*** No images found in EIF source files ***')
        return []
    else:
        images_time_table = sorted(
            images_time_table,
            key=lambda row: row[images_meta_csv.timestamp_col_index()]
        )

        if not old_eif_type and not query_sbet:
            [convert_timestamp(row, images_meta_csv.timestamp_col_index())
             for row in images_time_table]

        return images_time_table
