import copy
import json

import pdal


class PointCloud(object):
    PDAL_PIPELINE = {
        "pipeline": [
            {
                "type": "readers.las",
                "filename": ""
            }
        ]
    }

    def __init__(self, filename):
        self._filename = filename
        self._pipeline = None

    @property
    def filename(self):
        return self._filename

    @property
    def values(self):
        if self._pipeline is None:
            self._pipeline = self.read_file()
        return self._pipeline.arrays[0]

    @property
    def metadata(self):
        if self._pipeline is None:
            self._pipeline = self.read_file()
        return self._pipeline.metadata

    @property
    def elevations(self):
        return self.values['Z']

    @property
    def latitude(self):
        return self.values['Y']

    @property
    def longitudes(self):
        return self.values['X']

    def read_file(self):
        pipeline = copy.deepcopy(self.PDAL_PIPELINE)
        pipeline['pipeline'][0]['filename'] = self.filename

        pipeline = pdal.Pipeline(json.dumps(pipeline))
        pipeline.validate()
        pipeline.execute()
        return pipeline
