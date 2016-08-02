from django.conf.urls import url


urlpatterns = [
    url(r'^loadsolrpoll$', 'blackrock.blackrock_main.views.loadsolr_poll'),
    url(r'^previewsolr$', 'blackrock.blackrock_main.views.previewsolr')
]
