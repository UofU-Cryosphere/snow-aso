import glob
import os

import pandas

from images_meta_csv import ImagesMetaCsv
from sbet_file import SbetFile


class EifData(object):
    TIME_COLUMN = '#time[s]'
    FILE_COLUMN = 'file'
    OLD_EIF_HEADERS = [TIME_COLUMN, FILE_COLUMN]
    NEW_EIF_HEADERS = \
        OLD_EIF_HEADERS + \
        'sequenceID;roll[deg];pitch[deg];yaw[deg];omega[deg];phi[deg];' \
        'kappa[deg];latitude[deg];longitude[deg];altitude[m]'.split(';')

    OLD_CSV_OPTIONS = dict(names=OLD_EIF_HEADERS, sep=' ')
    NEW_CSV_OPTIONS = dict(
        names=NEW_EIF_HEADERS, sep=';', comment='#',
        usecols=NEW_EIF_HEADERS, lineterminator='\n'
    )

    def __init__(self, base_path, **kwargs):
        print('Getting image list')
        self.file_list = glob.glob(self.eif_files(base_path), recursive=True)
        self.new_eif_type = not kwargs['old_eif_type']
        self.force_query = kwargs['force_query']
        self.image_type = kwargs['image_type']
        self.images_time_table = []

    @staticmethod
    def eif_files(base_path):
        return os.path.join(base_path, '01_EIF/**/*.eif')

    @staticmethod
    def convert_time(entry):
        entry[ImagesMetaCsv.TIME_COLUMN] = SbetFile.seconds_to_time_of_day(
            entry[ImagesMetaCsv.TIME_COLUMN])

    def file_name_from_path(self, path):
        file_name = path.split('\\')[-1]

        file_type = path.split('.')[-1]
        if not file_type.endswith(self.image_type):
            file_name = file_name.replace(file_type, self.image_type)

        return file_name

    def add_to_table(self, row):
        data = [
            self.file_name_from_path(row.get(self.FILE_COLUMN)),
            row.get('longitude[deg]'),
            row.get('latitude[deg]'),
            row.get('altitude[m]'),
            SbetFile.yaw_to_360(
                row.get('yaw[deg]')) if 'yaw[deg]' in row else '',
            row.get('pitch[deg]'),
            row.get('roll[deg]'),
            0,  # 'Time Diff' values for new eif type are always 0
            row.get('#time[s]'),
        ]

        self.images_time_table.append(
            {k: v for k, v in zip(ImagesMetaCsv.RESULT_KEYS, data)}
        )

    def parse_files(self):
        for source_file in self.file_list:
            if self.new_eif_type:
                options = self.NEW_CSV_OPTIONS
            else:
                options = self.OLD_CSV_OPTIONS

            csv_data = pandas.read_csv(source_file, **options)

            csv_data.apply(lambda row: self.add_to_table(row), axis=1)

    def sort_by_time(self):
        self.images_time_table = sorted(
            self.images_time_table,
            key=lambda row: row[ImagesMetaCsv.TIME_COLUMN]
        )

    def get_images(self):
        self.parse_files()
        self.sort_by_time()

        if self.new_eif_type and not self.force_query:
            [self.convert_time(entry) for entry in self.images_time_table]
