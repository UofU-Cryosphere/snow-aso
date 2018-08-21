import datetime
import math
import os

import numpy
import pandas

from images_meta_csv import ImagesMetaCsv


class SbetFile(object):
    DAY_IN_SECONDS = 86400
    GPS_EPOCH_SECONDS = 18

    GPS_COLUMN = 'GpsTime'
    GPS_TIME_WINDOW = 0.1

    SBET_CSV_FILE_NAME = 'sbet.csv'
    SBET_DIR = 'SBET'
    SBET_CSV_DTYPES = {
        GPS_COLUMN: numpy.float32,  # in seconds
        'X': numpy.float32,         # in meters
        'Y': numpy.float32,         # in radians
        'Z': numpy.float32,         # in radians
        'Roll': numpy.float32,      # in radians
        'Pitch': numpy.float32,     # in radians
        'Heading': numpy.float32,   # in radians
    }

    def __init__(self, base_path):
        print('Adding IMU data')
        self.file_path = self.csv_file_path(base_path)
        self.sbet_table = pandas.read_csv(
            self.file_path, converters=self.SBET_CSV_DTYPES
        )
        self.day_of_week = self.get_gps_day_of_week()

    @staticmethod
    def csv_file_path(base_path):
        return os.path.join(
            base_path, SbetFile.SBET_DIR, SbetFile.SBET_CSV_FILE_NAME
        )

    @staticmethod
    def yaw_to_360(yaw):
        return yaw + 360 if yaw < 0 else yaw

    def get_gps_day_of_week(self):
        days = datetime.timedelta(
            seconds=self.sbet_table[:1][self.GPS_COLUMN][0]
        ).days
        return days * SbetFile.DAY_IN_SECONDS

    def row_time_to_gps_time(self, time):
        return self.day_of_week + float(time) + self.GPS_EPOCH_SECONDS

    def find_sbet_record(self, row_time):
        time = self.sbet_table[
            (self.sbet_table[
                 self.GPS_COLUMN] > row_time - self.GPS_TIME_WINDOW) &
            (self.sbet_table[self.GPS_COLUMN] < row_time + self.GPS_TIME_WINDOW)
            ]

        min_diff = (abs(time[self.GPS_COLUMN] - row_time))

        if len(min_diff) == 0:
            return []

        return self.sbet_table.iloc[min_diff.idxmin()]

    @staticmethod
    def update_row(row, values):
        for key, value in zip(ImagesMetaCsv.RESULT_KEYS, values):
            row[key] = value
        return row

    def imu_data_for_row(self, row):
        gps_time = self.row_time_to_gps_time(
            row.get(ImagesMetaCsv.TIME_COLUMN)
        )
        sbet_record = self.find_sbet_record(gps_time)

        result = [
            row.get(ImagesMetaCsv.FILE_COLUMN),
            math.degrees(sbet_record.X),
            math.degrees(sbet_record.Y),
            sbet_record.Z,
            self.yaw_to_360(math.degrees(sbet_record.Heading)),
            math.degrees(sbet_record.Pitch),
            math.degrees(sbet_record.Roll),
            gps_time - sbet_record[self.GPS_COLUMN],
            row.get(ImagesMetaCsv.TIME_COLUMN),
            row.get(ImagesMetaCsv.TIME_OF_DAY)
        ]

        return self.update_row(row, result)
