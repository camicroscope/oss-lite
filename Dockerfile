############################################################
# Dockerfile to build Oss-lite container images
# Based on Ubuntu
############################################################
FROM ubuntu:14.04

MAINTAINER Amit Verma

### update
RUN apt-get -q -y update
RUN apt-get -q -y upgrade
RUN apt-get -q -y dist-upgrade

RUN apt-get -q -y install build-essential \
			  python \
			  python-dev \
			  python-distribute \
			  python-pip \
			  git \
			  openslide-tools \
			  python-openslide

RUN pip install flask \
		gunicorn

RUN mkdir /root/src

WORKDIR /root/src

RUN git clone --recursive https://github.com/camicroscope/oss-lite.git

WORKDIR /root/src/oss-lite

CMD ["sh", "run.sh"]
