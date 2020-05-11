#!/usr/bin/env bash
# Convenience wrapper for ASP geodiff tool

${HOME}/asp/bin/geodiff \
  --float --threads 16 \
  $1 \
  $2
