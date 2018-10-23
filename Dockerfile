# set the base image
FROM python:3.6
# File Author / Maintainer
MAINTAINER Morne
RUN apt-get update && apt-get install -y build-essential

ENV APP_HOME /code
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

ADD requirements.txt $APP_HOME
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . $APP_HOME