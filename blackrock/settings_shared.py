import platform
import os.path
import sys
from ccnmtlsettings.shared import common

project = 'blackrock'
base = os.path.dirname(__file__)
locals().update(common(project=project, base=base))

if platform.linux_distribution()[1] == '16.04':
    # 15.04 and later need this set, but it breaks
    # on trusty.
    # yeah, it's not really going to work on non-Ubuntu
    # systems either, but I don't know a good way to
    # check for the specific issue. Anyone not running
    # ubuntu will just need to set this to the
    # appropriate value in their local_settings.py
    SPATIALITE_LIBRARY_PATH = 'mod_spatialite'

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
    'blackrock.sampler',
    'blackrock.treegrowth',
    'blackrock.waterquality',
]

TEMPLATES[0]['OPTIONS']['context_processors'].append(  # noqa
    'blackrock.blackrock_main.views.django_settings'
)

MIDDLEWARE_CLASSES += [  # noqa
    'blackrock.portal.middleware.ValueErrorMiddleware',
]

INSTALLED_APPS += [  # noqa
    'sorl.thumbnail',
    'django.contrib.gis',
    'blackrock.sampler',
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
    'template_utils',
    'blackrock.waterquality',
    'blackrock.mammals',
    'bootstrapform',
    'django_extensions',
    'django.contrib.humanize'
]

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
