from django.conf.urls.defaults import *
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
	(r'^$', 'blackrock.paleoecology.views.index'),
        (r'^identification$', 'blackrock.paleoecology.views.identification'),
        (r'^explore$', 'blackrock.paleoecology.views.explore'),
        (r'^results$', 'blackrock.paleoecology.views.results'),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
        (r'^loadcounts$', 'blackrock.paleoecology.views.loadcounts'),
        (r'^loadpercents$', 'blackrock.paleoecology.views.loadpercents'),
#        (r'^loadcsv$', 'blackrock.paleoecology.views.loadcsv'),
#        (r'^getcsv$', 'blackrock.paleoecology.views.getcsv'),
#        (r'^getsum$', 'blackrock.paleoecology.views.getsum'),
)
