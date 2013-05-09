from common import *

# Parse database configuration from $DATABASE_URL
from urlparse import urlparse
#import dj_database_url
#DATABASES['default'] =  dj_database_url.config()
#

if os.environ.has_key('DATABASE_URL'):
    url = urlparse(os.environ['DATABASE_URL'])
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': url.path[1:],
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port,
        }


STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJYAYIRX5I4M2KBYQ'
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "cartlogic"

STATIC_URL = "http://cartlogic.s3-website-us-east-1.amazonaws.com/"


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SOUTH_DATABASE_ADAPTERS ={
'default': "south.db.postgresql_psycopg2"

}

DEBUG = False