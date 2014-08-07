from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template
import os.path

media_root = os.path.join(os.path.dirname(__file__), "media")
data_root = os.path.join(os.path.dirname(__file__), "data")

urlpatterns = patterns(
    '',
    (r'^$', 'blackrock.paleoecology.views.index'),
    (r'^identification$', direct_to_template,
     {'template': 'paleoecology/identification.html'}),
    (r'^explore$', 'blackrock.paleoecology.views.explore'),
    (r'^resources$', direct_to_template,
     {'template': 'paleoecology/resources.html'}),
    (r'^getpercents$', 'blackrock.paleoecology.views.getpercents'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': media_root}),
    (r'^data/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': data_root}),
    (r'^loadcounts$', 'blackrock.paleoecology.views.loadcounts'),
    (r'^loadpercents$', 'blackrock.paleoecology.views.loadpercents'),
    (r'^loadsolr$', 'blackrock.paleoecology.views.loadsolr')
)
