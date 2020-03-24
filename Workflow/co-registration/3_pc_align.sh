#!/usr/bin/env bash

${HOME}/asp/bin/pc_align --threads 24 --max-displacement 1 \
         --alignment-method point-to-point \
         --save-transformed-source-points \
         --max-num-reference-points 35000000 \
         --max-num-source-points 100000000 \
         -o ${HOME}/scratch/pc_align_sfm_snow_on/sfm_snow_on \
         ${HOME}/scratch/reference.laz \
         ${HOME}/scratch/moving.laz
