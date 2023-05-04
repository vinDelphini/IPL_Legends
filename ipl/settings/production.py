import os
from dashboard.settings.base import *

DATABASES = {
    'default': {
        "ENGINE":  "django.db.backends.postgresql_psycopg2",
        "NAME":  "ipllegends",
        "USER":  "postgres",
        "PASSWORD":  "asdfghjkl",
        "HOST":  "ipl-db.c1utzps5ta5g.us-east-1.rds.amazonaws.com",
        "PORT":  "5432",
    }
}
