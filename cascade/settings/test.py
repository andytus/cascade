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

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'cascade.libs.storage.S3PipelineStorage'
AWS_ACCESS_KEY_ID = 'AKIAJYAYIRX5I4M2KBYQ'
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "cartlogic"
AWS_QUERYSTRING_AUTH = False

STATIC_URL = "http://cartlogic.s3-website-us-east-1.amazonaws.com/"
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SOUTH_DATABASE_ADAPTERS ={
    'default': "south.db.postgresql_psycopg2"

}


DEBUG = True


RQ_QUEUES = {
    'default': {
        'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379'),
        'PORT': 6379,
        'DB': 0,
        },
    'high': {
        'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379'), # Heroku
        'DB': 0,
        },
    'low': {
        'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379'),
        'PORT': 6379,
        'DB': 0,
        }
}

PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.slimit.SlimItCompressor'
PIPELINE_CSS_COMPRESSOR = None

DEFAULT_FROM_EMAIL = 'My Domain <noreply@mydomain.com>'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ['SMTP_HOST']
EMAIL_HOST_USER = os.environ['MANDRILL_USER']
EMAIL_HOST_PASSWORD = os.environ['MANDRILL_APIKEY']