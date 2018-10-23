# set the base image
FROM python:3.6
# File Author / Maintainer
MAINTAINER Morne
RUN mkdir /source
#set directoty where CMD will execute
WORKDIR /source
#add project files to the usr/src/app folder
ADD . /source
# Get pip to download and install requirements:
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
