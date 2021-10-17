#!/bin/bash
cd /home/$USER/Desktop/Projets/Recount/app
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn -c gunicorn.conf.py "wsgi:create_app('production')"

