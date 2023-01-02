FROM ubuntu:20.04
# This stops being asked for geographical location with apt-get
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /
COPY requirements.txt /
# TODO: #1 Maybe should not use update (as this can change environment from update to update)
RUN apt-get update -y
# Not installing python 2
RUN apt-get install -y python3.10 python3-pip git-all expect
RUN pip install -r requirements.txt
#RUN alias python=python3
