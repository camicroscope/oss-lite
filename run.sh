#!/bin/bash
gunicorn /root/src/oss-lite/ossliteserver:app -w 4 --bind 0.0.0.0:5000
while true; do sleep 1000; done
