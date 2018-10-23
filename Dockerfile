# set the base image
FROM python:3.6
# File Author / Maintainer
MAINTAINER Morne
RUN mkdir /code
#set directoty where CMD will execute
WORKDIR /code
#add project files to the usr/src/app folder
ADD . /code/
# Get pip to download and install requirements:
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
