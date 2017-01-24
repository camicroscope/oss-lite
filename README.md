##OSS-Lite Server
OSS-Lite (OpenSlide Server-Lite) is a lightweight python web service that implements the [IIIF Image API 2.1](http://iiif.io/api/image/2.1) specifications, and is built using the excellent digital pathology library called [OpenSlide](http://openslide.org/) 

##Usage
###Image Request API
Basic API syntax:
`{scheme}://{server}{/prefix}/{identifier}/{region}/{size}/{rotation}/{quality}.{format}`

Example:
`http://localhost/image-service/UID-12-2463/8000,9000,400,400/full/0/default.jpg`
This returns a 400x400 tile, from an image with the identifier UID-12-2463, who's top left corner is <8000,9000>
To learn more about image request parameters visit [IIIF Image API 2.1](http://iiif.io/api/image/2.1) webpage.

####Image Information API
API syntax:
`{scheme}://{server}{/prefix}/{identifier}/info.json`
Example:
`http://localhost/image-service/UID-12-2463/info.json`

##Docker Container Deployment
Here we assume that all the images are in the base folder `/data/myImages/` on the host machine and oss-lite will be deployed in a container and accessible at `http://localhost/image-service`
To deploy oss-lite in a docker container, follow the following steps:
* Clone this repo
* `cd oss-lite`
* `docker build -t oss-lite .`
* `docker run -itd -p <host_port>:5000 -v /data/myImages/:/image-service oss-lite`

While deploying it along with [Camicroscope Distro](https://github.com/camicroscope/Distro). Find out `$CAMIC_IMAGES_DIR` ([How?](https://github.com/camicroscope/Distro/blob/master/install.sh#L13)), it is the directory on the host machine where all the images are stored by the image loader. Image loader will load images with path `/data/images`.

`docker run -itd -p <host_port>:5000 -v $CAMIC_IMAGES_DIR:/data/images oss-lite`

##Deploying without Docker
To deploy oss-lite without Docker, follow the following steps:
* Install openslide-tools and python-openslide
On Ubuntu: `sudo apt-get install openslide-tools python-openslide`
* Insall python packages flask and gunicorn
Using pip: `pip install flask gunicorn`
* Clone this repo
* `cd oss-lite`
* `gunicorn ossliteserver:app -w <num_threads> --bind 0.0.0.0:5000`

