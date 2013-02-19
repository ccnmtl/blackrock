from settings_shared import *

DATABASE_ENGINE = 'postgresql_psycopg2'

TEMPLATE_DIRS = (
    "/usr/local/share/sandboxes/common/blackrock/blackrock/templates",
)

MEDIA_ROOT = '/usr/local/share/sandboxes/common/blackrock/uploads/'

# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia',
     '/usr/local/share/sandboxes/common/blackrock/blackrock/sitemedia'),
)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

HAYSTACK_SOLR_URL = \
    'http://wwwappdev.cc.columbia.edu/ccnmtl/solr/blackrock_portal'
HAYSTACK_SITECONF = 'portal.search_sites'
HAYSTACK_SEARCH_ENGINE = 'solr'
BLACK_ROCK_FEED = 'http://ccnmtl.columbia.edu/projects/blackrock/forestdata/'


try:
    from local_settings import *
except ImportError:
    pass
