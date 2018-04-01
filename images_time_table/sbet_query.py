import datetime
import math
import numpy
import pandas
import os

from images_time_table.constants import CO_SBET_PATH

DAY_IN_SECONDS = 86400

GPS_COLUMN = 'GpsTime'
GPS_EPOCH_SECONDS = 19

SBET_CSV = os.path.join(CO_SBET_PATH, 'sbet.csv')
SBET_DTYPES = {
    GPS_COLUMN: numpy.float32,
    'X': numpy.float32,
    'Y': numpy.float32,
    'Z': numpy.float32,
    'Pitch': numpy.float32,
    'Roll': numpy.float32,
    'Heading': numpy.float32,
}


def get_gps_day_of_week(gps_week_time):
    days = datetime.timedelta(seconds=gps_week_time).days
    return days * DAY_IN_SECONDS


def seconds_to_time_of_day(seconds):
    return str(datetime.timedelta(seconds=float(seconds)))


def find_coordinates_for_row(sbet_table, gps_day_of_week, row):
    row_time = gps_day_of_week + float(row[1]) + GPS_EPOCH_SECONDS

    time = sbet_table[
        (sbet_table[GPS_COLUMN] > row_time - 0.01) &
        (sbet_table[GPS_COLUMN] < row_time + 0.01)
    ]

    min_diff = (abs(time[GPS_COLUMN] - row_time)).idxmin()
    min_diff = sbet_table.iloc[min_diff]

    row[1] = seconds_to_time_of_day(row[1])
    row.extend([
        math.degrees(min_diff.X), # SBET has radians for X and Y
        math.degrees(min_diff.Y), #
        float(min_diff.Z),
        float(min_diff.Roll),
        float(min_diff.Pitch),
        float(min_diff.Heading),
    ])


def get_image_imu_data(image_list):
    sbet_table = pandas.read_csv(SBET_CSV, converters=SBET_DTYPES)
    gps_day_of_week = get_gps_day_of_week(float(sbet_table[:1][GPS_COLUMN]))

    [
        find_coordinates_for_row(sbet_table, gps_day_of_week, row)
        for row in image_list
    ]

    return image_list
