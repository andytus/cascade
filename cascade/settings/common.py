__author__ = 'jbennett'


# Django settings for cascade project.
import os

from django.conf import settings

ROOT_DIR = os.path.dirname(__file__)


DEBUG = True

TEMPLATE_DEBUG = DEBUG


ADMINS = (
# ('Your Name', 'your_email@example.com'),
    ('Joe', 'joe.bennett@cascadeng.com'),
    ('Joe', 'jbennett@webrapids.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cartlogictest',                      # Or path to database file if using sqlite3.
        'USER': 'admin_cartlogic',                      # Not used with sqlite3.
        'PASSWORD': 'charlize20',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}



# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.

TIME_ZONE = 'America/Detroit'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '' #'/configure/static/' #'/home/jbennett/python_projects/cascade/cascade/configure/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (

    os.path.abspath(os.path.join(ROOT_DIR,'..','configure/static' )),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    )


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ea&amp;5^_ekl^028+x4!=5a!iu43e1!amwd6nfes&amp;ik-!9trs5^zs'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    )



TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS + ( 'cascade.libs.context_processor.current_site',)


MIDDLEWARE_CLASSES = (
    'cascade.libs.middleware.MultiSiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #added on 2/20/2013
    'django.middleware.transaction.TransactionMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

ROOT_URLCONF = 'cascade.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'cascade.wsgi.application'

#
TEMPLATE_DIRS = (os.path.abspath(os.path.join(ROOT_DIR , '..', 'configure/templates')),)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'django_rq',
    'rest_framework',
    'south',
    'pipeline',
    'storages',
    'djrill',
    'cascade.apps.cartmanager',
    )

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        }
}

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/carts/app/tickets/report/'

#Storage Compression:

PIPELINE_CSS = {
    'cartlogic':{
        'source_filenames':(
            'css/cartlogic.css',
        ),
        'output_filename': 'compress/cartlogic.css',
    },
    'vendor_bootstrap':{
        'source_filenames':('css/bootstrap-responsive.min.css', 'css/bootstrap.min.css', ),
        'output_filename': 'compress/bootstrap.css'
    },

    'vendor_jquery-ui':{
        'source_filenames':('css/jquery.fileupload-ui.css', ),
        'output_filename': 'compress/jquery-ui.css'
    },


    'fonts':{
        'source_filenames':('css/font-awesome.min.css',),
        'output_filename': 'compress/font.css'
    }
 }


PIPELINE_JS = {
    'vendor_common': {
        'source_filenames': (
            'js/vendor/jquery/jquery.min.js',
            'js/vendor/bootstrap/bootstrap.js',
            'js/vendor/bootstrap/bootstrap-tab.js',
            'js/vendor/knockout/knockout-2.2.0.js',
            'js/vendor/knockout/knockout-mappings.js',
            'js/vendor/knockout/koUtilities.js'

            ),
        'output_filename': 'js/compress/vendor_common.js',
    },

    'vendor_jquery_uploads':{
        'source_filenames':(
            'js/vendor/jquery/jquery.ui.widget.js',
            'js/vendor/jquery/jquery.iframe-transport.js',
            'js/vendor/jquery/jquery.fileupload.js',


        ),

        'output_filename': 'js/compress/vendor_jquery_uploads.js',
    },

    'ajax':{
        'source_filenames': (
            'js/utilities/ajax.js',
        ),
        'output_filename': 'js/compress/ajax.js',
    },

    'common_data':{
        'source_filenames': (
            'js/utilities/common_data.js',
            ),
        'output_filename': 'js/compress/common_data.js',
        },

    'validators':{
        'source_filenames': (
            'js/utilities/validators.js',
            ),
        'output_filename': 'js/compress/validators.js',
        },

    'views_cart_list':{
        'source_filenames': (
            'js/cartmanager/views/CartListViewModel.js',
            ),
        'output_filename': 'js/compress/CartListViewModel.js',
        },

    'views_cart_profile_change_address':{
        'source_filenames': (
            'js/cartmanager/views/CartProfileChangeAddressViewModel.js',
            ),
        'output_filename': 'js/compress/CartProfileChangeAddressViewModel.js',
        },

    'views_cart_profile':{
        'source_filenames': (
            'js/cartmanager/views/CartProfileViewModel.js',
            ),
        'output_filename': 'js/compress/CartProfileViewModel.js',
        },
    'views_cart_search':{
        'source_filenames': (
            'js/cartmanager/views/CartSearchViewModel.js',
            ),
        'output_filename': 'js/compress/CartSearchViewModel.js',
        },
    'views_customer_new':{
        'source_filenames': (
            'js/cartmanager/views/CustomerNewViewModel.js',
            ),
        'output_filename': 'js/compress/CustomerNewViewModel.js',
        },
    'views_customer_profile':{
        'source_filenames': (
            'js/cartmanager/views/CustomerProfileViewModel.js',
            ),
        'output_filename': 'js/compress/CustomerProfileViewModel.js',
        },
    'views_location_search':{
        'source_filenames': (
            'js/cartmanager/views/LocationSearchViewModel.js',
            ),
        'output_filename': 'js/compress/LocationSearchViewModel.js',
        },
    'views_ticket_create':{
        'source_filenames': (
            'js/cartmanager/views/TicketCreateViewModel.js',
            ),
        'output_filename': 'js/compress/TicketCreateViewModel.js',
        },
    'views_ticket_profile':{
        'source_filenames': (
            'js/cartmanager/views/TicketProfileViewModel.js',
            ),
        'output_filename': 'js/compress/TicketProfileViewModel.js',
        },
    'views_tickets_list':{
        'source_filenames': (
            'js/cartmanager/views/TicketsListViewModel.js',
            ),
        'output_filename': 'js/compress/TicketsListViewModel.js',
        },
    'views_tickets_report':{
        'source_filenames': (
            'js/cartmanager/views/TicketsReportViewModel.js',
            ),
        'output_filename': 'js/compress/TicketsReportViewModel.js',
        },

    'models_cart':{
        'source_filenames': (
            'js/cartmanager/models/cart.js',
            ),
        'output_filename': 'js/compress/cart.js',
        },

    'models_cart_profile':{
        'source_filenames': (
            'js/cartmanager/models/cart_profile.js',
            ),
        'output_filename': 'js/compress/cart_profile.js',
        },

    'models_cart_status':{
        'source_filenames': (
            'js/cartmanager/models/cart_status.js',
            ),
        'output_filename': 'js/compress/cart_status.js',
        },

    'models_cart_type':{
        'source_filenames': (
            'js/cartmanager/models/cart_type.js',
            ),
        'output_filename': 'js/compress/cart_type.js',
        },

    'models_comments':{
        'source_filenames': (
            'js/cartmanager/models/comments.js',
            ),
        'output_filename': 'js/compress/comments.js',
        },

    'models_customer':{
        'source_filenames': (
            'js/cartmanager/models/customer.js',
            ),
        'output_filename': 'js/compress/customer.js',
        },

    'models_form_steps':{
        'source_filenames': (
            'js/cartmanager/models/form_steps.js',
            ),
        'output_filename': 'js/compress/form_steps.js',
        },

    'models_location':{
        'source_filenames': (
            'js/cartmanager/models/location.js',
            ),
        'output_filename': 'js/compress/location.js',
        },

    'models_map':{
        'source_filenames': (
            'js/cartmanager/models/map.js',
            ),
        'output_filename': 'js/compress/map.js',
        },

    'models_ticket':{
        'source_filenames': (
            'js/cartmanager/models/ticket.js',
            ),
        'output_filename': 'js/compress/ticket.js',
        },

    'models_ticket_services':{
        'source_filenames': (
            'js/cartmanager/models/ticket_services.js',
            ),
        'output_filename': 'js/compress/ticket_services.js',
        },

    'models_ticket_status':{
        'source_filenames': (
            'js/cartmanager/models/ticket_status.js',
            ),
        'output_filename': 'js/compress/ticket_status.js',
        },

    }


DEFAULT_FROM_EMAIL = os.environ['MANDRILL_USERNAME']
EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'
EMAIL_HOST = os.environ['SMTP_HOST']
EMAIL_HOST_PASSWORD = os.environ['MANDRILL_APIKEY']
SERVER_EMAIL = os.environ['MANDRILL_USERNAME']
EMAIL_USE_TLS = True
MANDRILL_API_KEY = os.environ['MANDRILL_APIKEY']
