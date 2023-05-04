import os
from ipl.settings.base import *

ALLOWED_HOSTS = ["ec2-54-163-215-193.compute-1.amazonaws.com"]

DATABASES = {
    'default': {
        "ENGINE":  "django.db.backends.postgresql_psycopg2",
        "NAME":  "postgres",
        "USER":  "postgres",
        "PASSWORD":  "asdfghjkl",
        "HOST":  "ipl-db.c1utzps5ta5g.us-east-1.rds.amazonaws.com",
        "PORT":  "5432",
    }
}
