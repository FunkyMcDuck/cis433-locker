FROM python:3.8
LABEL maintainer="cis433-locker"
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
COPY . /encryption
WORKDIR /encryption
RUN pip install --upgrade pip
RUN pip install -r requirements.txt