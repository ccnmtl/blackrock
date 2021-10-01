import distro
import os.path
import sys
from ccnmtlsettings.shared import common

project = 'blackrock'
base = os.path.dirname(__file__)
locals().update(common(project=project, base=base))

if 'ubuntu' in distro.linux_distribution()[0].lower():
    if distro.linux_distribution()[1] == '16.04':
        # 15.04 and later need this set, but it breaks
        # on trusty.
        SPATIALITE_LIBRARY_PATH = 'mod_spatialite'
    elif distro.linux_distribution()[1] == '18.04':
        # On Debian testing/buster, I had to do the following:
        # * Install the sqlite3 and libsqlite3-mod-spatialite packages.
        # * Add the following to writlarge/local_settings.py:
        # SPATIALITE_LIBRARY_PATH =
        # '/usr/lib/x86_64-linux-gnu/mod_spatialite.so' I think the
        # django docs might be slightly out of date here, or just not
        # cover all the cases.
        #
        # I've found that Ubuntu 18.04 also works with this full path
        # to the library file, but not 'mod_spatialite'. I'll raise
        # this issue with Django.
        SPATIALITE_LIBRARY_PATH = '/usr/lib/x86_64-linux-gnu/mod_spatialite.so'
elif 'debian' in distro.linux_distribution()[0].lower():
    SPATIALITE_LIBRARY_PATH = '/usr/lib/x86_64-linux-gnu/mod_spatialite.so'


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

PROJECT_APPS = [
    'blackrock.blackrock_main',
    'blackrock.mammals',
    'blackrock.optimization',
    'blackrock.paleoecology',
    'blackrock.portal',
    'blackrock.respiration',
    'blackrock.treegrowth',
    'blackrock.waterquality',
]

MIDDLEWARE += [  # noqa
    'blackrock.portal.middleware.ValueErrorMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django_cas_ng.middleware.CASMiddleware',
]

INSTALLED_APPS += [  # noqa
    'sorl.thumbnail',
    'django.contrib.gis',
    'blackrock.respiration',
    'blackrock.optimization',
    'blackrock.paleoecology',
    'blackrock.blackrock_main',
    'blackrock.portal',
    'django_databrowse',
    'googlecharts',
    'haystack',
    'tinymce',
    'pagetree',
    'pageblocks',
    'blackrock.waterquality',
    'blackrock.mammals',
    'bootstrapform',
    'django_extensions',
    'django_cas_ng',
    'django.contrib.humanize'
]

INSTALLED_APPS.remove('djangowind') # noqa

# Pageblocks/Pagetree settings
PAGEBLOCKS = [
    'pageblocks.HTMLBlockWYSIWYG',
    'pageblocks.ImageBlock',
    'pageblocks.TextBlock',
    'pageblocks.HTMLBlock',
    'portal.AssetList',
    'portal.FeaturedAsset',
    'portal.PhotoGallery',
    'portal.Webcam',
    'portal.Weather',
    'portal.InteractiveMap',
]

LOGIN_URL = "/admin/login"

# TinyMCE settings
TINYMCE_JS_URL = '/media/js/tiny_mce/tiny_mce.js'
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

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

MAX_DATA_COUNT = 12000

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://localhost:8080/solr/blackrock_portal',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 10,
    },
}

CDRS_SOLR_URL = 'http://solrdev.cul.columbia.edu:8080/solr/blackrock'
CDRS_SOLR_FILEURL = \
    'http://solrdev.cul.columbia.edu:8080/solr/blackrock/files/'

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend'
]

CAS_SERVER_URL = 'https://cas.columbia.edu/cas/'
CAS_VERSION = '3'
CAS_ADMIN_REDIRECT = False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(base, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'stagingcontext.staging_processor',
                'gacontext.ga_processor',
                'django.template.context_processors.csrf',
                'blackrock.blackrock_main.views.django_settings'
            ],
        },
    },
]
