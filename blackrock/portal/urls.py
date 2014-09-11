import os.path

from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
import django_databrowse
from pagetree.generic.views import EditView

from blackrock.portal.search import PortalSearchView, PortalSearchForm


media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = patterns(
    '',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': media_root}),

    (r'^browse/(.*)', django_databrowse.site.root),

    url(r'^search/',
        PortalSearchView(template="portal/search.html",
                         form_class=PortalSearchForm),
        name='search'),

    url(r'^nearby/(?P<latitude>-?\d+\.\d+)/(?P<longitude>-?\d+\.\d+)/$',
        'blackrock.portal.views.nearby'),

    url(r'^weather/$',
        TemplateView.as_view(template_name='portal/weather.html')),

    (r'^edit/(?P<path>.*)$', EditView.as_view(
        hierarchy_name="main", hierarchy_base="/")),

    (r'^(?P<path>.*)$', 'blackrock.portal.views.page')
)
