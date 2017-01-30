############################################################
# Dockerfile to build Oss-lite container images
# Based on Ubuntu
############################################################
FROM ubuntu:14.04

MAINTAINER Sapoonjyoti DuttaDuwarah

### update
RUN apt-get -q -y update
RUN apt-get -q -y upgrade
RUN apt-get -q -y dist-upgrade
RUN apt-get -q -y install openssh-server
RUN apt-get install -q -y curl

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




### need build tools for building openslide and later iipsrv
RUN apt-get -q -y install git autoconf automake make libtool pkg-config cmake


## get our configuration files
WORKDIR /root/src
RUN git clone https://tcpan@bitbucket.org/tcpan/iip-openslide-docker.git

## setup a mount point for images.  - this is external to the docker container.
RUN mkdir -p /mnt/images

### set up the ssh daemon
RUN mkdir /var/run/sshd
RUN echo 'root:iipdocker' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
## expose some ports
EXPOSE 22


# build with
#  sudo docker build --rm=true -t="repo/imgname" .

### need build tools for building openslide and later iipsrv
RUN apt-get -q -y install git autoconf automake make libtool pkg-config cmake

## setup a mount point for images.  - this is external to the docker container.
RUN mkdir -p /mnt/images


### prereqs for openslide
RUN apt-get -q -y install zlib1g-dev libpng12-dev libjpeg-dev libtiff5-dev libgdk-pixbuf2.0-dev libxml2-dev libsqlite3-dev libcairo2-dev libglib2.0-dev

#Libraries that are needed for openslide 
RUN curl -O -J -L http://downloads.sourceforge.net/lcms/lcms2-2.7.tar.gz && \
tar -xzvf lcms2-2.7.tar.gz && \
cd lcms2-2.7 && ./configure && \
make -j4 && make install && \
cd .. && rm -rf lcms2-2.7* 

RUN curl -O -J -L http://downloads.sourceforge.net/libpng/libpng-1.6.22.tar.xz && \
tar -xvf libpng-1.6.22.tar.xz && \
cd libpng-1.6.22 && ./configure && \
make -j4 && make install && \
cd .. && rm -rf libpng-1.6.22*

RUN curl -O -J -L http://download.osgeo.org/libtiff/tiff-4.0.6.tar.gz && \
tar -xzvf tiff-4.0.6.tar.gz && \
cd tiff-4.0.6 && ./configure && \
make -j4 && make install && \
cd .. && rm -rf tiff-4.0.6* 

RUN curl -O -J -L http://downloads.sourceforge.net/openjpeg.mirror/openjpeg-2.1.0.tar.gz && \
tar -xzvf openjpeg-2.1.0.tar.gz && \
cd openjpeg-2.1.0 && mkdir build && \
cd build && cmake ../ && \
make -j4 && make install && \
cd ../.. && rm -rf openjpeg-2.1.0*

WORKDIR /root/src


COPY run.sh /root/run.sh

CMD ["sh","/root/run.sh"]
