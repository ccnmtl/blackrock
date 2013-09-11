from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template
import os.path

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = patterns(
    '',
    (r'^$', 'blackrock.respiration.views.index'),
    (r'^leaf$', 'blackrock.respiration.views.leaf'),
    (r'^forest$', 'blackrock.respiration.views.forest'),
    (r'^resources/', direct_to_template,
     {'template': 'respiration/resources.html'}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
     'document_root': media_root}),
    (r'^loadcsv$', 'blackrock.respiration.views.loadcsv'),
    (r'^getcsv$', 'blackrock.respiration.views.getcsv'),
    (r'^getsum$', 'blackrock.respiration.views.getsum'),
    (r'^loadsolr$', 'blackrock.respiration.views.loadsolr')
)
