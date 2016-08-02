from django.conf.urls import url
import os.path
import django.views.static
from .views import (
    index, run, calculate, tree_png, export_csv, json2csv, trees_csv,
    test, loadcsv,
)

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    url(r'^$', index),
    url(r'^run$', run),
    url(r'^calculate$', calculate),
    url(r'^trees.png$', tree_png),

    url(r'^csv$', export_csv),
    url(r'^json2csv$', json2csv),
    url(r'^trees_csv$', trees_csv),

    url(r'^test$', test),
    url(r'^loadcsv$', loadcsv),
    url(r'^media/(?P<path>.*)$', django.views.static.serve,
        {'document_root': media_root}),
]
