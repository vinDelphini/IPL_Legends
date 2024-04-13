import os
from ipl.settings.base import *

ALLOWED_HOSTS = ["ec2-13-55-65-113.ap-southeast-2.compute.amazonaws.com"]

DATABASES = {
    'default': {
        "ENGINE":  "django.db.backends.postgresql_psycopg2",
        "NAME":  "postgres",
        "USER":  "postgres",
        "PASSWORD":  "asdfghjkl",
        "HOST":  "ipllegends.c3q2g6ckoaii.ap-southeast-2.rds.amazonaws.com",
        "PORT":  "5432",
    }
}
