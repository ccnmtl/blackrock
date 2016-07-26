import os.path

from django.conf import settings
from django.conf.urls import patterns, include
from django.contrib.auth.decorators import login_required
from django.contrib.gis import admin
from pagetree.generic.views import EditView


admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

urlpatterns = patterns(
    '',
    ('^accounts/', include('djangowind.urls')),
    (r'^smoketest/', include('smoketest.urls')),
    (r'^pagetree/', include('pagetree.urls')),
    (r'^admin/portal/rebuild_index',
     'blackrock.portal.views.admin_rebuild_index'),
    (r'^admin/portal/import_cdrs', 'blackrock.portal.views.admin_cdrs_import'),
    (r'^admin/portal/readercycle', 'blackrock.portal.views.admin_readercycle'),
    (r'^admin/', include(admin.site.urls)),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': site_media_root}),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
    (r'^sampler/', include('blackrock.sampler.urls')),
    (r'^respiration/', include('blackrock.respiration.urls')),
    (r'^optimization/', include('blackrock.optimization.urls')),
    (r'^paleoecology/', include('blackrock.paleoecology.urls')),
    (r'^waterchemistry/', include('blackrock.waterquality.urls')),
    (r'^waterquality/', include('blackrock.waterquality.urls')),
    (r'^treegrowth/', include('blackrock.treegrowth.urls')),
    (r'^blackrock_main/', include('blackrock.blackrock_main.urls')),

    # portal pagetree content
    (r'^edit/(?P<path>.*)$', login_required(EditView.as_view(
        hierarchy_name="main", hierarchy_base="/"))),
    (r'^portal/', include('blackrock.portal.urls')),
    (r'^mammals/', include('blackrock.mammals.urls')),
    (r'^$', 'blackrock.views.index'),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
