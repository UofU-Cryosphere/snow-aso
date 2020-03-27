#!/usr/bin/env bash
# Load custom conda module and activate given environment
set -e

module load miniconda3/latest
conda activate $1
