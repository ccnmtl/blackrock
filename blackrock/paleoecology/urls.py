import os.path
import django.views.static

from django.conf.urls import url
from django.views.generic.base import TemplateView

from .views import (
    index, explore, getpercents, loadcounts, loadpercents, loadsolr
)

media_root = os.path.join(os.path.dirname(__file__), "media")
data_root = os.path.join(os.path.dirname(__file__), "data")

urlpatterns = [
    url(r'^$', index),
    url(r'^identification$', TemplateView.as_view(
        template_name='paleoecology/identification.html')),
    url(r'^explore$', explore),
    url(r'^resources$', TemplateView.as_view(
        template_name='paleoecology/resources.html')),
    url(r'^getpercents$', getpercents),
    url(r'^media/(?P<path>.*)$', django.views.static.serve,
        {'document_root': media_root}),
    url(r'^data/(?P<path>.*)$', django.views.static.serve,
        {'document_root': data_root}),
    url(r'^loadcounts$', loadcounts),
    url(r'^loadpercents$', loadpercents),
    url(r'^loadsolr$', loadsolr)
]
