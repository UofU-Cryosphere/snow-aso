import csv
import os


class ImagesMetaCsv(object):
    FILE_COLUMN = 'Filename'
    TIME_OF_DAY = 'Time of Day'
    TIME_COLUMN = 'Timestamp'
    RESULT_KEYS = [
        FILE_COLUMN, 'X', 'Y', 'Z', 'Yaw', 'Pitch', 'Roll', 'Time Diff',
        TIME_COLUMN, TIME_OF_DAY
    ]
    CSV_OPTIONS = dict(
        fieldnames=RESULT_KEYS,
        delimiter=',',
        lineterminator='\n',
    )

    CSV_OUTPUT_FILE = 'images_metadata.csv'

    @staticmethod
    def read_file(file):
        with open(file, mode='r') as csv_file:
            csv_data = csv.DictReader(csv_file, **ImagesMetaCsv.CSV_OPTIONS)
            next(csv_data)  # Skip header
            for row in csv_data:
                yield row

    @staticmethod
    def write_output_file(base_path, images_data):
        csv_file = os.path.join(base_path, ImagesMetaCsv.CSV_OUTPUT_FILE)
        print('Writing CSV file to:')
        print('    ' + str(csv_file))
        with open(csv_file, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, **ImagesMetaCsv.CSV_OPTIONS)
            writer.writeheader()
            writer.writerows(images_data)
