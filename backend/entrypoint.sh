#!/bin/sh

pip3 install -r /app/requirements.txt --no-cache-dir
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py loaddata stat_types.json
gunicorn foodgram.wsgi:application --bind 0:8000
exec "$@"
