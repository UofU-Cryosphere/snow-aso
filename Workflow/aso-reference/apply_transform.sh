#!/usr/bin/env bash
# Four required arguments
# 1: transform to be applied
# 2: output folder
# 3: reference cloud
# 4: moving cloud


${HOME}/asp/bin/pc_align \
  --threads 1 \
  --max-displacement -1 \
  --num-iterations 0 \
  --alignment-method point-to-point \
  --save-transformed-source-points \
  --initial-transform ${1} \
  -o ${2} \
  ${3} \
  ${4}

