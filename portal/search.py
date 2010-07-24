from django import forms
from haystack.views import SearchView, FacetedSearchView
from haystack.forms import *
from portal.models import *
from django.utils.translation import ugettext_lazy as _

_facets = ['audience', 'keyword']

class PortalSearchForm(FacetedSearchForm):
  def __init__(self, *args, **kwargs):
    super(PortalSearchForm, self).__init__(*args, **kwargs)
    self.fields['audience'] = forms.ModelMultipleChoiceField(queryset=Audience.objects.all().order_by("name"), required=False, label=_('Audience'), widget=forms.CheckboxSelectMultiple)
    self.fields['models'] = forms.MultipleChoiceField(choices=model_choices(), required=False, label=_('Types'), widget=forms.CheckboxSelectMultiple)
    self.fields['keyword'] = forms.ModelMultipleChoiceField(queryset=Keyword.objects.all().order_by("name"), required=False, label=_('Keyword'), widget=forms.CheckboxSelectMultiple)
    
  def get_models(self):
    """Return an alphabetical list of model classes in the index."""
    search_models = []
    
    if hasattr(self, "cleaned_data"):
      for model in self.cleaned_data['models']:
        search_models.append(models.get_model(*model.split('.')))
    
    return search_models
  
  def get_multiplechoicefield(self, name):
    query = ""
    
    if hasattr(self, "cleaned_data"):
      for a in self.cleaned_data[name]:
        if len(query):
          query += ' OR '
        query += "%s:%s" % (name, a.name)
    return query
  
  def search(self):
    """Filter by full text search string or empty string if does not exist"""
    if not hasattr(self, "cleaned_data"):
      sqs = self.searchqueryset.auto_query("").order_by("name")
      
      if self.load_all:
        sqs = sqs.load_all()
        
      return sqs;

    elif self.is_valid():
      sqs = self.searchqueryset.auto_query(self.cleaned_data['q']).order_by("name")
        
      if self.load_all:
        sqs = sqs.load_all()
        
      for facet in _facets:
        query = self.get_multiplechoicefield(facet)
        if len(query):
          sqs = sqs.narrow(query)
        
      return sqs.models(*self.get_models())
    else:
      return []
      
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


    

    
    
