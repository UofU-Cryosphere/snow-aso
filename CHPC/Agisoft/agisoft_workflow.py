import argparse
import datetime
import glob
import os
import sys

import Metashape


# Class to automate Agisoft Metashape processing
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

    WGS_84 = Metashape.CoordinateSystem("EPSG::4326")
    UTM_CA = Metashape.CoordinateSystem("EPSG::32611")
    UTM_CO = Metashape.CoordinateSystem("EPSG::32613")
    X_1M_IN_DEG = 1.13747e-05  # 1m in degree using EPSG:4326
    Y_1M_IN_DEG = 9.0094e-06   #
    X_5M_IN_DEG = 5.76345e-05  # 5m in degree using EPSG:4326
    Y_5M_IN_DEG = 4.50396e-05  #

    CAMERA_LOCATION_ACCURACY = Metashape.Vector([1., 1., 1.])
    CAMERA_ROTATION_ACCURACY = Metashape.Vector([1., 1., 1.])

    IMAGE_ACCURACY_MATCHING = Metashape.HighestAccuracy
    KEYPOINT_LIMIT = 40000
    TIEPOINT_LIMIT = 4000

    REPROJECTION_ERROR_THRESHOLD = 0.3
    REPROJECTION_ACCURACY_THRESHOLD = 10

    DENSE_POINT_QUALITY = dict(
        high=Metashape.HighQuality,
        medium=Metashape.MediumQuality,
    )

    EXPORT_DEFAULTS = dict(
        image_format=Metashape.ImageFormat.ImageFormatTIFF,
        projection=WGS_84,
        dx=X_1M_IN_DEG,
        dy=Y_1M_IN_DEG,
    )

    def __init__(self, options):
        # Ensure trailing slash
        self.project_base_path = os.path.join(options.base_path, '')
        self.project_file_name = self.project_file_path(options.project_name)

        self.setup_application()

        self.create_new_project()
        self.project = Metashape.app.document
        self.project.open(self.project_file_name + self.PROJECT_TYPE)
        self.chunk = self.project.chunk

        self.setup_camera()

        self.image_folder = os.path.join(
            self.project_base_path, options.image_folder, ''
        )
        self.image_type = options.image_type

    def create_new_project(self):
        if not os.path.exists(path=self.project_file_name + self.PROJECT_TYPE):
            new_project = Metashape.Document()
            chunk = new_project.addChunk()
            new_project.save(
                path=self.project_file_name + self.PROJECT_TYPE,
                chunks=[chunk]
            )

    def project_file_path(self, project_name):
        run_date = datetime.date.today().strftime('%Y_%m_%d')
        project_name = project_name + '_' + run_date
        return os.path.join(
            self.project_base_path, project_name
        )

    @staticmethod
    def setup_application():
        app = Metashape.Application()
        # Use all available GPUs, needs a bit mask
        number_of_gpus = len(Metashape.app.enumGPUDevices())
        mask = int(str('1' * number_of_gpus).rjust(8, '0'), 2)
        app.gpu_mask = mask
        # Allow usage of CPU and GPU
        app.cpu_enable = True

        settings = Metashape.Application.Settings()
        # Logging - Disabled for now
        settings.log_enable = False
        # settings.log_path = self.project_file_name + '_agisoft.log'
        settings.save()

    def setup_camera(self):
        # Imported camera coordinates projection
        self.chunk.crs = self.WGS_84
        # Accuracy for camera position in m
        self.chunk.camera_location_accuracy = self.CAMERA_LOCATION_ACCURACY
        # Accuracy for camera orientations in degree
        self.chunk.camera_rotation_accuracy = self.CAMERA_ROTATION_ACCURACY

    def save_and_exit(self):
        self.project.save()
        sys.exit(-1)

    def image_list(self):
        images = glob.glob(
            self.image_folder + '**/*' + self.image_type, recursive=True
        )
        if len(images) == 0:
            print('**** EXIT - ' + self.image_type +
                  ' no files found in directory:')
            print('    ' + self.image_folder)
            self.save_and_exit()
        else:
            return images

    def check_reference_file(self, file):
        """
        Check that the given reference file exists and has the image types
        loaded with this project by comparing file endings.
        """
        if os.path.exists(file):
            with open(file) as file:
                next(file)  # skip header line
                first_file = next(file).split(',')[0]
                if not first_file.endswith(self.image_type):
                    print('**** Reference file has different '
                          'source image types *****\n'
                          '   given: ' + self.image_type + '\n'
                          '   first image: ' + first_file)
                    self.save_and_exit()
        else:
            print('**** EXIT - No reference file found ****')
            self.save_and_exit()

    def load_image_references(self):
        reference_file = self.project_base_path + self.REFERENCE_FILE
        self.check_reference_file(reference_file)
        self.chunk.loadReference(
            path=reference_file,
            delimiter=',',
            format=Metashape.ReferenceFormatCSV,
        )

    def align_images(self):
        self.chunk.addPhotos(self.image_list())
        self.load_image_references()
        self.chunk.matchPhotos(
            accuracy=self.IMAGE_ACCURACY_MATCHING,
            generic_preselection=True,
            reference_preselection=True,
            keypoint_limit=self.KEYPOINT_LIMIT,
            tiepoint_limit=self.TIEPOINT_LIMIT,
        )
        self.chunk.alignCameras()

    def remove_by_criteria(self, criteria, threshold):
        point_cloud_filter = Metashape.PointCloud.Filter()
        point_cloud_filter.init(self.chunk, criterion=criteria)
        point_cloud_filter.removePoints(threshold)

    def filter_sparse_cloud(self):
        # Points that statistical error in point placement exceed threshold
        self.remove_by_criteria(
            Metashape.PointCloud.Filter.ReprojectionError,
            self.REPROJECTION_ERROR_THRESHOLD,
        )
        # Points that accuracy of point placement from local neighbor points
        # exceed threshold
        self.remove_by_criteria(
            Metashape.PointCloud.Filter.ProjectionAccuracy,
            self.REPROJECTION_ACCURACY_THRESHOLD,
        )

    def build_dense_cloud(self, dense_cloud_quality):
        self.chunk.buildDepthMaps(
            quality=self.DENSE_POINT_QUALITY.get(dense_cloud_quality, 'high'),
            filter=Metashape.AggressiveFiltering,
        )
        self.chunk.buildDenseCloud()

    def export_results(self):
        self.chunk.exportDem(
            path=self.project_file_name + '_dem' + self.EXPORT_IMAGE_TYPE,
            **self.EXPORT_DEFAULTS
        )
        self.chunk.exportOrthomosaic(
            path=self.project_file_name + self.EXPORT_IMAGE_TYPE,
            tiff_big=True,
            **self.EXPORT_DEFAULTS
        )
        self.chunk.exportReport(self.project_file_name + self.PROJECT_REPORT)

    def process(self, options):
        self.align_images()
        self.filter_sparse_cloud()
        self.project.save()

        self.build_dense_cloud(options.dense_cloud_quality)
        self.project.save()

        self.chunk.buildDem()
        self.project.save()

        self.chunk.buildOrthomosaic()
        self.project.save()

        if options.with_export:
            self.export_results()


parser = argparse.ArgumentParser()
parser.add_argument(
    '--base-path', help='Root directory of the project.', required=True
)
parser.add_argument('--project-name', help='Name of project.', required=True)
parser.add_argument(
    '--image-folder',
    help='Location of images relative to base-path.',
    default='images'
)
parser.add_argument(
    '--image-type',
    help='Type of images - default to .tif',
    default=Agisoft.IMPORT_IMAGE_TYPE,
)
parser.add_argument(
    '--dense-cloud-quality', type=str, required=False, default='high',
    help='Overwrite default dense point cloud quality (High).'
)
parser.add_argument(
    '--with-export', type=bool, required=False, default=False,
    help='Export DEM, Orthomosaic and PDF report after dense cloud'
)

# Example command line execution:
# Mac OS:
# ./MetashapePro -r agisoft_workflow.py --base-path /path/to/root/project/directory --project-name test
#
# Windows:
# .\Metashape.exe -r agisoft_workflow.py --base-path D:\path/to/root/project/direcotry --project-name test
#
# Linux (headless):
# metashape.sh -platform offscreen -r agisoft_workflow.py --base_path /path/to/root/project/directory -- project-name test
# Optional arguments are:
# _image_folder_: Name and relative location where images are
# _image_type_: TYpe of images (i.e. .jpg, .iiq)
#
if __name__ == '__main__':
    arguments = parser.parse_args()
    project = Agisoft(arguments)
    project.process(arguments)
