#!/usr/bin/env python

import argparse
import json
import os
import shutil

from shapely.geometry import shape, Point

from images_time_table.base import ImagesMetaCsv


def parser():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        '--images-path',
        type=str,
        help='Path containing images',
        required=True
    )
    argument_parser.add_argument(
        '--csv',
        type=str,
        help='Path to csv file containing images to keep.'
             'Format should be as written by create_csv script',
        required=True
    )
    argument_parser.add_argument(
        '--boundary',
        type=str,
        help='Path to boundaries in GeoJSON format',
    )
    return argument_parser


def load_boundaries(file):
    with open(file, 'r') as boundary_file:
        boundary = json.load(boundary_file)

        boundary = shape(boundary['features'][0]['geometry'])

    return boundary


def inbounds(polygon, image_location):
    return polygon.contains(
        Point(
            float(image_location['X']),
            float(image_location['Y'])
        )
    )


def ensure_destination_folder(base_dir):
    folder = os.path.join(base_dir, 'keep', '')
    if not os.path.exists(folder):
        os.mkdir(folder)

    return folder


def main():
    arguments = parser().parse_args()

    keep_folder = ensure_destination_folder(arguments.images_path)

    if arguments.boundary:
        bounds = load_boundaries(arguments.boundary)
    else:
        bounds = None

    for image in ImagesMetaCsv.read_file(arguments.csv):
        if bounds and not inbounds(bounds, image):
            continue

        image = os.path.join(
            arguments.images_path, image[ImagesMetaCsv.FILE_COLUMN]
        )

        if os.path.exists(image):
            print('moving file: ' + str(image))
            print('  to: ' + keep_folder)
            shutil.move(image, keep_folder)
        else:
            print(f'Missing file {image} from csv')


if __name__ == '__main__':
    main()
