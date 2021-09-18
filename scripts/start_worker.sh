#!/usr/bin/bash

set -o errexit
set -o nounset

# Run celery worker for asynchronous tasks
celery -A src.infrastructure.server worker -l INFO
