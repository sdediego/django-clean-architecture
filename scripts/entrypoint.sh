#!/usr/bin/env sh

set -o errexit
set -o nounset

# Check env variables
echo "DJANGO_ENV is ${DJANGO_ENV}"
export DJANGO_ENV
echo "Port ${PORT} exposed"
export PORT

# Run python specific scripts
python manage.py migrate
python manage.py runserver 0.0.0.0:${PORT}
