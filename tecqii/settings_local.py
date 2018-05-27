from .settings_base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "dev.db",
        'OPTIONS': {
            'timeout': 15,
        }
    }
}


DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'projectdata',
       'USER': 'projectdatauser',
       'PASSWORD': 'password',
       'HOST': 'localhost',
       'PORT': '',
   }
}

PHANTOMJS_PATH = '/usr/local/bin/phantomjs'