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


DEFAULT_FROM_EMAIL = 'app15581190@heroku.com'

EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'app15581190@heroku.com'
EMAIL_USE_TLS = True
SERVER_EMAIL =  'app15581190@heroku.com'

MANDRILL_API_KEY = "acBTdIlNFLJ4wR-KWHhxsw"