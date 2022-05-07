#!/bin/bash

set -ex

python manage.py collectstatic --no-input
python manage.py makemigrations --no-input
python manage.py migrate --no-input

gunicorn core.wsgi:application --bind 0.0.0.0:8000
