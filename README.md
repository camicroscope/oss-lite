##OSS-Lite Server
Serves images using [open-slide](http://openslide.org/) as per [IIIF Image API 2.1](http://iiif.io/api/image/2.1) specifications


##Docker Container Deployment
To deploy oss-lite in a docker container, follow the following steps:
* Clone this repo
* `cd oss-lite`
* `docker build -t oss-lite .`
* `docker run -itd -p <host_port>:5000 -v <host_images_folder_path>:<host_images_folder_path> oss-lite`

##Deploying without Docker
To deploy oss-lite without Docker, follow the following steps:
* Install openslide-tools and python-openslide
On Ubuntu: `sudo apt-get install openslide-tools python-openslide`
* Insall python packages flask and gunicorn
Using pip: `pip install flask gunicorn`
* Clone this repo
* `cd oss-lite`
* `gunicorn ossliteserver:app -w <num_threads> --bind 0.0.0.0:5000`

##Usage
###Image Request API
Basic API syntax:
`{scheme}://{server}{/prefix}/{identifier}/{region}/{size}/{rotation}/{quality}.{format}`

Example:
`http://your.server/fcgi-bin/iipsrv.fcgi?IIIF=image.svs/10000,10000,400,400/full/0/default.jpg`

To learn more about image request parameters visit [IIIF Image API 2.1](http://iiif.io/api/image/2.1) webpage.

###Image Information API
API syntax:
`{scheme}://{server}{/prefix}/{identifier}/info.json`

Example:
`http://your.server/fcgi-bin/iipsrv.fcgi?IIIF=image.svs/info.json`

