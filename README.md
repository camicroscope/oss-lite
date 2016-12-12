##OSS-Lite Server
A service to serve images using open-slide as per IIIF Image API specifications

##Docker Container Deployment
To deploy oss-lite in a docker container, follow the following steps:
* Clone this repo
* cd oss-lite
* docker build -t oss-lite .
* docker run -p <host_port>:5000 -v <host_images_folder_path>:<host_images_folder_path> oss-lite

##Deploying without Docker
To deploy oss-lite without Docker, follow the following steps:
* Install openslide-tools and python-openslide
On Ubuntu: `sudo apt-get install openslide-tools python-openslide`
* Insall python packages flask and gunicorn
Using pip: `pip install flask gunicorn`
* Clone this repo
* cd oss-lie
* gunicorn ossliteserver:app -w <no_threads> --bind 0.0.0.0:5000

##Usage
