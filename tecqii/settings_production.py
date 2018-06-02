from .settings_base import *

# DEBUG = False

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

PHANTOMJS_PATH = '/usr/bin/phantomjs'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '163.44.168.82:11211',
    }
}