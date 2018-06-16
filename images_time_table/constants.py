import numpy

CSV_HEADER_ROW = [
    'File_name', 'X', 'Y', 'Z', 'Yaw', 'Pitch', 'Roll', 'Timestamp'
]

IMAGE_DIR = 'camera'

GPS_COLUMN = 'GpsTime'

SBET_DIR = 'SBET'
SBET_CSV = 'sbet.csv'
SBET_DTYPES = {
    GPS_COLUMN: numpy.float32,
    'X': numpy.float32,
    'Y': numpy.float32,
    'Z': numpy.float32,
    'Pitch': numpy.float32,
    'Roll': numpy.float32,
    'Heading': numpy.float32,
}
