from blackrock.portal.views import (
    admin_rebuild_index, admin_cdrs_import, admin_readercycle,
)
from blackrock.views import index
from django.conf import settings
from django.urls import include, path, re_path
from django.contrib.auth.decorators import login_required
from django.contrib.gis import admin
from django.views.static import serve
from django_cas_ng import views as cas_views
from pagetree.generic.views import EditView


admin.autodiscover()

urlpatterns = [
    path('accounts', include('django.contrib.auth.urls')),
    path('cas/login', cas_views.LoginView.as_view(),
         name='cas_ng_login'),
    path('cas/logout', cas_views.LogoutView.as_view(),
         name='cas_ng_logout'),
    path('smoketest/', include('smoketest.urls')),
    path('pagetree/', include('pagetree.urls')),
    path('admin/portal/rebuild_index', admin_rebuild_index),
    path('admin/portal/import_cdrs', admin_cdrs_import),
    path('admin/portal/readercycle', admin_readercycle),
    path('admin/', admin.site.urls),
    re_path(r'^uploads/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
    path('respiration/', include('blackrock.respiration.urls')),
    path('optimization/', include('blackrock.optimization.urls')),
    path('paleoecology/', include('blackrock.paleoecology.urls')),
    path('waterchemistry/', include('blackrock.waterquality.urls')),
    path('waterquality/', include('blackrock.waterquality.urls')),
    path('treegrowth/', include('blackrock.treegrowth.urls')),
    path('blackrock_main/', include('blackrock.blackrock_main.urls')),

    # portal pagetree content
    re_path(
        r'^edit/(?P<path>.*)$', login_required(EditView.as_view(
            hierarchy_name="main", hierarchy_base="/"))),
    path('portal/', include('blackrock.portal.urls')),
    path('mammals/', include('blackrock.mammals.urls')),
    path('', index),
    re_path(r'^uploads/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
