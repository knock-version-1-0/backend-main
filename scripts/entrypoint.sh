#!/bin/bash
set -e

echo "Start migrate of django orm"
python manage.py migrate

echo "Application start"
# gunicorn --bind 0.0.0.0:8000 knock.wsgi
daphne -b 0.0.0.0 -p 8000 knock.asgi:application
