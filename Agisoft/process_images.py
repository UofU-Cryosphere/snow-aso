import argparse
import datetime
import glob
import os
import sys

import Metashape


class ProcessImages:
    """
    Class to automate Agisoft Metashape processing

    The following project structure is assumed:

    ``base_path``:
      Root location for the project.

    ``base_path/image_folder``:
      Folder name with all the images. Name defaults to 'images' unless given
      with a different name relative to _base_path_ location.

    A reference file with the name 'images_metadata.csv' is assumed
    under *base_path* as well. The sequence for the fields has to be:
    image_file_name, lon, lat, elevation, yaw, pitch, roll

    The Agisoft project file will be saved under *base_path*
    """

    # Default image type for input images
    IMPORT_IMAGE_TYPE = '.tif'
    PROJECT_TYPE = '.psx'
    IMAGE_FOLDER = 'images'
    REFERENCE_FILE = 'images_metadata.csv'

    WGS_84 = Metashape.CoordinateSystem("EPSG::4326")

    CAMERA_LOCATION_ACCURACY = Metashape.Vector([1., 1., 1.])
    CAMERA_ROTATION_ACCURACY = Metashape.Vector([1., 1., 1.])

    KEYPOINT_LIMIT = 40000
    TIEPOINT_LIMIT = 4000

    REPROJECTION_ERROR_THRESHOLD = 0.3
    REPROJECTION_ACCURACY_THRESHOLD = 10

    # Source:
    # https://www.agisoft.com/forum/index.php?topic=11697.msg52455#msg52455
    class ImageMatching:
        HIGH = 1
        MEDIUM = 2

    class DepthMapQuality:
        ULTRA = 1
        HIGH = 2
        MEDIUM = 4

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
        # Disable CPU usage; recommended in manual
        app.cpu_enable = False

        settings = Metashape.Application.Settings()
        settings.log_enable = False
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
            columns='nxyzabc',
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
            reference_preselection_mode=Metashape.ReferencePreselectionSource,
            keypoint_limit=self.KEYPOINT_LIMIT,
            tiepoint_limit=self.TIEPOINT_LIMIT,
        )
        self.chunk.alignCameras()
        self.project.save()

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
        self.chunk.optimizeCameras()
        self.project.save()

    def build_dense_cloud(self, dense_cloud_quality):
        self.chunk.buildDepthMaps(
            downscale=dense_cloud_quality,
            filter_mode=Metashape.MildFiltering,
        )
        self.chunk.buildDenseCloud()
        self.project.save()

    def process(self, options):
        self.align_images()
        self.filter_sparse_cloud()
        self.build_dense_cloud(options.dense_cloud_quality)

        self.project.save()


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
        default=ProcessImages.IMAGE_FOLDER,
        help='Location of images relative to base-path.',
    )
    parser.add_argument(
        '--image-type',
        default=ProcessImages.IMPORT_IMAGE_TYPE,
        help='Type of images - default to .tif',
    )
    parser.add_argument(
        '--dense-cloud-quality',
        type=int,
        required=False,
        default=ProcessImages.DepthMapQuality.HIGH,
        choices=[
            ProcessImages.DepthMapQuality.ULTRA,
            ProcessImages.DepthMapQuality.HIGH,
            ProcessImages.DepthMapQuality.MEDIUM,
        ],
        help="Integer for dense point cloud quality (default: High).\n"
             "Highest -> " + str(ProcessImages.DepthMapQuality.ULTRA) + ",\n"
             "High -> " + str(ProcessImages.DepthMapQuality.HIGH) + ",\n"
             "Medium -> " + str(ProcessImages.DepthMapQuality.MEDIUM)
    )

    return parser


# Example command line execution:
#
# * Mac OS
# ./MetashapePro -r process_images.py \
#                --base-path /project/root/path \
#                --project-name test
#
# * Windows
# .\Metashape.exe -r process_images.py \
#                 --base-path C:\project\root\path \
#                 --project-name test
#
# * Linux (headless)
# metashape.sh -platform offscreen \
#              -r process_images.py \
#              --base-path /project/root/path \
#              --project-name test
#
if __name__ == '__main__':
    arguments = argument_parser().parse_args()
    project = ProcessImages(arguments)
    project.process(arguments)
