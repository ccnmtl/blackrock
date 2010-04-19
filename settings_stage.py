from settings_shared import *

DATABASE_ENGINE = 'postgresql_psycopg2'

TEMPLATE_DIRS = (
    "/usr/local/share/sandboxes/common/blackrock/blackrock/templates",
)

MEDIA_ROOT = '/usr/local/share/sandboxes/common/blackrock/uploads/'

DEBUG = False
TEMPLATE_DEBUG = DEBUG
