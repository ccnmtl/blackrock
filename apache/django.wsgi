import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/blackrock/blackrock/ve/lib/python2.7/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/var/www/blackrock/blackrock/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'blackrock.settings_production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
