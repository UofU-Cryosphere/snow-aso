import argparse

from pathlib import PurePath

import Metashape


class CreateOrthomosaic:
    """
    Class to generate an orthomosaic for a existing Metashape project.
    """
    EXPORT_IMAGE_TYPE = '.tif'

    WGS_84 = Metashape.CoordinateSystem("EPSG::4326")

    # Degree using EPSG:4326
    X_1M_IN_DEG = 1.13747e-05
    Y_1M_IN_DEG = 9.0094e-06

    # Degree using EPSG:4326
    X_5M_IN_DEG = 5.76345e-05
    Y_5M_IN_DEG = 4.50396e-05

    EXPORT_DEFAULTS = dict(
        image_format=Metashape.ImageFormat.ImageFormatTIFF,
        projection=WGS_84,
        dx=X_1M_IN_DEG,
        dy=Y_1M_IN_DEG,
    )

    def __init__(self, options):
        self.project_file = PurePath(options.project_file)

        self.setup_application()

        self.project = Metashape.app.document
        self.project.open(self.project_file.as_posix())
        self.chunk = self.project.chunk

    @property
    def project_file_name(self):
        return self.project_file.stem

    @staticmethod
    def setup_application():
        app = Metashape.Application()
        number_of_gpus = len(Metashape.app.enumGPUDevices())
        mask = int(str('1' * number_of_gpus).rjust(8, '0'), 2)
        app.gpu_mask = mask
        app.cpu_enable = False

        settings = Metashape.Application.Settings()
        settings.log_enable = False
        settings.save()

    def process(self, options):
        self.chunk.buildDem()
        self.project.save()

        self.chunk.buildModel()
        self.chunk.buildOrthomosaic(
            fill_holes=False,
        )
        self.project.save()

        if options.with_export:
            self.chunk.exportOrthomosaic(
                path=str(
                    self.project_file.with_suffix(self.EXPORT_IMAGE_TYPE)
                ),
                tiff_big=True,
                **self.EXPORT_DEFAULTS
            )


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--project-file',
        required=True,
        help='Full path to Metashape project file',
    )
    parser.add_argument(
        '--with-export',
        action='store_true',
        help='Flag to also export as .tif'
    )

    return parser


# Example command line execution:
#
# * Mac OS
# ./MetashapePro -r create_orthomosaic.py \
#                --project-file /path/to/project.psx \
#
# * Windows
# .\Metashape.exe -r create_orthomosaic.py \
#                 --project-file C:\path\to\project.psx \
#
# * Linux (headless)
# metashape.sh -platform offscreen \
#              -r create_orthomosaic.py \
#              --project-file /path/to/project.psx \
#
if __name__ == '__main__':
    arguments = argument_parser().parse_args()
    project = CreateOrthomosaic(arguments)
    project.process(arguments)
