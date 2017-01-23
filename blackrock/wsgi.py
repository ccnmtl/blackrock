import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "blackrock.settings")
application = get_wsgi_application()
