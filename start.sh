#!/bin/bash

sudo service nginx reload
../virtualenv/bin/gunicorn --bind \
unix:/tmp/superlists-192.168.199.189.socket \
superlists.wsgi:application
