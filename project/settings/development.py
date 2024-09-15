from .base import *
import os
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# SECRET_KEY = os.getenv("SECRET_KEY","")
ALLOWED_HOSTS = ["*"]
ENCRYPTION_KEY = '12345678'
INI_VEC = '2456789'
ENCRYPTION_REQUIRED = True

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

    }
}
# DATABASES = {
# 	'default': {
# 		'ENGINE': 'django.db.backends.postgresql_psycopg2',
# 		'NAME': os.getenv("DB_NAME","NOT FOUNT"),
# 		'USER': os.getenv("DB_USER","NOT FOUNT"),
# 		'PASSWORD': os.getenv("DB_PASSWORD","NOT FOUNT"),
# 		'HOST': os.getenv("DB_HOST","NOT FOUNT"),
# 		'PORT': os.getenv("DB_PORT",5432),
# 	}
# }