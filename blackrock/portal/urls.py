import os.path

from django.urls import path, re_path
from django.views.generic.base import TemplateView
import django.views.static


from blackrock.portal.search import PortalSearchView, PortalSearchForm

from blackrock.portal.views import PortalPageView, nearby, portal_databrowse


media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', django.views.static.serve,
            {'document_root': media_root}),
    re_path(r'^browse/(.*)', portal_databrowse),
    path('search/', PortalSearchView(
        template="portal/search.html",
        form_class=PortalSearchForm), name='portal-search'),
    re_path(r'^nearby/(?P<latitude>-?\d+\.\d+)/(?P<longitude>-?\d+\.\d+)/$',
            nearby),
    path('weather/', TemplateView.as_view(
        template_name='portal/weather.html')),
    re_path(r'^(?P<path>.*)$', PortalPageView.as_view())
]
