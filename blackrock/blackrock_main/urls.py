from django.urls import path
from .views import loadsolr_poll, previewsolr

urlpatterns = [
    path('loadsolrpoll', loadsolr_poll),
    path('previewsolr', previewsolr),
]
