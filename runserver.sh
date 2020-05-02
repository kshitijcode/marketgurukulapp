#!/usr/bin/env bash
python manage.py makemigrations && python manage.py migrate
python manage.py collectstatic --noinput
gunicorn --bind :8000 --workers 3 marketgurukul.wsgi