# flake8: noqa
import os.path
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('admin', 'sysadmin@example.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['.ccnmtl.columbia.edu', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'blackrock',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
    }
}

if 'test' in sys.argv or 'jenkins' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.spatialite',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
        }
    }

    HAYSTACK_SITECONF = 'blackrock.portal.search_sites'
    HAYSTACK_SEARCH_ENGINE = 'solr'
    HAYSTACK_SOLR_URL = \
        'http://wwwapp.cc.columbia.edu/ccnmtl/solr/blackrock_portal'
    CDRS_SOLR_URL = HAYSTACK_SOLR_URL

    SOUTH_DATABASE_ADAPTERS = {
        'default': "south.db.sqlite3"
    }


JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)


PROJECT_APPS = ['blackrock.blackrock_main',
                'blackrock.mammals',
                'blackrock.optimization',
                'blackrock.paleoecology',
                'blackrock.portal',
                'blackrock.respiration',
                'blackrock.sampler',
                'blackrock.waterquality']

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    "--exclude-dir-file=nose_exclude.txt",
    '--cover-package=blackrock.respiration,blackrock.blackrock_main,blackrock.mammals,blackrock.waterquality,blackrock.portal,blackrock.sampler,blackrock.optimization',
]
SOUTH_TESTS_MIGRATE = False

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = "/var/www/blackrock/uploads/"
MEDIA_URL = '/uploads/'
STATIC_URL = '/media/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'blackrock.blackrock_main.views.django_settings',
    'stagingcontext.staging_processor',
)

MIDDLEWARE_CLASSES = (
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'blackrock.portal.middleware.ValueErrorMiddleware',
)

ROOT_URLCONF = 'blackrock.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # Put application templates before these fallback ones:
    "/var/www/blackrock/blackrock/templates/",
    os.path.join(os.path.dirname(__file__), "templates"),
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.humanize',
    'sorl.thumbnail',
    'compressor',
    'django_statsd',
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
    'blackrock.waterquality',
    'googlecharts',
    'blackrock.mammals',
    'south',
    'django_nose',
    'django_jenkins',
    'smoketest',
    'annoying',
]

# Pageblocks/Pagetree settings
PAGEBLOCKS = ['pageblocks.HTMLBlockWYSIWYG',
              'pageblocks.ImageBlock',
              'pageblocks.TextBlock',
              'pageblocks.HTMLBlock',
              'portal.AssetList',
              'portal.FeaturedAsset',
              'portal.PhotoGallery',
              'portal.Webcam',
              'portal.Weather',
              'portal.InteractiveMap']

THUMBNAIL_SUBDIR = "thumbs"
# THUMBNAIL_DEBUG = "True"

LOGIN_URL = "/admin/login"

COMPRESS_ROOT = "/var/www/blackrock/blackrock/media/"

# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', 'sitemedia'),
)

STATSD_CLIENT = 'statsd.client'
STATSD_PREFIX = 'blackrock'
STATSD_HOST = '127.0.0.1'
STATSD_PORT = 8125
STATSD_PATCHES = ['django_statsd.patches.db', ]

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

FIVE_HOURS = 60 * 60 * 5
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = FIVE_HOURS

MAX_DATA_COUNT = 12000

# if you add a 'deploy_specific' directory
# then you can put a settings.py file and templates/ overrides there
try:
    from blackrock.deploy_specific.settings import *
except ImportError:
    pass
