#!/bin/bash

# Jekyll incremental build and serve script
# This script runs Jekyll with incremental builds for faster development

echo "Starting Jekyll with incremental builds..."
bundle exec jekyll serve --incremental
