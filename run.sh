#!/bin/bash
gunicorn ossliteserver:app -w 4 --bind 127.0.0.1:5000
while true; do sleep 1000; done
