# set the base image
FROM python:3.6
# File Author / Maintainer
MAINTAINER Morne
#add project files to the usr/src/app folder
ADD . /source/RMateMange
#set directoty where CMD will execute
WORKDIR /source/RMateMange
# Get pip to download and install requirements:
RUN pip install --no-cache-dir -r requirements.txt
# Expose ports
EXPOSE 8000
# default command to execute
gunicorn rmatemanage.wsgi:application --bind 0.0.0.0:8000 --workers 3
