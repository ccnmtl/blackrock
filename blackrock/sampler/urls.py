import os.path
from django.conf.urls import url
from django.views.static import serve

from .views import (
    index, plot, transect, worksheet, export_csv, import_csv,
)

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    url(r'^$', index),
    url(r'^plot$', plot),
    url(r'^transect$', transect),
    url(r'^worksheet$', worksheet),
    url(r'^csv$', export_csv),
    url(r'^import_csv$', import_csv),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': media_root}),
]
