import csv
import os


class ImagesMetaCsv(object):
    TIME_COLUMN = 'Timestamp'
    FILE_COLUMN = 'Filename'
    RESULT_KEYS = [
        FILE_COLUMN, 'X', 'Y', 'Z', 'Yaw', 'Pitch', 'Roll', 'Time Diff',
        TIME_COLUMN
    ]

    CSV_OUTPUT_FILE = 'images_metadata.csv'

    @staticmethod
    def write_output_file(base_path, images_data):
        csv_file = os.path.join(base_path, ImagesMetaCsv.CSV_OUTPUT_FILE)
        print('Writing CSV file to:')
        print('    ' + str(csv_file))
        with open(csv_file, 'w') as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=ImagesMetaCsv.RESULT_KEYS,
                delimiter=',',
                lineterminator='\n',
            )
            writer.writeheader()
            writer.writerows(images_data)
