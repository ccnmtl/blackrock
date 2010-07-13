from django.conf.urls.defaults import *
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
	(r'^$', 'blackrock.optimization.views.index'),
	(r'^run$', 'blackrock.optimization.views.run'),
	(r'^calculate$', 'blackrock.optimization.views.calculate'),
	(r'^trees.png$', 'blackrock.optimization.views.tree_png'),
	(r'^csv$', 'blackrock.optimization.views.export_csv'),
	(r'^test$', 'blackrock.optimization.views.test'),
	(r'^loadcsv$', 'blackrock.optimization.views.loadcsv'),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
)
