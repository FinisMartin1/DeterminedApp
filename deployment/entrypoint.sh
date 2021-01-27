#!/bin/sh


python database_load.py --mode=refresh
python manage.py collectstatic --no-input

gunicorn Determined.wsgi:application --bind 0.0.0.0:8000