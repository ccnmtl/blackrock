# flake8: noqa
import os.path
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()

MANAGERS = ADMINS

ALLOWED_HOSTS = ['.ccnmtl.columbia.edu', 'localhost']

# fake. overriden in local_settings.py
SECRET_KEY = ')ng#)ef_u@_^zvvu@dxm7ql-yb^_!a6%v3v^j3b(mp+)l+5%@h'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'blackrock',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
        'ATOMIC_REQUESTS': True,
    }
}

if 'test' in sys.argv or 'jenkins' in sys.argv or 'validate' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.spatialite',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
            'ATOMIC_REQUESTS': True,
        }
    }


JENKINS_TASKS = (
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

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

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
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.template.context_processors.static',
    'django.template.context_processors.media',
    'blackrock.blackrock_main.views.django_settings',
    'stagingcontext.staging_processor',
    'djangowind.context.context_processor',
)

MIDDLEWARE_CLASSES = [
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'blackrock.portal.middleware.ValueErrorMiddleware',
]

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
    'django_databrowse',
    'googlecharts',
    'haystack',
    'smartif',
    'tinymce',
    'pagetree',
    'pageblocks',
    'template_utils',
    'blackrock.waterquality',
    'blackrock.mammals',
    'bootstrapform',
    'django_jenkins',
    'smoketest',
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

EMAIL_SUBJECT_PREFIX = "[blackrock] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "blackrock@ccnmtl.columbia.edu"


LOGIN_URL = "/admin/login"

COMPRESS_URL = "/media/"
COMPRESS_ROOT = "media/"

AUTHENTICATION_BACKENDS = ('djangowind.auth.SAMLAuthBackend',
                           'django.contrib.auth.backends.ModelBackend')

CAS_BASE = "https://cas.columbia.edu/"
WIND_PROFILE_HANDLERS = ['djangowind.auth.CDAPProfileHandler']
WIND_AFFIL_HANDLERS = ['djangowind.auth.AffilGroupMapper',
                       'djangowind.auth.StaffMapper',
                       'djangowind.auth.SuperuserMapper']
WIND_STAFF_MAPPER_GROUPS = ['tlc.cunix.local:columbia.edu']
WIND_SUPERUSER_MAPPER_GROUPS = [
    'anp8', 'jb2410', 'zm4', 'cld2156',
    'sld2131', 'amm8', 'mar227', 'lrw2128', 'njn2118']


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

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://wwwappdev.cc.columbia.edu/ccnmtl/solr/blackrock_portal',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 10,
    },
}

CDRS_SOLR_URL = 'http://solrdev.cul.columbia.edu:8080/solr/blackrock'
CDRS_SOLR_FILEURL = 'http://solrdev.cul.columbia.edu:8080/solr/blackrock/files/'

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
