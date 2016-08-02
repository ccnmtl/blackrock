import os.path
import django.views.static

from django.conf.urls import url
from django.views.generic.base import TemplateView
import django_databrowse

from blackrock.portal.search import PortalSearchView, PortalSearchForm

from .views import page, nearby

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    url(r'^media/(?P<path>.*)$', django.views.static.serve,
        {'document_root': media_root}),
    url(r'^browse/(.*)', django_databrowse.site.root),
    url(r'^search/', PortalSearchView(
        template="portal/search.html",
        form_class=PortalSearchForm), name='search'),
    url(r'^nearby/(?P<latitude>-?\d+\.\d+)/(?P<longitude>-?\d+\.\d+)/$',
        nearby),
    url(r'^weather/$', TemplateView.as_view(
        template_name='portal/weather.html')),
    url(r'^(?P<path>.*)$', page)
]
