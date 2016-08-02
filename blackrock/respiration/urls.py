import os.path

from django.conf.urls import url
from django.views.generic.base import TemplateView


media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    url(r'^$', 'blackrock.respiration.views.index'),
    url(r'^leaf$', 'blackrock.respiration.views.leaf'),
    url(r'^forest$', 'blackrock.respiration.views.forest'),
    url(r'^resources/',
        TemplateView.as_view(template_name='respiration/resources.html')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': media_root}),
    url(r'^loadcsv$', 'blackrock.respiration.views.loadcsv'),
    url(r'^getcsv$', 'blackrock.respiration.views.getcsv'),
    url(r'^getsum$', 'blackrock.respiration.views.getsum'),
    url(r'^loadsolr$', 'blackrock.respiration.views.loadsolr')
]
