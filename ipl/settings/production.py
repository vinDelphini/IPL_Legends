import os
from ipl.settings.base import *

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        "ENGINE":  "django.db.backends.postgresql_psycopg2",
        "NAME":  "ipllegends",
        "USER":  "postgres",
        "PASSWORD":  "asdfghjkl",
        "HOST":  "ipllegends.c3q2g6ckoaii.ap-southeast-2.rds.amazonaws.com",
        "PORT":  "5432",
    }
}
