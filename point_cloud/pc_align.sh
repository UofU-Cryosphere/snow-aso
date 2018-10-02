#!/usr/bin/env bash

cd /base/path

pc_align --max-displacement 1 \
         --max-num-reference-points 50000000\
         --max-num-source-points 10000000 \
         --save-transformed-source-points \
/Path/To/Lidar.laz \
/Path/To/Agisoft.laz
