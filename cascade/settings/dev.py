from common import *


STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJYAYIRX5I4M2KBYQ'
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "cartlogic"

STATIC_URL = "http://cartlogic.s3-website-us-east-1.amazonaws.com/"
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SOUTH_DATABASE_ADAPTERS ={
    'default': "south.db.postgresql_psycopg2"

}

