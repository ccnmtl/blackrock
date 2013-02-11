from settings_shared import *

DATABASE_ENGINE = 'postgresql_psycopg2'

TEMPLATE_DIRS = (
    "/var/www/blackrock/blackrock/templates",
)

MEDIA_ROOT = '/var/www/blackrock/uploads/'

# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/blackrock/blackrock/sitemedia'),
)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

HAYSTACK_SITECONF = 'portal.search_sites'
HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SOLR_URL = \
    "http://wwwapp.cc.columbia.edu/ccnmtl/solr/blackrock_portal"

try:
    from local_settings import *
except ImportError:
    pass
