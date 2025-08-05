#!/bin/bash

# Jekyll incremental build and serve script
# This script runs Jekyll with incremental builds for faster development

# Initialize rbenv if available
if command -v rbenv >/dev/null 2>&1; then
    eval "$(rbenv init -)"
fi

echo "Starting Jekyll with incremental builds..."
echo "Using Ruby: $(ruby --version)"
echo "Using Bundler: $(bundle --version)"
bundle exec jekyll serve --incremental
