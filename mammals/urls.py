from django.conf.urls.defaults import *
import os.path
from django.contrib import databrowse
from portal.search import PortalSearchView, PortalSearchForm

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
				(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
				(r'^$',              'blackrock.mammals.views.grid' ),
				(r'^grid/',          'blackrock.mammals.views.grid' ),
				(r'^grid_square/',   'blackrock.mammals.views.grid_block' ),
)
