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
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'localhost:6379',
        'OPTIONS': {'DB': 0},
    }

}


PIPELINE_ENABLED = False

EMAIL_SUBJECT_PREFIX = '[CartLogic-Dev]'