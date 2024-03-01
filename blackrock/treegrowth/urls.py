from django.urls import path
from django.views.generic.base import TemplateView


urlpatterns = [
    path('',
         TemplateView.as_view(template_name='treegrowth/index.html'),
         name='treegrowth-index'),
    path('graph/',
         TemplateView.as_view(template_name='treegrowth/graph.html'),
         name='treegrowth-graph'),
    path('notes/',
         TemplateView.as_view(template_name='treegrowth/notes.html'),
         name='treegrowth-notes'),
]
