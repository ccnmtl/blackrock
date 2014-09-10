from django.conf.urls import patterns
import os.path

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = patterns('',
                      (r'^$', 'blackrock.sampler.views.index'),
                      (r'^plot$', 'blackrock.sampler.views.plot'),
                      (r'^transect$', 'blackrock.sampler.views.transect'),
                      (r'^worksheet$', 'blackrock.sampler.views.worksheet'),
                      (r'^csv$', 'blackrock.sampler.views.export_csv'),
                      (r'^import_csv$', 'blackrock.sampler.views.import_csv'),
                      (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                       {'document_root': media_root}),
                       )
