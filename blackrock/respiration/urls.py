import os.path

from django.urls import path, re_path
from django.views.generic.base import TemplateView
from django.views.static import serve

from .views import (
    index, leaf, forest, loadcsv, getcsv, getsum, loadsolr,
)


media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    path('', index),
    path('leaf', leaf),
    path('forest', forest),
    path('resources/', TemplateView.as_view(
        template_name='respiration/resources.html')),
    re_path('media/(?P<path>.*)$', serve, {'document_root': media_root}),
    path('loadcsv', loadcsv),
    path('getcsv', getcsv),
    path('getsum', getsum),
    path('loadsolr', loadsolr)
]
