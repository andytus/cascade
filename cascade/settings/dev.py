from common import *


RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        #'PASSWORD': 'some-password',
        },
    'high': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0
        },
    'low': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar', )


PIPELINE_ENABLED = False
PIPELINE = False

EMAIL_SUBJECT_PREFIX = '[CartLogic-Dev]'
ALLOWED_HOSTS = ALLOWED_HOSTS + ['*']

