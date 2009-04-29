from django.conf.urls.defaults import *
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
	(r'^$', 'blackrock.optimization.views.index'),
	(r'^run$', 'blackrock.optimization.views.run'),
	(r'^calculate$', 'blackrock.optimization.views.calculate'),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
)
