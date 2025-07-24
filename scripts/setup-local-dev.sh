#!/bin/bash

# Setup script for local development
# This script reads .env file and sets up Jekyll environment

if [ ! -f .env ]; then
    echo "Error: .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Source the .env file
export $(cat .env | grep -v '^#' | xargs)

# Check if CHATBOT_API_URL is set
if [ -z "$CHATBOT_API_URL" ]; then
    echo "Error: CHATBOT_API_URL not set in .env file"
    exit 1
fi

echo "Starting Jekyll with CHATBOT_API_URL=$CHATBOT_API_URL"

# Start Jekyll with the environment variable
CHATBOT_API_URL="$CHATBOT_API_URL" bundle exec jekyll serve --livereload
