#!/bin/bash
set -e

echo ".env파일을 읽어서 environment 추가"
if [[ -f .env ]]; then
  export $(cat .env | grep -v '^#' | xargs)
fi

echo "run test"
pytest

echo "django orm migrate"
python manage.py migrate

echo "runserver"
python manage.py runserver 0.0.0.0:8000
