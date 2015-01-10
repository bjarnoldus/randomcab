#!/bin/bash

sudo postfix start
python3 manage.py migrate --noinput
python3 manage.py runserver 
