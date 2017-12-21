FROM python:2.7.10
MAINTAINER Lucas Rondenet

RUN apt-get update -y
RUN apt-get install -y python-pip 

ADD . /code
WORKDIR /code
RUN pip install --editable .
CMD boxel
