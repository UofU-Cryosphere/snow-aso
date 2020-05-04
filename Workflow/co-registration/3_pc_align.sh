#!/usr/bin/env bash
# Three required arguments
# 1: output folder
# 2: reference cloud
# 3: moving cloud

${HOME}/asp/bin/pc_align \
  --threads 24 \
  --max-displacement 1 \
  --alignment-method point-to-point \
  --save-transformed-source-points \
  --max-num-reference-points 200000000 \
  --max-num-source-points 200000000 \
  -o ${1} \
  ${2} \
  ${3}
