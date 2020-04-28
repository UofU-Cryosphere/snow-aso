import argparse
import datetime
import glob
import os
import sys

import Metashape


# Class to automate Agisoft Metashape processing
#
# The following project structure is assumed:
# _base_path_:
#  Root location for the project.
#
# _base_path_/_image_folder_:
#  Folder name with all the images. Name defaults to 'images' unless given
#  with a different name relative to _base_path_ location.
#
#  A reference file with the name 'images_metadata.csv' is assumed
#  under _base_path_ as well. The sequence for the fields has to be:
#  image_file_name, lon, lat, elevation, yaw, pitch, roll
#
#  The Agisoft project file will be saved under _base_path_ along with the
#  project report that can be optionally created at the end.
#
class Agisoft:
    EXPORT_IMAGE_TYPE = '.tif'
    # Default image type for input images
    IMPORT_IMAGE_TYPE = '.tif'
    PROJECT_TYPE = '.psx'
    PROJECT_REPORT = '.pdf'
    IMAGE_FOLDER = 'images'
    REFERENCE_FILE = 'images_metadata.csv'

    WGS_84 = Metashape.CoordinateSystem("EPSG::4326")

    # Degree using EPSG:4326
    X_1M_IN_DEG = 1.13747e-05
    Y_1M_IN_DEG = 9.0094e-06

    # Degree using EPSG:4326
    X_5M_IN_DEG = 5.76345e-05
    Y_5M_IN_DEG = 4.50396e-05

    CAMERA_LOCATION_ACCURACY = Metashape.Vector([1., 1., 1.])
    CAMERA_ROTATION_ACCURACY = Metashape.Vector([1., 1., 1.])

    # Source:
    # https://www.agisoft.com/forum/index.php?topic=11697.msg52455#msg52455
    class ImageMatching:
        HIGH = 1
        MEDIUM = 2

    class DepthMapQuality:
        ULTRA = 1
        HIGH = 2
        MEDIUM = 4

    KEYPOINT_LIMIT = 40000
    TIEPOINT_LIMIT = 4000

    REPROJECTION_ERROR_THRESHOLD = 0.3
    REPROJECTION_ACCURACY_THRESHOLD = 10

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
        self.project.open(self.project_name)
        self.chunk = self.project.chunk

        self.setup_camera()

        self.image_folder = os.path.join(
            self.project_base_path, options.image_folder, ''
        )
        self.image_type = options.image_type

    @property
    def project_name(self):
        return self.project_file_name + self.PROJECT_TYPE

    def create_new_project(self):
        if not os.path.exists(path=self.project_name):
            new_project = Metashape.Document()
            chunk = new_project.addChunk()
            new_project.save(
                path=self.project_name,
                chunks=[chunk]
            )

    def project_file_path(self, project_name):
        """
        Return absolute Agisoft project file path. The project will be saved
        under initialized  _base_path_.
        Project name will be given _project_name_ parameter and a run date,
        when the project was created and will be appended to the name.
        Example: my_project_name_2019_01_01
        """
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
        """
        Find all images recursively under the initialized image folder.
        Only images with the specified file ending will be found.
        Default image file ending is '.tif'.

        The script will exit if there are no images found.
        """
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
        """
        Load reference information for each image.

        The reference file is assumed under the given _base_path_
        with a file name of: images_metadata.csv

        The script will exit if the file can not be found.
        """
        reference_file = self.project_base_path + self.REFERENCE_FILE
        self.check_reference_file(reference_file)
        self.chunk.importReference(
            path=reference_file,
            delimiter=',',
            format=Metashape.ReferenceFormatCSV,
            create_markers=False,
        )

    def align_images(self):
        self.chunk.addPhotos(self.image_list())
        self.load_image_references()
        self.chunk.matchPhotos(
            downscale=self.ImageMatching.HIGH,
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
            quality=dense_cloud_quality,
            filter=Metashape.MildFiltering,
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


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--base-path',
        required=True,
        help='Root directory of the project.',
    )
    parser.add_argument(
        '--project-name',
        required=True,
        help='Name of project.',
    )
    parser.add_argument(
        '--image-folder',
        default=Agisoft.IMAGE_FOLDER,
        help='Location of images relative to base-path.',
    )
    parser.add_argument(
        '--image-type',
        default=Agisoft.IMPORT_IMAGE_TYPE,
        help='Type of images - default to .tif',
    )
    parser.add_argument(
        '--dense-cloud-quality',
        type=int,
        required=False,
        default=Agisoft.DepthMapQuality.HIGH,
        choices=[
            Agisoft.DepthMapQuality.ULTRA,
            Agisoft.DepthMapQuality.HIGH,
            Agisoft.DepthMapQuality.MEDIUM,
        ],
        help="Integer for dense point cloud quality (default: High).\n" +
             f"Highest -> {Agisoft.DepthMapQuality.ULTRA},\n" +
             f"High -> {Agisoft.DepthMapQuality.HIGH},\n" +
             f"Medium -> {Agisoft.DepthMapQuality.MEDIUM}"
    )
    parser.add_argument(
        '--with-export',
        action='store_true',
        help='Export DEM, Orthomosaic and PDF report after dense cloud'
    )

    return parser


# Example command line execution:
#
# * Mac OS
# ./MetashapePro -r agisoft_workflow.py \
#                --base-path /project/root/path \
#                --project-name test
#
# * Windows
# .\Metashape.exe -r agisoft_workflow.py \
#                 --base-path C:\project\root\path \
#                 --project-name test
#
# * Linux (headless)
# metashape.sh -platform offscreen \
#              -r agisoft_workflow.py \
#              --base_path /project/root/path \
#              --project-name test
#
if __name__ == '__main__':
    arguments = argument_parser().parse_args()
    project = Agisoft(arguments)
    project.process(arguments)
