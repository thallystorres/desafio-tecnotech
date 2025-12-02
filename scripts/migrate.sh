#!/bin/bash

makemigrations.sh
echo "Executando migrate.sh"
python manage.py migrate --noinput
