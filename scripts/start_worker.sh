#!/usr/bin/bash

set -o errexit
set -o nounset

# Check env variables
echo "DJANGO_ENV is ${DJANGO_ENV}"

# Set working directory
cd ${PROJECT_DIR}
echo "Change to working directory $(pwd)"

# Run celery worker for asynchronous tasks
celery -A src.infrastructure.server worker -l INFO
