from django import forms
from haystack.views import SearchView, FacetedSearchView
from haystack.forms import *
from portal.models import *
from django.utils.translation import ugettext_lazy as _
from django.db.models import get_model

_facets = {'audience': 'Audience', 'study_type': 'Keyword', 'species': 'Keyword', 'discipline': 'Keyword' }

class PortalSearchForm(FacetedSearchForm):

  audience = forms.MultipleChoiceField(required=False, label=_('Audience'), widget=forms.CheckboxSelectMultiple)
  models = forms.MultipleChoiceField(choices=model_choices(), required=False, label=_('Types'), widget=forms.CheckboxSelectMultiple)
  study_type = forms.MultipleChoiceField(required=False, label=_('Study Type'), widget=forms.CheckboxSelectMultiple)
  species = forms.MultipleChoiceField(required=False, label=_('Species'), widget=forms.CheckboxSelectMultiple)
  discipline = forms.MultipleChoiceField(required=False, label=_('Discipline'), widget=forms.CheckboxSelectMultiple)

  
  def __init__(self, *args, **kwargs):
    super(PortalSearchForm, self).__init__(*args, **kwargs)
    
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
        m = get_model('portal', _facets[name]).objects.get(id=a)
        query += "%s:%s" % (name, m.name)
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
        
      sqs = sqs.models(*self.get_models())

    # facet counts based on result set
    if len(sqs) > 0:
      counts = sqs.facet_counts()
      for facet in counts['fields']:
        for key, value in counts['fields'][facet]:
          instance = get_model("portal", _facets[facet]).objects.get(name=key)
          choice = (instance.id, "%s (%s)" % (key, value))
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


    

    
    
