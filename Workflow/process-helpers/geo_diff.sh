#!/usr/bin/env bash
# Convenience wrapper for ASP geodiff tool

${HOME}/asp/bin/geodiff \
  --float --threads ${SLURM_NTASKS} \
  $1 \
  $2
