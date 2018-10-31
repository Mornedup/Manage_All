#!/bin/bash


yes | python manage.py collectstatic


sleep 5

gunicorn manage_all.wsgi:application -b 0.0.0.0:8001 -w 6 --log-level DEBUG
#python manage.py runserver 0.0.0.0:8001 # port
