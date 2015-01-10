import os
import json
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CONFIG_FILE_NAME = '/etc/randomcab/main.ini'
INSTALL_DIR = ""

from configparser import RawConfigParser
config = RawConfigParser()

if os.path.exists(CONFIG_FILE_NAME):
    DEBUG = False
    config.read(CONFIG_FILE_NAME)
    INSTALL_DIR = config.get('directories', 'INSTALL_DIR')
else:
    DEBUG = True    
    INSTALL_DIR = "/".join(os.getcwd().split('/')[:-1]);
    config.read(INSTALL_DIR+CONFIG_FILE_NAME)
   

if INSTALL_DIR is None:
    raise Exception("INSTALL_DIR not defined")
    
    
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Admin', 'info@randomcab.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': 'sqlite.db',                     
    }
}

FLICKR_API_KEY = config.get('secrets', 'FLICKR_API_KEY')
FLICKR_API_SECRET = config.get('secrets', 'FLICKR_API_SECRET')


DEFAULT_FROM_EMAIL='info@randomcab.com'
LOG_EMAIL=config.get('mail', 'LOG_EMAIL')
SERVER_EMAIL='django@randomcab.com'

EMAIL_BACKEND = "randomcab.backends.mail.MailFailOverBackend"
EMAIL_BACKEND_LIST = json.loads(config.get('mail', 'EMAIL_BACKEND_LIST'))['mailservers']


ALLOWED_HOSTS = [".randomcab.com"]
TIME_ZONE = 'Europe/Amsterdam'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True



STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    INSTALL_DIR + "/resources/static",
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = config.get('secrets', 'SECRET_KEY')
    

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'randomcab.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'randomcab.wsgi.application'


TEMPLATE_DIRS = (
    INSTALL_DIR + "/resources/templates",
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #3rd party
    'widget_tweaks',

 
    #randomcab   
    'randomcab.home',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

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
