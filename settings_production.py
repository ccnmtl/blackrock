from settings_shared import *

DATABASE_ENGINE = 'postgresql_psycopg2' # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.

TEMPLATE_DIRS = (
    "/var/www/blackrock/blackrock/templates",
)

MEDIA_ROOT = '/var/www/blackrock/uploads/'

DEBUG = False
TEMPLATE_DEBUG = DEBUG
HAYSTACK_SOLR_URL = "http://wwwapp.cc.columbia.edu/ccnmtl/solr/blackrock_portal"
