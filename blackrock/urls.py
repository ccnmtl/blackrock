import os.path

from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.contrib.gis import admin
from pagetree.generic.views import EditView


admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

urlpatterns = [
    url('^accounts/', include('djangowind.urls')),
    url(r'^smoketest/', include('smoketest.urls')),
    url(r'^pagetree/', include('pagetree.urls')),
    url(r'^admin/portal/rebuild_index',
        'blackrock.portal.views.admin_rebuild_index'),
    url(r'^admin/portal/import_cdrs',
        'blackrock.portal.views.admin_cdrs_import'),
    url(r'^admin/portal/readercycle',
        'blackrock.portal.views.admin_readercycle'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': site_media_root}),
    url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^sampler/', include('blackrock.sampler.urls')),
    url(r'^respiration/', include('blackrock.respiration.urls')),
    url(r'^optimization/', include('blackrock.optimization.urls')),
    url(r'^paleoecology/', include('blackrock.paleoecology.urls')),
    url(r'^waterchemistry/', include('blackrock.waterquality.urls')),
    url(r'^waterquality/', include('blackrock.waterquality.urls')),
    url(r'^treegrowth/', include('blackrock.treegrowth.urls')),
    url(r'^blackrock_main/', include('blackrock.blackrock_main.urls')),

    # portal pagetree content
    url(r'^edit/(?P<path>.*)$', login_required(EditView.as_view(
        hierarchy_name="main", hierarchy_base="/"))),
    url(r'^portal/', include('blackrock.portal.urls')),
    url(r'^mammals/', include('blackrock.mammals.urls')),
    url(r'^$', 'blackrock.views.index'),
    url(r'^uploads/(?P<path>.*)$',
        'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]
