import os.path

from django.conf.urls import patterns
from django.views.generic.base import TemplateView


media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = patterns(
    '',
    (r'^$', 'blackrock.respiration.views.index'),
    (r'^leaf$', 'blackrock.respiration.views.leaf'),
    (r'^forest$', 'blackrock.respiration.views.forest'),
    (r'^resources/',
     TemplateView.as_view(template_name='respiration/resources.html')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
     'document_root': media_root}),
    (r'^loadcsv$', 'blackrock.respiration.views.loadcsv'),
    (r'^getcsv$', 'blackrock.respiration.views.getcsv'),
    (r'^getsum$', 'blackrock.respiration.views.getsum'),
    (r'^loadsolr$', 'blackrock.respiration.views.loadsolr')
)
