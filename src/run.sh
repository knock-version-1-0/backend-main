#!/bin/bash

if [[ -f .env ]]; then
  export $(cat .env | grep -v '^# ' | xargs)
fi

python manage.py runserver 0.0.0.0:8000
