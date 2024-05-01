from django.urls import path, re_path
import os.path
import django.views.static
from .views import (
    index, run, calculate, tree_png, export_csv, json2csv, trees_csv,
    test, loadcsv,
)

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    path('', index),
    path('run', run),
    path('calculate', calculate),
    path('trees.png', tree_png),

    path('csv', export_csv),
    path('json2csv', json2csv),
    path('trees_csv', trees_csv),

    path('test', test),
    path('loadcsv', loadcsv),
    re_path(r'^media/(?P<path>.*)$', django.views.static.serve,
            {'document_root': media_root}),
]
