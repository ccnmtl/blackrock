from django.conf.urls import url
import os.path

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    url(r'^$', 'blackrock.sampler.views.index'),
    url(r'^plot$', 'blackrock.sampler.views.plot'),
    url(r'^transect$', 'blackrock.sampler.views.transect'),
    url(r'^worksheet$', 'blackrock.sampler.views.worksheet'),
    url(r'^csv$', 'blackrock.sampler.views.export_csv'),
    url(r'^import_csv$', 'blackrock.sampler.views.import_csv'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': media_root}),
]
