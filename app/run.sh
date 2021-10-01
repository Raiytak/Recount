#!/bin/bash
cd /home/mathieu/Desktop/Projets/Recount/app
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn -c gunicorn.conf.py --chdir src/ "wsgi:create_app('production')"

