from django.conf.urls import url
from .views import loadsolr_poll, previewsolr

urlpatterns = [
    url(r'^loadsolrpoll$', loadsolr_poll),
    url(r'^previewsolr$', previewsolr),
]
