import os.path
import django.views.static

from django.conf.urls import url
from django.views.generic.base import TemplateView

from blackrock.paleoecology.views import (
    index, explore, getpercents
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
        {'document_root': data_root})
]
