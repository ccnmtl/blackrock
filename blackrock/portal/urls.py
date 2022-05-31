import os.path

from django.conf.urls import url
from django.views.generic.base import TemplateView
import django.views.static


from blackrock.portal.search import PortalSearchView, PortalSearchForm

from blackrock.portal.views import PortalPageView, nearby, portal_databrowse


media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    url(r'^media/(?P<path>.*)$', django.views.static.serve,
        {'document_root': media_root}),
    url(r'^browse/(.*)', portal_databrowse),
    url(r'^search/', PortalSearchView(
        template="portal/search.html",
        form_class=PortalSearchForm), name='portal-search'),
    url(r'^nearby/(?P<latitude>-?\d+\.\d+)/(?P<longitude>-?\d+\.\d+)/$',
        nearby),
    url(r'^weather/$', TemplateView.as_view(
        template_name='portal/weather.html')),
    url(r'^(?P<path>.*)$', PortalPageView.as_view())
]
