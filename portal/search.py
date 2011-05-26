from django import forms
from haystack.views import SearchView, FacetedSearchView
from haystack.forms import *
from portal.models import *
from django.utils.translation import ugettext_lazy as _
from django.db.models import get_model, get_app
from django.utils.text import capfirst

class PortalSearchForm(SearchForm):

  def default_type_choices(site=None):
    if site is None:
        site = haystack.site
    
    choices = [(m._meta.object_name, m._meta.verbose_name) for m in site.get_indexed_models()]
    choices.sort()
    return choices
  
  def default_facet_choices(facet):
    choices = [ (f.name, f.display_name) for f in Facet.objects.filter(facet=facet)]
    choices.sort()
    return choices

  asset_type = forms.MultipleChoiceField(required=False, label=_('Record Type'), widget=forms.CheckboxSelectMultiple, choices=default_type_choices())
  study_type = forms.MultipleChoiceField(required=False, label=_('Study Type'), widget=forms.CheckboxSelectMultiple, choices=default_facet_choices("Study Type"))
  species = forms.MultipleChoiceField(required=False, label=_('Species'), widget=forms.CheckboxSelectMultiple, choices=default_facet_choices("Species"))
  discipline = forms.MultipleChoiceField(required=False, label=_('Discipline'), widget=forms.CheckboxSelectMultiple, choices=default_facet_choices("Discipline"))
  
  def __init__(self, *args, **kwargs):
    super(PortalSearchForm, self).__init__(*args, **kwargs)
  
  def get_multiplechoicefield(self, name):
    query = ""
    
    if hasattr(self, "cleaned_data"):
      if name in self.cleaned_data:
        for a in self.cleaned_data[name]:
          if len(query):
            query += ' OR '
          query += "%s:%s" % (name, a)
    
    return query
  
  def search(self):
    sqs = []
    self.hidden = []
    
    """Filter by full text search string or empty string if does not exist"""
    if not hasattr(self, "cleaned_data"):
      sqs = self.searchqueryset.auto_query("").order_by("name")

      if self.load_all:
        sqs = sqs.load_all()
      
      for facet in Facet.asset_facets:
        sqs = sqs.facet(facet)
        if facet in self.fields:
          if len(self.fields[facet].choices) > 0:
            self.fields[facet].choices = []
      
    elif self.is_valid():
      q = self.cleaned_data['q'].lower()
      sqs = self.searchqueryset.auto_query(q).order_by("name")

      if self.load_all:
        sqs = sqs.load_all()
      
      for facet in Facet.asset_facets:
        sqs = sqs.facet(facet)
        if facet in self.fields:
          self.fields[facet].choices = []
        
      for facet in Facet.asset_facets:
        query = self.get_multiplechoicefield(facet)
        if len(query):
          sqs = sqs.narrow(query)

    # facet counts based on result set
    if len(sqs) > 0:
      counts = sqs.facet_counts()
      for facet in counts['fields']:
        if facet in self.fields:
          for key, value in counts['fields'][facet]:
            if value > 0:
              # Look up the display name for this facet
              display_name = key
              try:
                x = Facet.objects.get(name=key)
                display_name = x.display_name
              except:
                model = get_model("portal", key)
                if model:
                  display_name = capfirst(model._meta.verbose_name)
                
              choice = (key, "%s (%s)" % (display_name, value))
              self.fields[facet].choices.append(choice)
  
          self.fields[facet].choices.sort()
          
    return sqs
    
class PortalSearchView(SearchView):
  def __name__(self):
      return "PortalSearchView"
    
  def get_results(self):
    return self.form.search()
    
  def extra_context(self):
    extra = super(PortalSearchView, self).extra_context()
    if hasattr(self, "results"):
      extra["count"] = len(self.results)
      
    # Send down our current parameters minus page number
    query = ''
    for param, value in self.request.GET.items():
      if param != 'page':
        query += '%s=%s&' % (param, value) 
    extra['query'] = query
    return extra


    

    
    
