# flake8: noqa
from settings_shared import *

DATABASE_ENGINE = 'postgresql_psycopg2'

TEMPLATE_DIRS = (
    "/var/www/blackrock/blackrock/blackrock/templates",
)

MEDIA_ROOT = '/var/www/blackrock/uploads/'

# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/blackrock/blackrock/sitemedia'),
)


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'blackrock',
        'HOST': '',
        'PORT': 6432,  # see /etc/pgbouncer/pgbouncer.ini
        'USER': '',
        'PASSWORD': '',
    }
}

DEBUG = False
TEMPLATE_DEBUG = DEBUG

STATSD_PREFIX = 'blackrock-staging'
STAGING_ENV = True

SENTRY_SITE = 'blackrock-staging'
SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

try:
    from local_settings import *
except ImportError:
    pass
