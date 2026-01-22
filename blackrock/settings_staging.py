# flake8: noqa
from django.conf import settings
from blackrock.settings_shared import *
from ctlsettings.staging import common, init_sentry


locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
        s3static=True,
        s3prefix='ccnmtl'
    ))

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'blackrock',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',  # nosec
    }
}

try:
    from blackrock.local_settings import *
except ImportError:
    pass


if hasattr(settings, 'SENTRY_DSN'):
    init_sentry(SENTRY_DSN)  # noqa F405
