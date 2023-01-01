FROM ubuntu:20.04
# This stops being asked for geographical location with apt-get
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /
COPY requirements.txt /
RUN apt-get update -y
# Not installing python 2
RUN apt-get install -y python3.10 python3-pip
RUN pip install -r requirements.txt
RUN apt-get install git-all
#RUN alias python=python3
