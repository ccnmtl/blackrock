from django.conf.urls import url
import os.path

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    url(r'^$', 'blackrock.optimization.views.index'),
    url(r'^run$', 'blackrock.optimization.views.run'),
    url(r'^calculate$', 'blackrock.optimization.views.calculate'),
    url(r'^trees.png$', 'blackrock.optimization.views.tree_png'),

    url(r'^csv$', 'blackrock.optimization.views.export_csv'),
    url(r'^json2csv$', 'blackrock.optimization.views.json2csv'),
    url(r'^trees_csv$', 'blackrock.optimization.views.trees_csv'),

    url(r'^test$', 'blackrock.optimization.views.test'),
    url(r'^loadcsv$', 'blackrock.optimization.views.loadcsv'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': media_root}),
]
