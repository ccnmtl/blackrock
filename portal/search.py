from django import forms
from haystack.views import SearchView, FacetedSearchView
from haystack.forms import *
from portal.models import *
from django.utils.translation import ugettext_lazy as _

_facets = ['audience', 'study_type', 'species', 'discipline', 'asset_type']

class PortalSearchForm(FacetedSearchForm):

  audience = forms.MultipleChoiceField(required=False, label=_('Audience'), widget=forms.CheckboxSelectMultiple)
  asset_type = forms.ChoiceField(required=False, label=_('Asset Type'), widget=forms.RadioSelect)
  study_type = forms.MultipleChoiceField(required=False, label=_('Study Type'), widget=forms.CheckboxSelectMultiple)
  species = forms.MultipleChoiceField(required=False, label=_('Species'), widget=forms.CheckboxSelectMultiple)
  discipline = forms.MultipleChoiceField(required=False, label=_('Discipline'), widget=forms.CheckboxSelectMultiple)

  
  def __init__(self, *args, **kwargs):
    super(PortalSearchForm, self).__init__(*args, **kwargs)
  
  def get_multiplechoicefield(self, name):
    query = ""
    
    if hasattr(self, "cleaned_data"):
      if type(self.cleaned_data[name]) == type(list()):
        for a in self.cleaned_data[name]:
          if len(query):
            query += ' OR '
          query += "%s:%s" % (name, a)
      else:
        query += "%s:%s" % (name, self.cleaned_data[name])
    
    return query
  
  def search(self):
    sqs = []
    
    """Filter by full text search string or empty string if does not exist"""
    if not hasattr(self, "cleaned_data"):
      sqs = self.searchqueryset.auto_query("").order_by("name")
      
      for facet in _facets:
        sqs = sqs.facet(facet)
        if len(self.fields[facet].choices) > 0:
          self.fields[facet].choices = []
      
      if self.load_all:
        sqs = sqs.load_all()
      
    elif self.is_valid():
      sqs = self.searchqueryset.auto_query(self.cleaned_data['q']).order_by("name")
      
      for facet in _facets:
        sqs = sqs.facet(facet)
        self.fields[facet].choices = []

      if self.load_all:
        sqs = sqs.load_all()
        
      for facet in _facets:
        query = self.get_multiplechoicefield(facet)
        if len(query):
          sqs = sqs.narrow(query)

    # facet counts based on result set
    if len(sqs) > 0:
      counts = sqs.facet_counts()
      for facet in counts['fields']:
        for key, value in counts['fields'][facet]:
          choice = (key, "%s (%s)" % (key, value))
          self.fields[facet].choices.append(choice)
          
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
    return extra


    

    
    
