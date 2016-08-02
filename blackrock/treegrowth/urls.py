from django.conf.urls import url
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name='treegrowth/index.html'),
        name='treegrowth-index'),
    url(r'^graph/$',
        TemplateView.as_view(template_name='treegrowth/graph.html'),
        name='treegrowth-graph'),
]
