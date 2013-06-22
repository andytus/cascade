from common import *


RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        #'PASSWORD': 'some-password',
        },
    'high': {
        'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379'), # If you're on Heroku
        'DB': 0,
        },
    'low': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        }
}

PIPELINE_ENABLED = False


#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'localhost'
#EMAIL_PORT = 9999
#SERVER_EMAIL = "cartlogic@dev.com"


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'app15581190@heroku.com'
EMAIL_HOST_PASSWORD = 'acBTdIlNFLJ4wR-KWHhxsw'