from .base import *
import os
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# SECRET_KEY = '2v0z+*)r%3ylr*neqjya=mps%^h6p4_d_g3=gmti2iqr(%*6p^'
ALLOWED_HOSTS = ["*"]
ENCRYPTION_KEY = '12345678'
INI_VEC = '2456789'
ENCRYPTION_REQUIRED = False

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
# 	'default': {
# 		'ENGINE': 'django.db.backends.postgresql_psycopg2',
# 		'NAME': 'db_3',
# 		'USER': 'postgres',
# 		'PASSWORD': 'gpsoft$%^GY2'
# 		'HOST': os.getenv("DB_HOST_LOCAL","NOT FOUNT"), #3.222.63.70
# 		'PORT': os.getenv("DB_PORT",5432),
# 	}
# }

