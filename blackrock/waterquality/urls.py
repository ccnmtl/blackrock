from django.conf.urls import url
from django.views.generic.base import TemplateView

from .views import (
    BrowseView, GraphingToolView, SeriesView, SeriesAllView,
    SeriesVerifyView,
)


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='waterquality/index.html'),
        name='waterchemistry-index'),
    url(r'^graph/$', GraphingToolView.as_view(),
        name='waterchemistry-graphing-tool'),
    url(r'^browse/$', BrowseView.as_view(), name='waterchemistry-browse'),
    url(r'^series/(?P<pk>\d+)/$', SeriesView.as_view(),
        name='waterchemistry-series'),
    url(r'^series/(?P<pk>\d+)/all/$',
        SeriesAllView.as_view(), name='waterchemistry-series-all'),
    url(r'^series/(?P<pk>\d+)/verify/$',
        SeriesVerifyView.as_view(), name='waterchemistry-series-verify'),
    url(r'^teaching/$',
        TemplateView.as_view(template_name='waterquality/teaching.html'),
        name='waterchemistry-teaching'),
]
