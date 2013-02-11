# Django settings for blackrock project.
import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('admin', 'sysadmin@example.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'blackrock'  # Or path to database file if using sqlite3.
DATABASE_USER = ''  # Not used with sqlite3.
DATABASE_PASSWORD = ''  # Not used with sqlite3.
DATABASE_HOST = ''  # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''  # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = "/var/www/blackrock/uploads/"
MEDIA_URL = '/uploads/'
ADMIN_MEDIA_PREFIX = '/media/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'blackrock.blackrock_main.views.django_settings',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'blackrock.portal.middleware.ValueErrorMiddleware'
)

ROOT_URLCONF = 'blackrock.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # Put application templates before these fallback ones:
    "/var/www/blackrock/templates/",
    os.path.join(os.path.dirname(__file__), "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.humanize',
    'sorl.thumbnail',
    'django.contrib.gis',
    'django.contrib.admin',
    'blackrock.sampler',
    'blackrock.respiration',
    'blackrock.optimization',
    'blackrock.paleoecology',
    'blackrock.blackrock_main',
    'blackrock.portal',
    'django.contrib.databrowse',
    'gspreadsheet_importer',
    'haystack',
    'smartif',
    'tinymce',
    'pagetree',
    'pageblocks',
    'template_utils',
    'typogrify',
    'sentry.client',
    'waterquality',
    'googlecharts',
    'mammals',
    'south',
)

# Pageblocks/Pagetree settings
PAGEBLOCKS = ['pageblocks.HTMLBlockWYSIWYG',
              'pageblocks.ImageBlock',
              'portal.AssetList',
              'portal.FeaturedAsset',
              'pageblocks.TextBlock',
              'portal.PhotoGallery',
              'portal.Webcam',
              'portal.Weather',
              'portal.InteractiveMap',
              'pageblocks.HTMLBlock']

THUMBNAIL_SUBDIR = "thumbs"
# THUMBNAIL_DEBUG = "True"

LOGIN_URL = "/admin/login"

# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', 'sitemedia'),
)

# TinyMCE settings
TINYMCE_JS_URL = '/site_media/js/tiny_mce/tiny_mce.js'
TINYMCE_JS_ROOT = 'media/js/tiny_mce'

# if you set this to True, you may have to
# override TINYMCE_JS_ROOT with the full path on production
TINYMCE_COMPRESSOR = False
TINYMCE_SPELLCHECKER = True

TINYMCE_DEFAULT_CONFIG = {'cols': 80,
                          'rows': 30,
                          'plugins': 'table,spellchecker,paste,searchreplace',
                          'theme': 'simple'}

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 900

MAX_DATA_COUNT = 12000

# if you add a 'deploy_specific' directory
# then you can put a settings.py file and templates/ overrides there
try:
    from blackrock.deploy_specific.settings import *
    INSTALLED_APPS = INSTALLED_APPS + ('blackrock.deploy_specific',)

    if 'EXTRA_INSTALLED_APPS' in locals():
        INSTALLED_APPS = EXTRA_INSTALLED_APPS + INSTALLED_APPS
except ImportError:
    pass
