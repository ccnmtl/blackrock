from django.conf.urls.defaults import *
import os.path
from django.contrib import databrowse
from haystack.views import SearchView, FacetedSearchView
from haystack.forms import SearchForm, ModelSearchForm, FacetedSearchForm
from haystack.query import SearchQuerySet
from portal.search import PortalSearchView, PortalSearchForm

media_root = os.path.join(os.path.dirname(__file__),"media")

sqs = SearchQuerySet().facet('audience')

urlpatterns = patterns('',
				(r'^$', 'blackrock.portal.views.index'),
				(r'^browse/(.*)', databrowse.site.root),
        url(r'^facet/', PortalSearchView(template="portal/facet.html", form_class=PortalSearchForm), name='haystack_facet_search'),
				url(r'^textsearch/', SearchView(template="portal/textsearch.html", form_class=SearchForm), name='haystack_text_search'),
				url(r'^modelsearch/', SearchView(template="portal/modelsearch.html", form_class=ModelSearchForm), name='haystack_model_search'),
				url(r'^singlefacet/', FacetedSearchView(template="portal/singlefacet.html", form_class=FacetedSearchForm, searchqueryset=sqs), name='haystack_single_facet')
)



