#!/bin/bash


echo yes | python manage.py collectstatic

sleep 5

yes | python manage.py migrate

sleep 5

#gunicorn manage_all.wsgi:application -b 0:8001 -w 6 --log-level DEBUG
python manange.py runserver