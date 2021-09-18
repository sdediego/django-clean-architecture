#!/usr/bin/bash

set -o errexit
set -o nounset

# Check env variables
echo "Port ${PORT} exposed for Forex API"
export PORT

# Run database migrations
python manage.py migrate

if [ ${DJANGO_ENV} != 'production' ]; then
    # Create superuser if not exists
    export DJANGO_SUPERUSER_USERNAME="admin"
    export DJANGO_SUPERUSER_PASSWORD="admin"
    export DJANGO_SUPERUSER_EMAIL="admin@forex.com"
    python manage.py createsuperuser --noinput || echo "Superuser already exists."

    # Load fixtures if needed
    for file in "${PROJECT_DIR}/fixtures/*.json"; do
        python manage.py loaddata $file
    done
fi

# Start API server
python manage.py runserver 0.0.0.0:${PORT}
