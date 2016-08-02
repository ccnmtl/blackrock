import os.path

from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.views.static import serve

from .views import (
    index, leaf, forest, loadcsv, getcsv, getsum, loadsolr,
)


media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    url(r'^$', index),
    url(r'^leaf$', leaf),
    url(r'^forest$', forest),
    url(r'^resources/', TemplateView.as_view(
        template_name='respiration/resources.html')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': media_root}),
    url(r'^loadcsv$', loadcsv),
    url(r'^getcsv$', getcsv),
    url(r'^getsum$', getsum),
    url(r'^loadsolr$', loadsolr)
]
