import argparse
import datetime
import glob
import os
import sys

import PhotoScan


# Class to automate Agisoft Photoscan processing
#
# This automates the processing with the following assumed project structure:
# _base_path_:
#  Root location for the project. This is where the image folder is assumed
#  under 'images' unless given with a different relative path location.
#
#  The Agisoft project file will be saved under this location along with the
#  project report that is created at the end.
#
#  For setting the reference a file with the name 'images_metadata.csv' is
#  assumed under here as well. The sequence for the fields should be:
#  file_name, lon, lat, elevation, yaw, pitch, roll
#
class Agisoft:
    IMAGE_TYPE = '.tif'
    PROJECT_TYPE = '.psx'
    PROJECT_REPORT = '.pdf'
    REFERENCE_FILE = 'images_metadata.csv'

    KEYPOINT_LIMIT = 40000
    TIEPOINT_LIMIT = 4000

    def __init__(self, base_path, project_name, image_folder, image_type):
        # Ensure trailing slash
        self.project_base_path = os.path.join(base_path, '')
        self.setup_application()

        project = PhotoScan.Document()
        chunk = project.addChunk()

        self.project_file_path = self.project_path(project_name)
        project.save(
            path=self.project_file_path + self.PROJECT_TYPE,
            chunks=[chunk]
        )

        self.project = PhotoScan.app.document
        self.project.open(self.project_file_path + self.PROJECT_TYPE)
        self.chunk = self.project.chunk
        self.images = self.list_images(image_folder, image_type)

    def setup_application(self):
        app = PhotoScan.Application()
        # Use all available GPUs
        app.gpu_mask = len(PhotoScan.app.enumGPUDevices())
        # Allow usage of CPU and GPU
        app.cpu_enable = True

        settings = PhotoScan.Application.Settings()
        # Logging
        settings.log_enable = True
        settings.log_path = self.project_base_path + \
            'agisoft_' + self.today_as_filename() + '.log'
        settings.save()

    @staticmethod
    def today_as_filename():
        return datetime.date.today().strftime('%Y_%m_%d')

    def project_name(self, base_name):
        return base_name + '_' + self.today_as_filename()

    def project_path(self, project_name):
        return os.path.join(
            self.project_base_path, self.project_name(project_name)
        )

    def list_images(self, source_folder, image_type):
        source_folder = os.path.join(
            self.project_base_path, source_folder, '**', ''
        )
        images = glob.glob(source_folder + '*' + image_type, recursive=True)
        if len(images) == 0:
            print('**** EXIT - ' + image_type + ' no files found in directory:')
            print('    ' + source_folder)
            sys.exit(-1)
        else:
            return images

    def align_images(self):
        self.chunk.crs = PhotoScan.CoordinateSystem("EPSG::4326")
        self.chunk.addPhotos(self.images)
        if os.path.exists(self.project_base_path + self.REFERENCE_FILE):
            self.chunk.loadReference(
                path=self.project_base_path + self.REFERENCE_FILE,
                delimiter=',',
                format=PhotoScan.ReferenceFormatCSV,
            )
        else:
            print('**** WARNING - No reference file found ****')
        self.chunk.matchPhotos(
            accuracy=PhotoScan.HighAccuracy,
            generic_preselection=True,
            reference_preselection=False,
            keypoint_limit=self.KEYPOINT_LIMIT,
            tiepoint_limit=self.TIEPOINT_LIMIT,
        )
        self.chunk.alignCameras()
        self.project.save()

    def build_dense_cloud(self):
        self.chunk.buildDepthMaps(
            quality=PhotoScan.HighQuality,
            filter=PhotoScan.AggressiveFiltering,
        )
        self.chunk.buildDenseCloud()
        self.project.save()

    def process(self):
        self.align_images()
        self.build_dense_cloud()

        self.chunk.buildDem()
        self.chunk.buildOrthomosaic()
        self.project.save()

        self.chunk.exportReport(self.project_file_path + self.PROJECT_REPORT)


parser = argparse.ArgumentParser()
parser.add_argument(
    '--base-path', help='Root directory of the project.', required=True)
parser.add_argument('--project-name', help='Name of project.', required=True)
parser.add_argument(
    '--image-folder',
    help='Location of images relative to base-path.',
    default='images'
)
parser.add_argument(
    '--image-type',
    help='Type of images - default to .tif',
    default=Agisoft.IMAGE_TYPE
)

# Example command line execution:
# Mac OS:
# ./PhotoScanPro -r agisoft_workflow.py --base-path /path/to/root/project/directory --project-name test
#
# Windows:
# .\photoscan.exe -r agisoft_workflow.py --base-path D:\path/to/root/project/direcotry --project-name test
#
# Optional arguments are:
# _image_folder_: Name and relative location where images are
# _image_type_: TYpe of images (i.e. .jpg, .iiq)
#
if __name__ == '__main__':
    arguments = parser.parse_args()
    project = Agisoft(
        base_path=arguments.base_path,
        project_name=arguments.project_name,
        image_folder=arguments.image_folder,
        image_type=arguments.image_type
    )
    project.process()
