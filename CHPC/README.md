## CHPC

Collection of different SLURM script templates to enqueue jobs for GPU instances.

### Agisoft

* `agisoft_workflow.py`

Script that processes the images with Agisoft PhotoScan using their Python API.
See script `Agisoft` class documentation and parameter help for details.

Usage help:
```bash
python agisoft_workflow.py --help
```

### PDAL

Collection of PDAL pipelines to process lidar files.
* `pdal-merge.slurm`: Sample SLURM script to merge multiple .las files
* `pdal-pipeline_*.slurm`: Sample script to clip a .las file to a bounding box.

### raster_compare

Sample SLURM scripts to enqueue raster comparison or snow-depth calculation.