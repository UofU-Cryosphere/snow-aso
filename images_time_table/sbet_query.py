import datetime
import math
import os

import numpy
import pandas

DAY_IN_SECONDS = 86400
GPS_EPOCH_SECONDS = 19

GPS_COLUMN = 'GpsTime'

SBET_CSV = 'sbet.csv'
SBET_DIR = 'SBET'
SBET_DTYPES = {
    GPS_COLUMN: numpy.float32,
    'X': numpy.float32,
    'Y': numpy.float32,
    'Z': numpy.float32,
    'Pitch': numpy.float32,
    'Roll': numpy.float32,
    'Heading': numpy.float32,
}


def sbet_csv_file(base_path):
    return os.path.join(base_path, SBET_DIR, SBET_CSV)


def get_gps_day_of_week(gps_week_time):
    days = datetime.timedelta(seconds=gps_week_time).days
    return days * DAY_IN_SECONDS


def seconds_to_time_of_day(seconds):
    return str(datetime.timedelta(seconds=float(seconds)))


def find_coordinates_for_row(sbet_table, gps_day_of_week, row):
    row_time = gps_day_of_week + float(row[7]) + GPS_EPOCH_SECONDS

    time = sbet_table[
        (sbet_table[GPS_COLUMN] > row_time - 0.1) &
        (sbet_table[GPS_COLUMN] < row_time + 0.1)
    ]

    min_diff = (abs(time[GPS_COLUMN] - row_time))

    if len(min_diff) == 0:
        return

    min_diff = min_diff.idxmin()
    min_diff = sbet_table.iloc[min_diff]

    row[1] = math.degrees(min_diff.X) # SBET has radians for X and Y
    row[2] = math.degrees(min_diff.Y) #
    row[3] = min_diff.Z
    row[4] = abs(math.degrees(min_diff.Heading))
    row[5] = min_diff.Pitch
    row[6] = min_diff.Roll
    row[7] = seconds_to_time_of_day(row[7])


def get_image_imu_data(basin_path, image_list):
    sbet_table = pandas.read_csv(
        sbet_csv_file(basin_path), converters=SBET_DTYPES
    )

    gps_day_of_week = get_gps_day_of_week(sbet_table[:1][GPS_COLUMN][0])

    [
        find_coordinates_for_row(sbet_table, gps_day_of_week, row)
        for row in image_list
    ]

    return image_list
