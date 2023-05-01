#!/usr/bin/env bash

# kill python server
sudo pkill -f runserver

sudo chown -R $USER /home/ubuntu/ipllegends/

# install postgresql
sudo apt -y install postgresql-12 postgresql-client-12

pip install setuptools==44.0.0
pip install wheel
pip install psycopg2==2.8.6
pip install psycopg2-binary==2.8.6

pip install -r /home/ubuntu/ipllegends/requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic

screen -d -m python3 manage.py runserver 0:8000
