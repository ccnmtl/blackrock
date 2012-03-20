from django.conf.urls.defaults import *
import os.path
from django.contrib import databrowse
from portal.search import PortalSearchView, PortalSearchForm

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
				(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
				(r'^browse/(.*)', databrowse.site.root),
				(r'^mobile/(.*)$', 'blackrock.portal.views.mobile'),
				url(r'^search/', PortalSearchView(template="portal/search.html", form_class=PortalSearchForm), name='search'),
				url(r'^nearby/(?P<latitude>-?\d+\.\d+)/(?P<longitude>-?\d+\.\d+)/$', 'blackrock.portal.views.nearby'),
				(r'^grid/',       'blackrock.portal.views.grid' ),
				(r'^grid_block/', 'blackrock.portal.views.grid_block' ),
				(r'^(?P<path>.*)$','blackrock.portal.views.page'),
)



