#!/bin/bash

sudo service bash
../virtualenv/bin/gunicorn superlists.wsgi:application
