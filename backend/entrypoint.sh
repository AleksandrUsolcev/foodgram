#!/bin/sh

pip3 install -r /app/requirements.txt --no-cache-dir
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn foodgram.wsgi:application --bind 0:8000
exec "$@"
