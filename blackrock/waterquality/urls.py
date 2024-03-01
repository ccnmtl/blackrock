from django.urls import path, re_path
from django.views.generic.base import TemplateView

from .views import (
    BrowseView, GraphingToolView, SeriesView, SeriesAllView,
    SeriesVerifyView,
)


urlpatterns = [
    path('', TemplateView.as_view(template_name='waterquality/index.html'),
         name='waterchemistry-index'),
    path('graph/', GraphingToolView.as_view(),
         name='waterchemistry-graphing-tool'),
    path('browse/', BrowseView.as_view(), name='waterchemistry-browse'),
    re_path(r'^series/(?P<pk>\d+)/$', SeriesView.as_view(),
            name='waterchemistry-series'),
    re_path(r'^series/(?P<pk>\d+)/all/$',
            SeriesAllView.as_view(), name='waterchemistry-series-all'),
    re_path(r'^series/(?P<pk>\d+)/verify/$',
            SeriesVerifyView.as_view(), name='waterchemistry-series-verify'),
    path('teaching/',
         TemplateView.as_view(template_name='waterquality/teaching.html'),
         name='waterchemistry-teaching'),
]
