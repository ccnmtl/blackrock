import os.path
import django.views.static

from django.urls import path, re_path
from django.views.generic.base import TemplateView

from blackrock.paleoecology.views import (
    index, explore, getpercents
)

media_root = os.path.join(os.path.dirname(__file__), "media")
data_root = os.path.join(os.path.dirname(__file__), "data")

urlpatterns = [
    path('', index),
    path('identification', TemplateView.as_view(
        template_name='paleoecology/identification.html')),
    path('explore', explore),
    path('resources', TemplateView.as_view(
        template_name='paleoecology/resources.html')),
    path('getpercents', getpercents),
    re_path(r'^media/(?P<path>.*)$', django.views.static.serve,
            {'document_root': media_root}),
    re_path(r'^data/(?P<path>.*)$', django.views.static.serve,
            {'document_root': data_root})
]
