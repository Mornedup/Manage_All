FROM python:3.6
RUN mkdir /code
# Set Maintainer (as a label, MAINTAINER has been deprecated)
LABEL maintainer = "Morne"
# set working directory to /app/
WORKDIR /code
# install python dependencies
RUN pip install -U pip setuptools
RUN pip install -U pip wheel setuptools
RUN pip install -r requirements.txt
ADD . /code/
