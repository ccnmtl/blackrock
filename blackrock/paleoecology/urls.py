import os.path

from django.conf.urls import patterns
from django.views.generic.base import TemplateView

media_root = os.path.join(os.path.dirname(__file__), "media")
data_root = os.path.join(os.path.dirname(__file__), "data")

urlpatterns = patterns(
    '',
    (r'^$', 'blackrock.paleoecology.views.index'),
    (r'^identification$',
     TemplateView.as_view(template_name='paleoecology/identification.html')),
    (r'^explore$', 'blackrock.paleoecology.views.explore'),
    (r'^resources$',
     TemplateView.as_view(template_name='paleoecology/resources.html')),
    (r'^getpercents$', 'blackrock.paleoecology.views.getpercents'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': media_root}),
    (r'^data/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': data_root}),
    (r'^loadcounts$', 'blackrock.paleoecology.views.loadcounts'),
    (r'^loadpercents$', 'blackrock.paleoecology.views.loadpercents'),
    (r'^loadsolr$', 'blackrock.paleoecology.views.loadsolr')
)
