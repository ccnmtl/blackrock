from django.conf.urls.defaults import *
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
	(r'^$', 'blackrock.paleoecology.views.index'),
        (r'^identification$', 'blackrock.paleoecology.views.identification'),
        (r'^coresample$', 'blackrock.paleoecology.views.coresample'),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
#        (r'^loadcsv$', 'blackrock.paleoecology.views.loadcsv'),
#        (r'^getcsv$', 'blackrock.paleoecology.views.getcsv'),
#        (r'^getsum$', 'blackrock.paleoecology.views.getsum'),
)
