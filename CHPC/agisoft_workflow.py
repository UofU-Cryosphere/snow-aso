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
    EXPORT_IMAGE_TYPE = '.tif'
    IMPORT_IMAGE_TYPE = '.tif'
    PROJECT_TYPE = '.psx'
    PROJECT_REPORT = '.pdf'
    REFERENCE_FILE = 'images_metadata.csv'

    WGS_84 = PhotoScan.CoordinateSystem("EPSG::4326")
    UTM_CA = PhotoScan.CoordinateSystem("EPSG::32611")
    UTM_CO = PhotoScan.CoordinateSystem("EPSG::32613")
    X_1M_IN_DEG = 1.13747e-05  # 1m in degree using EPSG:4326
    Y_1M_IN_DEG = 9.0094e-06   #
    X_5M_IN_DEG = 5.76345e-05  # 5m in degree using EPSG:4326
    Y_5M_IN_DEG = 4.50396e-05  #

    IMAGE_ACCURACY_MATCHING = PhotoScan.HighAccuracy
    KEYPOINT_LIMIT = 40000
    TIEPOINT_LIMIT = 4000

    REPROJECTION_ERROR_THRESHOLD = 0.3
    REPROJECTION_ACCURACY_THRESHOLD = 10

    DENSE_POINT_QUALITY = PhotoScan.HighQuality

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
        self.setup_camera()

        self.image_type = image_type
        self.images = self.list_images(image_folder)

    def setup_application(self):
        app = PhotoScan.Application()
        # Use all available GPUs, needs a bit mask
        number_of_gpus = len(PhotoScan.app.enumGPUDevices())
        mask = int(str('1' * number_of_gpus).rjust(8, '0'), 2)
        app.gpu_mask = mask
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

    def list_images(self, source_folder):
        source_folder = os.path.join(
            self.project_base_path, source_folder, '**', ''
        )
        images = glob.glob(
            source_folder + '*' + self.image_type, recursive=True
        )
        if len(images) == 0:
            print('**** EXIT - ' + self.image_type +
                  ' no files found in directory:')
            print('    ' + source_folder)
            sys.exit(-1)
        else:
            return images

    def setup_camera(self):
        # Imported camera coordinates projection
        self.chunk.crs = self.WGS_84
        # Accuracy for camera position in m
        self.chunk.camera_location_accuracy = PhotoScan.Vector([1, 1, 1])
        # Accuracy for camera orientations in degree
        self.chunk.camera_rotation_accuracy = PhotoScan.Vector([1, 1, 1])

    def check_reference_file(self, file):
        """
        Check that the given reference file also has the image types loaded
        with this project by comparing file endings.
        """
        with open(file) as file:
            next(file)  # skip header line
            first_file = next(file).split(',')[0]
            if not first_file.endswith(self.image_type):
                print('**** Reference file has different '
                      'source image types *****\n'
                      '   given: ' + self.image_type + '\n'
                      '   first image: ' + first_file)
                sys.exit(-1)

    def load_image_references(self):
        reference_file = self.project_base_path + self.REFERENCE_FILE
        if os.path.exists(reference_file):
            self.check_reference_file(reference_file)
            self.chunk.loadReference(
                path=reference_file,
                delimiter=',',
                format=PhotoScan.ReferenceFormatCSV,
            )
            return True
        else:
            print('**** EXIT - No reference file found ****')
            sys.exit(-1)

    def align_images(self):
        self.chunk.addPhotos(self.images)
        self.load_image_references()
        self.chunk.matchPhotos(
            accuracy=self.IMAGE_ACCURACY_MATCHING,
            generic_preselection=True,
            reference_preselection=True,
            keypoint_limit=self.KEYPOINT_LIMIT,
            tiepoint_limit=self.TIEPOINT_LIMIT,
        )
        self.chunk.alignCameras()
        self.project.save()

    def remove_by_criteria(self, criteria, threshold):
        point_cloud_filter = PhotoScan.PointCloud.Filter()
        point_cloud_filter.init(self.chunk, criterion=criteria)
        point_cloud_filter.removePoints(threshold)

    def filter_sparse_cloud(self):
        # Points that statistical error in point placement exceed threshold
        self.remove_by_criteria(
            PhotoScan.PointCloud.Filter.ReprojectionError,
            self.REPROJECTION_ERROR_THRESHOLD,
        )
        # Points that accuracy of point placement from local neighbor points
        # exceed threshold
        self.remove_by_criteria(
            PhotoScan.PointCloud.Filter.ProjectionAccuracy,
            self.REPROJECTION_ACCURACY_THRESHOLD,
        )

    def build_dense_cloud(self):
        self.chunk.buildDepthMaps(
            quality=self.DENSE_POINT_QUALITY,
            filter=PhotoScan.AggressiveFiltering,
        )
        self.chunk.buildDenseCloud()
        self.project.save()

    def export_results(self):
        self.chunk.exportDem(
            path=self.project_file_path + '_dem' + self.EXPORT_IMAGE_TYPE,
            image_format=PhotoScan.ImageFormat.ImageFormatTIFF,
            projection=self.WGS_84,
            dx=self.X_1M_IN_DEG,
            dy=self.Y_1M_IN_DEG,
        )
        self.chunk.exportOrthomosaic(
            path=self.project_file_path + self.EXPORT_IMAGE_TYPE,
            image_format=PhotoScan.ImageFormat.ImageFormatTIFF,
            projection=self.WGS_84,
            tiff_big=True,
            dx=self.X_1M_IN_DEG,
            dy=self.Y_1M_IN_DEG,
        )
        self.chunk.exportReport(self.project_file_path + self.PROJECT_REPORT)

    def process(self, export_results):
        self.align_images()
        self.filter_sparse_cloud()
        self.build_dense_cloud()

        self.chunk.buildDem()
        self.chunk.buildOrthomosaic()
        self.project.save()

        if export_results:
            self.export_results()


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
    default=Agisoft.IMPORT_IMAGE_TYPE
)
parser.add_argument(
    '--with-export', type=bool, required=False, default=False,
    help='Export DEM, Orthomosaic and PDF report after dense cloud'
)

# Example command line execution:
# Mac OS:
# ./PhotoScanPro -r agisoft_workflow.py --base-path /path/to/root/project/directory --project-name test
#
# Windows:
# .\photoscan.exe -r agisoft_workflow.py --base-path D:\path/to/root/project/direcotry --project-name test
#
# Linux (headless):
# photoscan.sh -platform offscreen -r agisoft_workflow.py --base_path /path/to/root/project/directory -- project-name test
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
    project.process(arguments.with_export)
