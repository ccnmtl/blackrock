from django.conf.urls.defaults import *
import os.path

urlpatterns = patterns('',
        (r'^loadsolrpoll$', 'blackrock.blackrock_main.views.loadsolr_poll'),
        (r'^previewsolr$', 'blackrock.blackrock_main.views.previewsolr'),
)