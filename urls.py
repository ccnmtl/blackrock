from django.conf.urls.defaults import *
#from django.contrib import admin
from django.contrib.gis import admin
from django.conf import settings
from blackrock_main.urls import *
import os.path

admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
                       ('^accounts/',include('djangowind.urls')),
                       (r'^admin/portal/', include('gspreadsheet_importer.urls')),
                       (r'^admin/portal/rebuild_index', 'blackrock.portal.views.admin_rebuild_index'),
                       (r'^admin/(.*)', admin.site.root),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
                       (r'^sampler/', include('blackrock.sampler.urls')),
                       (r'^respiration/', include('blackrock.respiration.urls')),
                       (r'^optimization/', include('blackrock.optimization.urls')),
                       (r'^paleoecology/', include('blackrock.paleoecology.urls')),
                       (r'^blackrock_main/', include('blackrock.blackrock_main.urls')),
                       (r'^portal/', include('blackrock.portal.urls')),
                       (r'', 'blackrock.views.index')
)
