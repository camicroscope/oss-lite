## OSS-Lite Server
OSS-Lite (OpenSlide Server-Lite) is a lightweight python web service that implements the [IIIF Image API 2.1](http://iiif.io/api/image/2.1) specifications, and is built using the excellent digital pathology library called [OpenSlide](http://openslide.org/) 

## Usage

### Getting started
Place all the images that are to be exposed to the API in a base folder. Let's call it `/data/myImages/` for this example. The images could be organized in subfolders. E.g. 
`/data/myImages/imageDir1`, 
`/data/myImages/imageDir2`. 
The image files could be orgazied in the folders as:
`/data/myImages/imageDir1/image1.svs`
`/data/myImages/imageDir1/image2.svs`
`/data/myImages/imageDir2/image3.svs`

Having set up the images and deploying oss-lite using deployement instructions, the service could be accessed using the following API calls.

### Image Request API
Basic API syntax:
`{scheme}://{server}{/filepath}/{filename_with_extension}/{region}/{size}/{rotation}/{quality}.{format}`

Example:
`http://localhost/data/myImages/imageDir2/image1.svs/8000,9000,400,400/full/0/default.jpg`
This returns a 400x400 tile starting at the left corner <8000,9000>, in JPEG format, from an image with filename image1.svs that is placed at /data/myImages on the host machine.
To learn more about image request parameters visit [IIIF Image API 2.1](http://iiif.io/api/image/2.1) webpage.

#### Image Information API
API syntax:
`{scheme}://{server}{/filepath}/{filename_with_extension}/info.json`
Example:
`http://localhost/data/myImages/imageDir2/image1.svs/info.json`

## Docker Container Deployment
Here we assume that all the images are in the base folder `/data/myImages` on the host machine and oss-lite will be deployed in a container and accessible at `http://localhost/image-service`
To deploy oss-lite in a docker container, follow the following steps:
* Clone this repo
* `cd oss-lite`
* `docker build -t oss-lite .`
* `docker run -itd -p <host_port>:5000 -v /data/myImages:/data/myImages oss-lite`
This resutling docker container uses run.sh to start oss-lite as a daemon.

While deploying it along with [Camicroscope Distro](https://github.com/camicroscope/Distro). Find out `$CAMIC_IMAGES_DIR` ([How?](https://github.com/camicroscope/Distro/blob/master/install.sh#L13)), it is the directory on the host machine where all the images are stored by the image loader. Image loader will load images with path `/data/images`.

`docker run -itd -p <host_port>:5000 -v $CAMIC_IMAGES_DIR:/data/images oss-lite`

## Deploying without Docker
To deploy oss-lite without Docker, follow the following steps:
* Install openslide-tools and python-openslide
On Ubuntu: `sudo apt-get install openslide-tools python-openslide`
* Insall python packages flask and gunicorn
Using pip: `pip install flask gunicorn`
* Clone this repo
* `cd oss-lite`
* `gunicorn ossliteserver:app -w <num_threads> --bind 0.0.0.0:5000`

