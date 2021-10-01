from blackrock.portal.views import (
    admin_rebuild_index, admin_cdrs_import, admin_readercycle,
)
from blackrock.views import index
from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.contrib.gis import admin
from django.urls import path
from django.views.static import serve
from django_cas_ng import views as cas_views
from pagetree.generic.views import EditView


admin.autodiscover()

urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    path('cas/login', cas_views.LoginView.as_view(),
         name='cas_ng_login'),
    path('cas/logout', cas_views.LogoutView.as_view(),
         name='cas_ng_logout'),
    url(r'^smoketest/', include('smoketest.urls')),
    url(r'^pagetree/', include('pagetree.urls')),
    url(r'^admin/portal/rebuild_index', admin_rebuild_index),
    url(r'^admin/portal/import_cdrs', admin_cdrs_import),
    url(r'^admin/portal/readercycle', admin_readercycle),
    url(r'^admin/', admin.site.urls),
    url(r'^uploads/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
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
    url(r'^$', index),
    url(r'^uploads/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
