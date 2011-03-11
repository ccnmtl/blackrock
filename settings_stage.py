from settings_shared import *

DATABASE_ENGINE = 'postgresql_psycopg2'

TEMPLATE_DIRS = (
    "/usr/local/share/sandboxes/common/blackrock/blackrock/templates",
)

MEDIA_ROOT = '/usr/local/share/sandboxes/common/blackrock/uploads/'

# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/usr/local/share/sandboxes/common/blackrock/blackrock/sitemedia'),     
)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

HAYSTACK_SOLR_URL = 'http://wwwappdev.cc.columbia.edu/ccnmtl/solr/blackrock_portal'

