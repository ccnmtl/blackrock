import os.path

from django.conf.urls import url
from django.views.generic.base import TemplateView

media_root = os.path.join(os.path.dirname(__file__), "media")
data_root = os.path.join(os.path.dirname(__file__), "data")

urlpatterns = [
    url(r'^$', 'blackrock.paleoecology.views.index'),
    url(r'^identification$', TemplateView.as_view(
        template_name='paleoecology/identification.html')),
    url(r'^explore$', 'blackrock.paleoecology.views.explore'),
    url(r'^resources$',
        TemplateView.as_view(template_name='paleoecology/resources.html')),
    url(r'^getpercents$', 'blackrock.paleoecology.views.getpercents'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': media_root}),
    url(r'^data/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': data_root}),
    url(r'^loadcounts$', 'blackrock.paleoecology.views.loadcounts'),
    url(r'^loadpercents$', 'blackrock.paleoecology.views.loadpercents'),
    url(r'^loadsolr$', 'blackrock.paleoecology.views.loadsolr')
]
